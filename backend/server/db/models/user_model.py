from server.db.base import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship


class UserModel(Base):
    """
    用户表
    """

    __tablename__ = "auth_user_new"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户 ID")
    active = Column(Boolean, comment="是否激活")
    nickname = Column(String(256), comment="nickname")
    email = Column(String(256), comment="email")
    activate_code = Column(String(64), comment="activate_code")
    password = Column(String(256), comment="password")
    token = Column(String(256), unique=True, comment="token")
    avatar = Column(String(256), unique=False, comment="avatar")
    threads = relationship(
        "ThreadModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), comment="修改时间")

    def __repr__(self):
        return f"<UserModel(id='{self.id}', nickname='{self.nickname}',email='{self.email}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email,
            "token": self.token,
            "avatar": self.avatar,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class ThreadModel(Base):
    """
    Chat Thread Table
    """

    __tablename__ = "chat_thread"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Thread ID")
    user_id = Column(
        Integer, ForeignKey("auth_user_new.id"), nullable=False, comment="User ID"
    )
    user = relationship("UserModel", back_populates="threads")
    messages = relationship(
        "MessageModel", back_populates="thread", cascade="all, delete-orphan"
    )
    name = Column(String(256), comment="Thread Name", default="")
    created_at = Column(DateTime, default=func.now(), comment="Created Time")
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="Updated Time"
    )

    def as_dict(self):
        last_message = self.messages[-1].content if len(self.messages) > 0 else None
        return {
            "id": self.id,
            "user_id": self.user_id,
            "last_message": last_message,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "name": self.name,
        }


class MessageModel(Base):
    """
    Message Table
    """

    __tablename__ = "message"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Message ID")
    thread_id = Column(
        Integer, ForeignKey("chat_thread.id"), nullable=False, comment="Thread ID"
    )
    thread = relationship("ThreadModel", back_populates="messages")
    content = Column(Text, comment="Message Content")
    sender = Column(String(50), comment="Sender (user or ai)")
    created_at = Column(DateTime, default=func.now(), comment="Created Time")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
