from fastapi import APIRouter, HTTPException, Depends
from app.core.dependencies import create_session

from app.database.models import products

from app.schemas.Product_eschema import ProductEschemaResponse
from app.schemas.Product_eschema import ProductEschemaUpdate

products_route = APIRouter(prefix="/products", tags=["products"])


@products_route.get("/list_products", response_model=list[ProductEschemaResponse])
async def list_products(session = Depends(create_session)):

    products_list = session.query(products).all()

    return products_list


@products_route.post("/edit_product/{product_id}", response_model=ProductEschemaResponse)
async def edit_product(product_id: int, product: ProductEschemaUpdate, session = Depends(create_session)):

    produto = session.query(products).filter(products.id == product_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    
    dados = product.model_dump()

    for chave, valor in dados.items():
        setattr(produto, chave, valor)

    session.commit()
    session.refresh(produto)

    return produto