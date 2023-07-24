from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import transactions_dao
from ..database import get_db
from ..schemas import Response, Transaction

router = APIRouter()


@router.post("/pay", response_model=Response)
def pay(transaction: Transaction, db: Session = Depends(get_db)):
    try:
        balance = transactions_dao.pay(transaction.cbu, transaction.amount, db)
        if balance == -1:
            return send_error("Account not found")
        elif balance == -2:
            return send_error("Not enough balance")
        else:
            return send_data(balance)
    except HTTPException:
        return send_error("Error in bank")


@router.post("/charge", response_model=Response)
def charge(transaction: Transaction, db: Session = Depends(get_db)):
    try:
        balance = transactions_dao.charge(transaction.cbu, transaction.amount, db)
        if balance == -1:
            return send_error("Account not found")
        else:
            return send_data(balance)
    except HTTPException:
        return send_error("Error in bank")


def send_error(msg: str) -> Response:
    return Response(
        status_code=404,
        response_type="error",
        description=msg,
        data=None,
    )


def send_data(data: Any) -> Response:
    return Response(
        status_code=200,
        response_type="success",
        description="Operation successful",
        data=data
    )
