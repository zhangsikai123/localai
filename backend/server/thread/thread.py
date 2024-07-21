from typing import List

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from server.db.models.user_model import UserModel as User
from server.db.repository.thread_repository import add_messages_to_thread
from server.db.repository.thread_repository import create_thread
from server.db.repository.thread_repository import delete_thread
from server.db.repository.thread_repository import get_messages_by_thread
from server.db.repository.thread_repository import get_threads_by_user
from server.db.repository.thread_repository import name_thread_by_id
from server.user.auth import get_current_user
from server.utils import BaseResponse
from server.utils import ListMessagesResponse
from server.utils import ListThreadsResponse

router = APIRouter()


@router.post("/threads", response_model=BaseResponse)
async def create_thread_api(
    user: User = Depends(get_current_user),
) -> BaseResponse:
    thread = create_thread(user_id=user.id)
    return BaseResponse(
        code=200, msg=f"Thread created with ID: {thread.id}", data=thread.as_dict()
    )


@router.put("/threads/{thread_id}/name", response_model=BaseResponse)
async def name_thread_by_id_api(
    thread_id: int,
    name: str = Body(..., examples=["abc"]),
    user: User = Depends(get_current_user),
) -> BaseResponse:
    name_thread_by_id(thread_id=thread_id, new_name=name)
    return BaseResponse(code=200, msg=f"Thread with ID {thread_id} renamed to {name}")


@router.get("/threads", response_model=ListThreadsResponse)
async def get_threads_by_user_id_api(
    user: User = Depends(get_current_user),
):
    threads = get_threads_by_user(user_id=user.id)
    return ListThreadsResponse(data=[t.as_dict() for t in threads])


@router.get("/threads/messages/{thread_id}", response_model=ListMessagesResponse)
async def get_messages_by_thread_id_api(
    thread_id: int, user: User = Depends(get_current_user)
):
    messages = get_messages_by_thread(thread_id=thread_id)
    return ListMessagesResponse(data=[m.to_dict() for m in messages])


@router.post("/threads/messages/{thread_id}", response_model=BaseResponse)
async def add_messages_to_thread_api(
    thread_id: int,
    messages: List[dict],
    user: User = Depends(get_current_user),
) -> BaseResponse:
    add_messages_to_thread(thread_id=thread_id, messages=messages)
    return BaseResponse(code=200, msg=f"Messages added to Thread ID: {thread_id}")


@router.delete("/threads/{thread_id}", response_model=BaseResponse)
async def delete_thread_by_thread_id_api(
    thread_id: int, user: User = Depends(get_current_user)
):
    success = delete_thread(thread_id=thread_id)
    if success:
        return BaseResponse(
            code=200, msg=f"Thread with ID {thread_id} deleted successfully"
        )
    else:
        raise Exception("failed to delete thread")
