from fastapi import FastAPI
from app.database import create_db
from app.routers import transactions, users

app = FastAPI()

app.include_router(transactions.router, prefix='/transactions', tags=["transactions"])
app.include_router(users.router, prefix='/users', tags=["users"])

create_db()


