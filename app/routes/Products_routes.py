from fastapi import APIRouter, HTTPException, Depends
from app.core.dependencies import create_session

from app.database.models import products

from app.schemas.Product_eschema import ProductEschemaResponse
from app.schemas.Users_eschema import UserSchema

products_route = APIRouter(prefix="/products", tags=["products"])


@products_route.get("/list_products", response_model=list[ProductEschemaResponse])
async def list_products(session = Depends(create_session)):

    products_list = session.query(products).all()

    return products_list