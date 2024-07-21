from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from server.db.models.user_model import UserModel as User
from server.db.repository.user_repository import activate_user
from server.db.repository.user_repository import create_user
from server.db.repository.user_repository import email_exists
from server.db.repository.user_repository import find_user_by_password_and_email
from server.exceptions import NotFoundException
from server.user.auth import get_current_user
from server.utils import BaseResponse

# from server.directmail import MailSender
router = APIRouter()


@router.get("/bot")
async def bot():
    return {"message": "Hello, I am a bot"}


@router.get("/activate")
async def activate(activate_code: str) -> BaseResponse:
    try:
        activate_user(activate_code)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f"激活失败，用户不存在")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"激活失败，{e}")
    return BaseResponse(code=200, msg=f"激活成功")


@router.post("/signup")
async def signup(
    password: str = Body(..., examples=["password"]),
    email: str = Body(..., examples=["xxx@xxx.com"]),
) -> BaseResponse:
    token = uuid4().hex
    random_nickname = f"User{uuid4().hex[:6]}"
    # default baozi user img
    avatar = "src/assets/user.png"
    # check if email exists
    if email_exists(email):
        raise HTTPException(status_code=400, detail=f"邮箱{email}已经存在了")
    user = create_user(
        nickname=random_nickname,
        token=token,
        avatar=avatar,
        password=password,
        email=email,
    )
    activate_user(user.activate_code)
    # MailSender.send_activation_mail(email, user.activate_code)
    return BaseResponse(
        code=200,
        msg=f"注册成功，请前往邮箱{email}激活账号",
        data={"activate_code": user.activate_code},
    )


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    def gen_token_and_create_user():
        email = form_data.username
        password = form_data.password
        user = find_user_by_password_and_email(email, password)
        if not user:
            # login failed
            raise HTTPException(
                status_code=401,
                detail="login failed, please check your auth information",
            )
        elif not user.active:
            # login failed
            raise HTTPException(
                status_code=401,
                detail="login failed, user inactive, please check your mail inbox and click the activation link",
            )
        else:
            return user.token

    return {"access_token": gen_token_and_create_user(), "token_type": "bearer"}


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return current_user
