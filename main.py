from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("secret_key")
algoritimo = os.getenv("algoritimo")
expiracao_token =int(os.getenv("expiracao_token"))

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routes import auth_router
from ord_routes import ord_router

app.include_router(auth_router)
app.include_router(ord_router)
