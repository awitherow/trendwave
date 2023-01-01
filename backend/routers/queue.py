
from fastapi import APIRouter
from pydantic import BaseModel
from ..workers import add

router = APIRouter()

# Use pydantic to keep track of the input request payload


class Numbers(BaseModel):
    x: float
    y: float


@router.post('/queue/add')
def enqueue_add(n: Numbers):
    # We use celery delay method in order to enqueue the task with the given parameters
    add.delay(n.x, n.y)
