from fastapi import APIRouter, HTTPException, Depends
from app.core.dependencies import create_session

from app.database.models import orders
from app.database.models import products
from app.database.models import order_itens

from app.schemas.Orders_eschema import OrderCreateEschema
from app.schemas.Orders_eschema import OrdersEschemas

order_route = APIRouter(prefix="/order", tags=["order"])

@order_route.post("/create_order", response_model=OrdersEschemas)
async def create_order(pedido: OrderCreateEschema, session = Depends(create_session)):

    total = 0
    produtos_cache = {}

    try:
        for item in pedido.itens:

            item_existente = session.query(products).filter(products.id == item.product_id).first()

            if not item_existente:
                raise HTTPException(status_code=400, detail="Produdto nao existe")

            if  item.quantidade > item_existente.estoque:
                raise HTTPException(status_code=400, detail="Estoque insuficiente")
            
            if item.quantidade <= 0:
                raise HTTPException(status_code=400, detail="Quantidade invalida")

            produtos_cache[item.product_id] = item_existente

        novo_pedido = orders(user_id=pedido.user_id, status="PENDENTE")

        session.add(novo_pedido)
        session.flush()
            
        for item in pedido.itens:

            item_existente = produtos_cache[item.product_id]

            subtotal = item.quantidade * item_existente.preco
            total += subtotal

            item_existente.estoque -= item.quantidade

            novo_item = order_itens(order_id=novo_pedido.id, product_id=item_existente.id, quantidade=item.quantidade, preco_unitario=item_existente.preco)

            session.add(novo_item)

        novo_pedido.total = total   

        session.commit()
        session.refresh(novo_pedido)

        return novo_pedido 

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erro Interno")
    

@order_route.get("/get_order/{order_id}", response_model=OrdersEschemas)
async def get_order(order_id: int, session = Depends(create_session)):

    id_order = session.query(orders).filter(orders.id == order_id).first()

    if not id_order:
        raise HTTPException(status_code=400, detail=("Pedido Inexistente"))
    
    else:
        return id_order


@order_route.get("/list_order", response_model=list[OrdersEschemas])
async def list_order(session = Depends(create_session)):

    order_list = session.query(orders).all()

    return order_list