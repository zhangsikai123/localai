from server.db.base import Base
from server.db.base import engine
from server.db.models.user_model import UserModel
from server.db.models.user_model import ThreadModel
from server.db.models.user_model import MessageModel

def create_tables():
    Base.metadata.create_all(bind=engine)


create_tables()
# add user admin
