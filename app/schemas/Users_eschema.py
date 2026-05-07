from pydantic import BaseModel
from datetime import date

class UserSchema(BaseModel):
    id: int
    nome: str
    email: str
    senha: str
    data_criacao: date  

    class config:
        from_atributes = True


class UserResponseEschema (BaseModel):
    id: int
    nome: str
    email: str

    class config:
        from_atributes = True