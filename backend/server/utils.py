import asyncio
import os

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any
from typing import Awaitable
from typing import List
from typing import Optional

import pydantic

from configs import log_verbose
from configs import logger
from fastapi import FastAPI
from pydantic import BaseModel


async def wrap_done(fn: Awaitable, event: asyncio.Event):
    """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
    try:
        await fn
    except Exception as e:
        # TODO: handle exception
        import traceback

        traceback.print_exc()
        msg = f"Caught exception: {e}"
        logger.error(
            f"{e.__class__.__name__}: {msg}", exc_info=e if log_verbose else None
        )
    finally:
        # Signal the aiter to stop.
        event.set()


class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="API status code")
    msg: str = pydantic.Field("success", description="API status message")
    data: Any = pydantic.Field(None, description="API data")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
            }
        }


class ThreadResponse(BaseModel):
    id: int
    user_id: int
    created_at: str
    updated_at: str


class MessageResponse(BaseModel):
    id: int
    thread_id: int
    content: str
    sender: str
    created_at: str
    updated_at: str


class ListMessagesResponse(BaseResponse):
    data: List[dict] = []

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": [
                    {
                        "id": 1,
                        "thread_id": 123,
                        "content": "Who are you bro？",
                        "sender": "User",
                        "created_at": "2023-01-01T12:00:00",
                        "updated_at": "2023-01-02T15:30:00",
                    },
                    # Add more message examples as needed
                ],
            }
        }


class ListThreadsResponse(BaseResponse):
    data: List[dict] = []

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": [
                    {
                        "id": 1,
                        "user_id": 123,
                        "created_at": "2023-01-01T12:00:00",
                        "updated_at": "2023-01-02T15:30:00",
                    },
                    # Add more thread examples as needed
                ],
            }
        }


class ListResponse(BaseResponse):
    data: List[str] = pydantic.Field(..., description="List of names")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": ["doc1.docx", "doc2.pdf", "doc3.txt"],
            }
        }


class ChatMessage(BaseModel):
    question: str = pydantic.Field(..., description="Question text")
    response: str = pydantic.Field(..., description="Response text")
    history: List[List[str]] = pydantic.Field(..., description="History text")
    source_documents: List[str] = pydantic.Field(
        ..., description="List of source documents and their scores"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Who are you bro？",
                "response": "Hi there",
                "history": [
                    [
                        "Who are you bro?",
                    ],
                ],
                "source_documents": ["hello"],
            }
        }


def MakeFastAPIOffline(
    app: FastAPI,
    static_dir=Path(__file__).parent / "static",
    static_url="/static-offline-docs",
    docs_url: Optional[str] = "/docs",
    redoc_url: Optional[str] = "/redoc",
) -> None:
    """patch the FastAPI obj that doesn't rely on CDN for the documentation page"""
    from fastapi import Request
    from fastapi.openapi.docs import (
        get_redoc_html,
        get_swagger_ui_html,
        get_swagger_ui_oauth2_redirect_html,
    )
    from fastapi.staticfiles import StaticFiles
    from starlette.responses import HTMLResponse

    openapi_url = app.openapi_url
    swagger_ui_oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url

    def remove_route(url: str) -> None:
        """
        remove original route from app
        """
        index = None
        for i, r in enumerate(app.routes):
            if r.path.lower() == url.lower():
                index = i
                break
        if isinstance(index, int):
            app.routes.pop(index)

    # Set up static file mount
    app.mount(
        static_url,
        StaticFiles(directory=Path(static_dir).as_posix()),
        name="static-offline-docs",
    )

    if docs_url is not None:
        remove_route(docs_url)
        remove_route(swagger_ui_oauth2_redirect_url)

        # Define the doc and redoc pages, pointing at the right files
        @app.get(docs_url, include_in_schema=False)
        async def custom_swagger_ui_html(request: Request) -> HTMLResponse:
            root = request.scope.get("root_path")
            favicon = f"{root}{static_url}/favicon.png"
            return get_swagger_ui_html(
                openapi_url=f"{root}{openapi_url}",
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
                swagger_js_url=f"{root}{static_url}/swagger-ui-bundle.js",
                swagger_css_url=f"{root}{static_url}/swagger-ui.css",
                swagger_favicon_url=favicon,
            )

        @app.get(swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect() -> HTMLResponse:
            return get_swagger_ui_oauth2_redirect_html()

    if redoc_url is not None:
        remove_route(redoc_url)

        @app.get(redoc_url, include_in_schema=False)
        async def redoc_html(request: Request) -> HTMLResponse:
            root = request.scope.get("root_path")
            favicon = f"{root}{static_url}/favicon.png"

            return get_redoc_html(
                openapi_url=f"{root}{openapi_url}",
                title=app.title + " - ReDoc",
                redoc_js_url=f"{root}{static_url}/redoc.standalone.js",
                with_google_fonts=False,
                redoc_favicon_url=favicon,
            )


def get_prompt_template(type: str, name: str) -> Optional[str]:
    """
    load template from prompt config
    """

    from configs import prompt_config
    import importlib

    importlib.reload(prompt_config)
    return prompt_config.PROMPT_TEMPLATES[type].get(name)
