from datetime import datetime

from server.db.models.user_model import MessageModel
from server.db.models.user_model import ThreadModel
from server.db.session import with_session
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session


@with_session
def create_thread_with_message(session: Session, user_id: int) -> ThreadModel:
    thread = create_thread(user_id=user_id)
    return thread


@with_session
def create_thread(session: Session, user_id: int) -> ThreadModel:
    thread = ThreadModel(user_id=user_id)
    thread.messages = []
    session.add(thread)
    return thread


@with_session
def name_thread_by_id(session: Session, thread_id: int, new_name: str) -> ThreadModel:
    thread = session.query(ThreadModel).filter(ThreadModel.id == thread_id).first()
    if thread:
        thread.name = new_name
    return thread


@with_session
def get_thread_by_id(session: Session, thread_id: int) -> ThreadModel:
    return session.query(ThreadModel).filter(ThreadModel.id == thread_id).first()


@with_session
def get_threads_by_user(session: Session, user_id: int) -> list[ThreadModel]:
    return (
        session.query(ThreadModel)
        .options(joinedload(ThreadModel.messages))
        .filter(ThreadModel.user_id == user_id)
        .order_by(ThreadModel.created_at.desc())
        .all()
    )


@with_session
def create_message(
    session: Session, thread_id: int, content: str, sender: str
) -> MessageModel:
    message = MessageModel(thread_id=thread_id, content=content, sender=sender)
    session.add(message)
    return message


@with_session
def add_messages_to_thread(
    session: Session, thread_id: int, messages: list[dict]
) -> ThreadModel:
    messages = [MessageModel(thread_id=thread_id, **m) for m in messages]
    session.add_all(messages)
    return messages


@with_session
def get_messages_by_thread(session: Session, thread_id: int) -> list[MessageModel]:
    return session.query(MessageModel).filter(MessageModel.thread_id == thread_id).all()


@with_session
def update_thread(session: Session, thread_id: int) -> ThreadModel:
    thread = session.query(ThreadModel).filter(ThreadModel.id == thread_id).first()
    if thread:
        thread.updated_at = datetime.now()
    return thread


@with_session
def update_message(session: Session, message_id: int, content: str) -> MessageModel:
    message = session.query(MessageModel).filter(MessageModel.id == message_id).first()
    if message:
        message.content = content
    return message


@with_session
def delete_thread(session: Session, thread_id: int) -> bool:
    thread = session.query(ThreadModel).filter(ThreadModel.id == thread_id).first()
    if thread:
        session.delete(thread)
        return True
    return False


@with_session
def delete_message(session: Session, message_id: int) -> bool:
    message = session.query(MessageModel).filter(MessageModel.id == message_id).first()
    if message:
        session.delete(message)
        return True
    return False
