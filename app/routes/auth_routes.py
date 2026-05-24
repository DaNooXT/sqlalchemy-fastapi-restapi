from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.database.models import users

from app.main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from app.schemas.Users_eschema import UserSchema
from app.schemas.Users_eschema import UserResponseEschema

from app.core.dependencies import create_session

auth_route = APIRouter(prefix="/auth", tags=["auth"])


def create_token(dados: dict, tempo_expiracao: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    dados_token = {
        "sub": dados.nome,
        "id": dados.id
    }

    expiracao = datetime.now(timezone.utc) + timedelta(minutes=tempo_expiracao)

    if tempo_expiracao <= 0 or tempo_expiracao > 100:
        raise ValueError("tempo invalido")

    dados_token.update({"exp": expiracao})

    token = jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


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
    