from fastapi import FastAPI
from app.routers import transactions, users, banks

app = FastAPI()

app.include_router(banks.router, prefix='/banks', tags=["banks"])
app.include_router(transactions.router, prefix='/transactions', tags=["transactions"])
app.include_router(users.router, prefix='/users', tags=["users"])


