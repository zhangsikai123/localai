import hashlib

from server.db.models.user_model import UserModel
from server.db.session import with_session
from server.exceptions import NotFoundException


def encode_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def generate_activate_code(seed):
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


@with_session
def activate_user(session, activate_code: str = ""):
    u = session.query(UserModel).filter_by(activate_code=activate_code).first()
    if u:
        if u.active is True:
            raise Exception("user already activated")
        else:
            u.active = True
            session.commit()
    else:
        raise NotFoundException("user not found")


@with_session
def find_user_by_password_and_email(
    session, email: str = "", password: str = ""
) -> UserModel:
    password = encode_password(password)
    usr = session.query(UserModel).filter_by(email=email, password=password).first()
    return usr


@with_session
def email_exists(session, email: str = "") -> bool:
    usr = session.query(UserModel).filter_by(email=email).first()
    return usr is not None


@with_session
def create_user(
    session,
    nickname: str,
    avatar: str = "",
    email: str = "",
    password: str = "",
    token: str = "",
) -> UserModel:
    password = encode_password(password)
    activate_code = generate_activate_code(token)
    usr = UserModel(
        nickname=nickname,
        email=email,
        token=token,
        avatar=avatar,
        password=password,
        active=False,
        activate_code=activate_code,
    )
    session.add(usr)
    return usr


@with_session
def get_user_by_id(session, uid: int) -> UserModel:
    return session.query(UserModel).filter_by(id=uid).first()


@with_session
def get_user_by_token(session, token: int) -> UserModel:
    return session.query(UserModel).filter_by(token=token).first()


@with_session
def get_current_user_count(session):
    return session.query(UserModel).count()


@with_session
def update_user_token_by_id(session, uid: int, token: str):
    u = session.query(UserModel).filter_by(id=uid).first()
    if u:
        u.token = token
