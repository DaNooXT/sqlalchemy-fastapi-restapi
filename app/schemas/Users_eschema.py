from pydantic import BaseModel

class UserSchemaCreate(BaseModel):
    nome: str
    email: str
    senha: str

    class config:
        from_atributes = True

class UserResponseEschema (BaseModel):
    id: int
    nome: str
    email: str

    class config:
        from_atributes = True

class UserEschemaLogin (BaseModel):
    email: str
    senha: str

    class Config:
        from_atributer = True