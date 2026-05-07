from pydantic import BaseModel
from datetime import date 
from decimal import Decimal
from typing import List

class OrdersEschemas (BaseModel):
    id: int
    user_id: int
    data_pedidos: date
    status: str
    total: Decimal
    
    class config:
        from_atributes = True


class OrderItensEschema (BaseModel):
    product_id: int
    quantidade:int

    class config:
        from_atributes = True


class OrderCreateEschema (BaseModel):
    user_id: int
    itens: List[OrderItensEschema]

    class config:
        from_atributes = True