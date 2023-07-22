from fastapi import FastAPI

from backend.app.config import settings
from backend.app.routers import banks, transactions, users
import uvicorn

app = FastAPI()

app.include_router(banks.router, prefix='/banks', tags=["banks"])
app.include_router(transactions.router, prefix='/transactions', tags=["transactions"])
app.include_router(users.router, prefix='/users', tags=["users"])

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
