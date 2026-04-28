from sqlmodel import select, and_ # type: ignore
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status # type: ignore
from ...databases.sessions import SessionDep
from ...core.auth import AuthUser, get_current_user, require_view, require_create, require_delete, require_edit
from ...databases.models import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
def list_tasks(user: Annotated[AuthUser, Depends(require_view)], session: SessionDep):
    tasks = session.exec(select(Task).where(and_(Task.org_id == user.org_id))).scalars()
    return tasks


@router.post("", response_model=TaskResponse)
def create_task(
        task_data: TaskCreate,
        user: Annotated[AuthUser, Depends(require_create)],
        session: SessionDep,
):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        org_id=user.org_id,
        created_by=user.user_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
        task_id: str,
        user: Annotated[AuthUser, Depends(require_view)],
        session: SessionDep
):
    task = session.exec(
        select(Task).where(
            and_(
                Task.id == task_id,
                Task.org_id == user.org_id,
            )
        )
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
        task_id: str,
        task_data: TaskUpdate,
        user: Annotated[AuthUser, Depends(require_edit)],
        session: SessionDep
):
    task = session.exec(
        select(Task).where(
            and_(
                Task.id == task_id,
                Task.org_id == user.org_id,
            )
        )
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
        task_id: str,
        user: Annotated[AuthUser, Depends(require_delete)],
        session: SessionDep
):
    task = session.exec(
        select(Task).where(
            and_(
                Task.id == task_id,
                Task.org_id == user.org_id,
            )
        )
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()
    return None