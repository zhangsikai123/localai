import pytest

from server.db.base import Base
from server.db.repository.thread_repository import create_message
from server.db.repository.thread_repository import create_thread
from server.db.repository.thread_repository import delete_message
from server.db.repository.thread_repository import delete_thread
from server.db.repository.thread_repository import get_messages_by_thread
from server.db.repository.thread_repository import get_thread_by_id
from server.db.repository.thread_repository import get_threads_by_user
from server.db.repository.thread_repository import update_message
from server.db.repository.thread_repository import update_thread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use an SQLite in-memory database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
# Create an engine and bind it to the Base)
Base.metadata.create_all(bind=engine)

# Create a sessionmaker with the in-memory database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture to create a session for each test
@pytest.fixture
def session():
    # Create a new session for each test
    db = SessionLocal()
    # Apply migrations or seed data if needed
    yield db
    # Clean up the session after the test
    db.close()


# Test create_thread and get_thread_by_id
def test_create_and_get_thread(session):
    user_id = 1
    thread = create_thread(session=session, user_id=user_id)
    assert thread.id is not None

    # Test get_thread_by_id
    retrieved_thread = get_thread_by_id(thread.id, session=session)
    assert retrieved_thread.id == thread.id
    assert retrieved_thread.user_id == user_id
    delete_thread(thread_id=thread.id, session=session)


# Test get_threads_by_user
def test_get_threads_by_user(session):
    user_id = 1
    # Create threads for the user
    create_thread(session=session, user_id=user_id)
    create_thread(session=session, user_id=user_id)

    # Test get_threads_by_user
    threads = get_threads_by_user(session=session, user_id=user_id)
    assert len(threads) == 2


# Test create_message and get_messages_by_thread
def test_create_and_get_messages(session):
    user_id = 1
    thread = create_thread(user_id=user_id, session=session)

    # Create messages for the thread
    create_message(
        thread_id=thread.id, content="Message 1", sender="User", session=session
    )
    create_message(
        thread_id=thread.id, content="Message 2", sender="AI", session=session
    )

    # Test get_messages_by_thread
    messages = get_messages_by_thread(thread_id=thread.id, session=session)
    assert len(messages) == 2


# Test update_thread
def test_update_thread(session):
    user_id = 1
    thread = create_thread(user_id=user_id, session=session)
    updated_at = thread.updated_at
    # Test update_thread
    updated_thread = update_thread(thread_id=thread.id, session=session)
    assert updated_thread.updated_at > updated_at


# Test update_message
def test_update_message(session):
    user_id = 1
    thread = create_thread(user_id=user_id, session=session)
    message = create_message(
        thread_id=thread.id, content="Original Content", sender="User", session=session
    )

    # Test update_message
    updated_message = update_message(
        message_id=message.id, content="Updated Content", session=session
    )
    assert updated_message.content == "Updated Content"


# Test delete_thread and delete_message
def test_delete_thread_and_message(session):
    user_id = 1
    thread = create_thread(user_id=user_id, session=session)
    message = create_message(
        thread_id=thread.id, content="To be deleted", sender="User", session=session
    )

    # Test delete_thread
    assert delete_thread(thread_id=thread.id, session=session)

    # Test delete_message
    assert not delete_message(message_id=message.id, session=session)


# Add more tests as needed based on your specific requirements
