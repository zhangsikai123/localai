from contextlib import contextmanager
from functools import wraps

from server.db.base import SessionLocal


@contextmanager
def session_scope():
    """上下文管理器用于自动获取 Session, 避免错误"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:  # noqa
        session.rollback()
        raise
    finally:
        session.close()


def with_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            try:
                if "session" in kwargs:
                    session = kwargs.pop("session")
                result = f(session, *args, **kwargs)
                session.commit()
                return result
            except:  # noqa
                session.rollback()
                raise

    return wrapper


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db0() -> SessionLocal:
    db = SessionLocal()
    return db
