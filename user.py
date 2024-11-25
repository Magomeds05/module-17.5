from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from user2 import User
from task2 import Task
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get("/user_id/tasks")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)],
                           user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    task = db.scalars(select(Task))
    if user is None:
        return user
    else:
        return task

@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)],
                     user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        return user
    raise HTTPException(status_code=404, detail="User was not found")

@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)],
                      user_create_model: CreateUser):
    db.execute(insert(User).values(username = user_create_model.username,
                                   firstname = user_create_model.firstname,
                                   lastname = user_create_model.lastname,
                                   age = user_create_model.age,
                                   slug = slugify(user_create_model.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)],
                      update_user: UpdateUser, user_id: int):
    users = db.scalars(select(User).where(User.id == user_id))
    for user in users:
        if user is None:
            db.execute(update(User).where(User.id == user_id).values(
                firstname=update_user.firstname,
                lastname=update_user.lastname,
                age=update_user.age))
            db.commit()
            return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

    raise HTTPException(status_code=404, detail="User was not found")


@router.delete("/delete")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalars(select(User).where(User.id == user_id))
    for user in users:
        if user is None:
            db.execute(update(User).where(User.id == user_id))
            db.commit()
            return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}

    raise HTTPException(status_code=404, detail="User was not found")

#Создайте новый маршрут get "/user_id/tasks" и функцию tasks_by_user_id. Логика этой функции должна заключатся в возврате всех Task конкретного User по id.
#Дополните функцию delete_user так, чтобы вместе с пользователем удалялись все записи связанные с ним.


