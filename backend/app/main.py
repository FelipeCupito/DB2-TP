import uvicorn
from fastapi import FastAPI

from backend.app.database import create_db
from backend.app.routers import transactions, users

app = FastAPI()

app.include_router(transactions.router, prefix='/transactions', tags=["transactions"])
app.include_router(users.router, prefix='/users', tags=["users"])

if __name__ == "__main__":
    # uvicorn.run(app, host=settings.host, port=settings.port)
    create_db()
    uvicorn.run(app)
