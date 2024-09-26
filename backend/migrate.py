from server.db.base import Base
from server.db.base import engine
from server.db.models.user_model import MessageModel
from server.db.models.user_model import ThreadModel
from server.db.models.user_model import UserModel
from server.db.repository.user_repository import activate_user
from server.db.repository.user_repository import create_user
from server.db.repository.user_repository import get_user_by_token

__all__ = ["UserModel", "MessageModel", "ThreadModel"]


def create_tables():
    Base.metadata.create_all(bind=engine)


create_tables()
# add user admin
if not get_user_by_token("admin"):
    user = create_user(
        nickname="admin",
        token="admin",
        avatar="src/assets/user.png",
        password="admin",
        email="admin",
    )
    activate_user(user.activate_code)
