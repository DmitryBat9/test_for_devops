import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel


SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-secret-change-before-production-47d7f42c5de249aa",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI(title="Users API with JWT")

password_hasher = PasswordHash.recommended()
bearer_scheme = HTTPBearer()


class User(BaseModel):
    id: int
    name: str
    email: str


class UserRegister(User):
    password: str


class StoredUser(User):
    password_hash: str


class LoginData(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


users: list[StoredUser] = []


def find_user_by_id(user_id: int):
    for user in users:
        if user.id == user_id:
            return user

    return None


def find_user_by_email(email: str):
    for user in users:
        if user.email == email:
            return user

    return None


def create_access_token(user_id: int):
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token_data = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    authentication_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить токен",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        token_data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        user_id = int(token_data.get("sub"))
    except (InvalidTokenError, TypeError, ValueError):
        raise authentication_error

    user = find_user_by_id(user_id)

    if user is None:
        raise authentication_error

    return user


@app.get("/")
def root():
    return {"message": "Users API with JWT работает"}


@app.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
def register(new_user: UserRegister):
    if find_user_by_id(new_user.id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким id уже существует",
        )

    if find_user_by_email(new_user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует",
        )

    stored_user = StoredUser(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        password_hash=password_hasher.hash(new_user.password),
    )

    users.append(stored_user)
    return stored_user


@app.post("/login", response_model=Token)
def login(login_data: LoginData):
    user = find_user_by_email(login_data.email)

    if user is None or not password_hasher.verify(
        login_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.id)

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@app.get("/profile", response_model=User)
def read_profile(current_user: StoredUser = Depends(get_current_user)):
    return current_user


@app.get("/users", response_model=list[User])
def read_users(current_user: StoredUser = Depends(get_current_user)):
    return users


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
