from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm  
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.database.models import users

from app.main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from app.schemas.Users_eschema import UserSchemaCreate, UserResponseEschema, UserEschemaLogin

from app.core.dependencies import create_session, verify_token


auth_route = APIRouter(prefix="/auth", tags=["auth"])


def create_token(dados, tempo_expiracao = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)):

    expiracao = datetime.now(timezone.utc) + tempo_expiracao

    if tempo_expiracao.total_seconds() <= 0:
        raise ValueError("tempo invalido")

    dados_token = {
        "sub": str(dados),
        "exp": expiracao
    }

    token = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
    
    return token


def authenticate_user (email, senha, session: Session):
    
    usuario = session.query(users).filter(users.email == email).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha invalidos")
    
    elif not bcrypt_context.verify(senha, usuario.senha):
        raise HTTPException(status_code=400, detail="Email ou senha invalidos")
    
    return usuario  


@auth_route.post("/create_user")
async def create_user(usuario: UserSchemaCreate, session: Session = Depends(create_session)):

    novo_existente = session.query(users).filter(users.email == usuario.email).first()

    if novo_existente:
        raise HTTPException(status_code=400, detail="Usuario ja existente")
    else:
        
        senha_criptografada = bcrypt_context.hash(usuario.senha)
        novo_usuario = users(nome=usuario.nome, email=usuario.email, senha=senha_criptografada)

        try:
            session.add(novo_usuario)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise HTTPException(status_code=500, detail=("Erro ao criar usuario"))
        
        return {"mensagem": "Usuario cadrastrado com sucesso"}
    

@auth_route.get("/get_user/{usuario_id}")
async def get_user(usuario_id: int, session: Session = Depends(create_session)):

    pergar_usuario = session.query(users).filter(users.id == usuario_id).first()

    if not pergar_usuario:
        raise HTTPException(status_code=400, detail="Usuario inexistente")
    
    else:
        return pergar_usuario

 
@auth_route.get("/list_user", response_model=list[UserResponseEschema])
async def list_user(session = Depends(create_session)):
    
    user_list = session.query(users).all()

    return user_list


@auth_route.post("/login")
async def login (dados: UserEschemaLogin, session: Session = Depends(create_session)):

    usuario = authenticate_user(dados.email, dados.senha, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario inexistente")
    
    access_token = create_token(usuario.id)
    refresh_token = create_token(usuario.id, tempo_expiracao = timedelta(days=7))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "type_token": "bearer"
    }


@auth_route.post("/login-form")
async def login_form (dados_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(create_session)):

    usuario = authenticate_user(dados_form.username, dados_form.password, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario inexistente")
    
    access_token = create_token(usuario.id)

    return {
        "access_token": access_token,
        "type_token": "bearer"
    }


@auth_route.get("/refresh")
async def use_refresh_token(usuario: users = Depends(verify_token)):

    access_token = create_token(usuario.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }   