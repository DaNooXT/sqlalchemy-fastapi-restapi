from pydantic import BaseModel

class ProductEschema (BaseModel):
    id: int
    quantidade: int

    class config:
        from_atributes = True


class ProductEschemaResponse (BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    estoque: int

    class config:
        from_atributes = True


class ProductEschemaUpdate (BaseModel):
    nome: str
    descricao: str
    preco: float
    estoque: int

    class config:
        from_atributes = True