from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.grtenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

App = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from app.routes.auth_routes import auth_route
from app.routes.order_routes import order_route
from app.routes.Products_routes import products_route

App.include_router(auth_route)
App.include_router(order_route)
App.include_router(products_route)

#uvicorn main:app --reload