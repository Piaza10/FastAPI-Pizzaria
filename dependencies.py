from main import secret_key, algoritimo, Oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
        
def verificar_token(token: str = Depends(Oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        informacoes = jwt.decode(token, secret_key, algoritimo)
        id_usuario = int(informacoes.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="acesso negado! (VERIFIQUE A VALIDADE DO TOKEN.)")
    
    #verifica se o token é válido e extrai o id do usuario no token
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="acesso inválido")
    return usuario
