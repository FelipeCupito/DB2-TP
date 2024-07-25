from fastapi import FastAPI, Request
from app.routers import transactions, users, banks
import logging

app = FastAPI()

app.include_router(banks.router, prefix='/banks', tags=["banks"])
app.include_router(transactions.router, prefix='/transactions', tags=["transactions"])
app.include_router(users.router, prefix='/users', tags=["users"])


# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logging.info(f"Request URL: {request.url}")
#     logging.info(f"Request Method: {request.method}")
#     logging.info(f"Request Headers: {request.headers}")
#     if request.method in ("POST", "PUT"):
#         logging.info(f"Request Body: {await request.body()}")
#     response = await call_next(request)
#     logging.info(f"Response Status: {response.status_code}")
#     return response