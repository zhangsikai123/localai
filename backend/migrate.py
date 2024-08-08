from server.db.base import Base
from server.db.base import engine
from server.db.models import UserModel
from server.db.models import MessageModel
from server.db.models import ThreadModel

__all__ = ["UserModel", "MessageModel", "ThreadModel"]

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()
# add user admin
