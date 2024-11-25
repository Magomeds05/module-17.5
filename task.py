from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from task2 import Task
from schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    task = db.scalars(select(Task)).all()
    return task


@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)],
                     task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))
    if task is None:
        return task
    raise HTTPException(status_code=404, detail="Task was not found")

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)],
                      create_task_model: CreateTask, task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))
    for i in task:
        if i is None:
            db.execute(insert(Task).values(username = create_task_model.username,
                                           firstname = create_task_model.firstname,
                                           lastname = create_task_model.lastname,
                                           age = create_task_model.age,
                                           slug = slugify(create_task_model.username)))
            db.commit()
            return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

    raise HTTPException(status_code=404, detail="User was not found")



@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)],
                      update_task_model: UpdateTask, task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))
    for i in task:
        if i is None:
            db.execute(update(Task).where(Task.id == task_id).values(
                firstname=update_task_model.firstname,
                lastname=update_task_model.lastname,
                age=update_task_model.age))
            db.commit()
            return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}

    raise HTTPException(status_code=404, detail="Tasl was not found")

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    tasks = db.scalars(select(Task).where(Task.id == task_id))
    for task in tasks:
        if task is None:
            db.execute(update(Task).where(Task.id == task_id))
            db.commit()
            return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}

    raise HTTPException(status_code=404, detail="User was not found")


