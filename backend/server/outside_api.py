import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from configs import VERSION, OPEN_CROSS_DOMAIN
from server.third_qa_support_api import qa_handler
from server.utils import (
    BaseResponse,
    FastAPI,
    MakeFastAPIOffline,
)


async def document():
    return RedirectResponse(url="/docs")


def create_app():
    app = FastAPI(title="Chatchat outside API Server", version=VERSION)
    MakeFastAPIOffline(app)

    if OPEN_CROSS_DOMAIN:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.get("/", response_model=BaseResponse, summary="swagger 文档")(document)

    app.post(
        "/v1/third-qa/work-tool",
        tags=["Server State"],
        summary="企微工具 qa 回调地址",
    )(qa_handler)
    return app
