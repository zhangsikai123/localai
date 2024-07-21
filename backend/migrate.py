from server.db.base import Base
from server.db.base import engine


def create_tables():
    Base.metadata.create_all(bind=engine)


create_tables()
# add user admin
