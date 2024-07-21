import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from configs import VERSION
from configs.server_config import OPEN_CROSS_DOMAIN
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from server.chat import (
    chat,
)

from server.utils import (
    BaseResponse,
    FastAPI,
    MakeFastAPIOffline,
)
from server.thread.thread import router as thread_router
from server.user.user import router as user_router


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

    return app


app = create_app()
