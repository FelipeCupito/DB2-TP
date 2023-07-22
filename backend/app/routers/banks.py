from fastapi import APIRouter
from backend.app.crud import banks_dao

from backend.app.models import Bank

router = APIRouter()


@router.post("/bank", response_model=Bank)
def create_bank(name: str, port: str):
    return banks_dao.create(name, port)
