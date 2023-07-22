import uvicorn
from fastapi import FastAPI
from backend.app.routers import banks, transactions, users

app = FastAPI()

# crea la base de datos
# models.Base.metadata.create_all(bind=engine)


app.include_router(banks.router, prefix='/banks', tags=["banks"])
app.include_router(transactions.router, prefix='/transactions', tags=["transactions"])
app.include_router(users.router, prefix='/users', tags=["users"])

if __name__ == "__main__":
    # uvicorn.run(app, host=settings.host, port=settings.port)
    uvicorn.run(app)
