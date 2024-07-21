import os
import sys

import nltk

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from configs import VERSION
from configs.model_config import NLTK_DATA_PATH
from configs.server_config import OPEN_CROSS_DOMAIN
import argparse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from server.chat import (
    chat,
    search_engine_chat,
)
from server.llm_api import (
    list_running_models,
    list_config_models,
    change_llm_model,
    stop_llm_model,
    get_model_config,
    list_search_engines,
)
from server.utils import (
    BaseResponse,
    FastAPI,
    MakeFastAPIOffline,
    get_server_configs,
)
from server.thread.thread import router as thread_router
from server.user.user import router as user_router

nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path


async def document():
    return RedirectResponse(url="/docs")


def create_app():
    app = FastAPI(title="Chatbot API Server", version=VERSION)
    MakeFastAPIOffline(app)
    # Add CORS middleware to allow all origins
    # 在config.py中设置OPEN_DOMAIN=True，允许跨域
    # set OPEN_DOMAIN=True in config.py to allow cross-domain
    if OPEN_CROSS_DOMAIN:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(user_router)

    app.include_router(thread_router)

    app.get("/", response_model=BaseResponse, summary="swagger 文档")(document)

    app.post("/chat/chat", tags=["Chat"], summary="与llm模型对话(通过LLMChain)")(chat)

    app.post("/chat/search_engine_chat", tags=["Chat"], summary="与搜索引擎对话")(
        search_engine_chat
    )

    # LLM模型相关接口
    app.post(
        "/llm_model/list_running_models",
        tags=["LLM Model Management"],
        summary="列出当前已加载的模型",
    )(list_running_models)

    app.post(
        "/llm_model/list_config_models",
        tags=["LLM Model Management"],
        summary="列出configs已配置的模型",
    )(list_config_models)

    app.post(
        "/llm_model/get_model_config",
        tags=["LLM Model Management"],
        summary="获取模型配置（合并后）",
    )(get_model_config)

    app.post(
        "/llm_model/stop",
        tags=["LLM Model Management"],
        summary="停止指定的LLM模型（Model Worker)",
    )(stop_llm_model)

    app.post(
        "/llm_model/change",
        tags=["LLM Model Management"],
        summary="切换指定的LLM模型（Model Worker)",
    )(change_llm_model)

    # 服务器相关接口
    app.post(
        "/server/configs",
        tags=["Server State"],
        summary="获取服务器原始配置信息",
    )(get_server_configs)

    app.post(
        "/server/list_search_engines",
        tags=["Server State"],
        summary="获取服务器支持的搜索引擎",
    )(list_search_engines)
    return app


app = create_app()


def run_api(host, port, **kwargs):
    if kwargs.get("ssl_keyfile") and kwargs.get("ssl_certfile"):
        uvicorn.run(
            app,
            host=host,
            port=port,
            ssl_keyfile=kwargs.get("ssl_keyfile"),
            ssl_certfile=kwargs.get("ssl_certfile"),
        )
    else:
        uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="langchain-ChatGLM",
        description="About langchain-ChatGLM, local knowledge based ChatGLM with langchain"
        " ｜ 基于本地知识库的 ChatGLM 问答",
    )
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7861)
    parser.add_argument("--ssl_keyfile", type=str)
    parser.add_argument("--ssl_certfile", type=str)
    # 初始化消息
    args = parser.parse_args()
    args_dict = vars(args)
    run_api(
        host=args.host,
        port=args.port,
        ssl_keyfile=args.ssl_keyfile,
        ssl_certfile=args.ssl_certfile,
    )
