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
    quantidade: int
    preco: float
    estoque: int


    class config:
        from_atributes = True