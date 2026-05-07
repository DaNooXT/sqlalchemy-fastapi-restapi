from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

App = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from app.routes.auth_routes import auth_route
from app.routes.order_routes import order_route

App.include_router(auth_route)
App.include_router(order_route)

#uvicorn main:app --reload