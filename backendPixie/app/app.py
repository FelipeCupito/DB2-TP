from fastapi import FastAPI

from app.config import settings
from app.routers import banks, transactions, users
import uvicorn

app = FastAPI()

app.include_router(banks.router, prefix='/banks', tags=["banks"])
app.include_router(transactions.router, prefix='/transactions', tags=["transactions"])
app.include_router(users.router, prefix='/users', tags=["users"])


