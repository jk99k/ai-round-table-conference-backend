from ninja import Router
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth
from .schemas import UserRegisterIn, UserOut
from pydantic import BaseModel

router = Router(tags=["users"])

class LoginIn(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access: str
    refresh: str

class RefreshIn(BaseModel):
    refresh: str

@router.post("", response={201: UserOut, 400: dict})
def register(request, data: UserRegisterIn):
    try:
        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password
        )
        return 201, UserOut(id=user.id, username=user.username, email=user.email)
    except IntegrityError:
        return 400, {"error": "Username or email already exists."}

@router.get("/me", response=UserOut, auth=JWTAuth())
def get_me(request):
    user = request.user
    return UserOut(id=user.id, username=user.username, email=user.email)

@router.post("/login", response={200: TokenOut, 401: dict})
def login(request, data: LoginIn):
    user = authenticate(username=data.username, password=data.password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return 200, TokenOut(access=str(refresh.access_token), refresh=str(refresh))
    return 401, {"error": "Invalid credentials"}

@router.post("/refresh", response={200: TokenOut, 401: dict})
def refresh_token(request, data: RefreshIn):
    try:
        refresh = RefreshToken(data.refresh)
        access_token = str(refresh.access_token)
        return 200, TokenOut(access=access_token, refresh=str(refresh))
    except Exception:
        return 401, {"error": "Invalid refresh token"}
