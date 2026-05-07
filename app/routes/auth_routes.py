from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from app.main import bcrypt_context

from app.database.models import users

from app.schemas.Users_eschema import UserSchema
from app.schemas.Users_eschema import UserResponseEschema
from app.core.dependencies import create_session

auth_route = APIRouter(prefix="/auth", tags=["auth"])

@auth_route.get("/")
async def home():
    """ 
    Acessa a rota rome do site
    """
    return {"mensagem": "Rota acessada com sucesso"}

@auth_route.post("/create_user")
async def create_user(usuario: UserSchema, session = Depends(create_session)):

    novo_existente = session.query(users).filter(users.email == usuario.email).first()

    if novo_existente:
        raise HTTPException(status_code=400, detail="Usuario ja existente")
    else:
        
        senha_criptografada = bcrypt_context.hash(usuario.senha)
        novo_usuario = users(nome=usuario.nome, email=usuario.email, senha=senha_criptografada)

        try:
            session.add(novo_usuario)
            session.commit()

        except SQLAlchemyError as e:
            session.rollback()
            print(e)
            raise HTTPException(status_code=500, detail=("Erro ao criar usuario"))
        
        return {"mensagem": "Usuario cadrastrado com sucesso"}
    

@auth_route.get("/get_user/{usuario_id}")
async def get_user(usuario_id: int, session = Depends(create_session)):

    pergar_usuario = session.query(users).filter(users.id == usuario_id).first()

    if not pergar_usuario:
        raise HTTPException(status_code=400, detail="Usuario inexistente")
    
    else:
        return pergar_usuario

 
@auth_route.get("/list_user", response_model=list[UserResponseEschema])
async def list_user(session = Depends(create_session)):
    
    user_list = session.query(users).all()

    return user_list
    