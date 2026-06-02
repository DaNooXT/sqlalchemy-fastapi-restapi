from fastapi import Depends, HTTPException
from app.main import SECRET_KEY, ALGORITHM, oauth2_schema
from sqlalchemy.orm import sessionmaker, Session
from app.database.models import db
from app.database.models import users
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError


def create_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally: 
        session.close()


def verify_token (token: str = Depends(oauth2_schema), session: Session = Depends(create_session)):

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = decoded_token.get("sub")
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso nagado")
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    
    if decoded_token.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if not usuario_id: 
        raise HTTPException(status_code=401, detail="Usuario inexistente")
    
    usuario = session.query(users).filter(users.id == int(usuario_id)).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Acesso nageado")
    
    return usuario