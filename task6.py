from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI(title="Users API")


class User(BaseModel):
    id: int
    name: str
    email: str


users: list[User] = []


def find_user_index(user_id: int) -> int:
    """Возвращает индекс пользователя или -1, если пользователь не найден."""

    for index, user in enumerate(users):
        if user.id == user_id:
            return index

    return -1


@app.post(
    "/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: User):
    if find_user_index(user.id) != -1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким id уже существует",
        )

    users.append(user)
    return user


@app.get("/users", response_model=list[User])
def read_users():
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    user_index = find_user_index(user_id)

    if user_index == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    return users[user_index]

@app.get("/")
def root():
    return {"message": "Users API работает"}  # Для проверки работы

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    user_index = find_user_index(user_id)

    if user_index == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    if updated_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="id в адресе и теле запроса должны совпадать",
        )

    users[user_index] = updated_user
    return updated_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user_index = find_user_index(user_id)

    if user_index == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    deleted_user = users.pop(user_index)

    return {
        "message": "Пользователь удалён",
        "user": deleted_user,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
