from datetime import timedelta, datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from database import Session, engine
from models import User


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='new_auth/login')

SECRET_KEY = 'dd7381b6385a4308695f416342732bf8aee495e8c96f5294b3b38454132094aa'
ALGORITHM = 'HS256'


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {
        'sub': username,
        'id': user_id,
    }
    expires = datetime.utcnow() + expires_delta
    encode.update(
        {
            'exp': expires
        }
    )
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')  # Corrected key name
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {
            "username": username,
            "user_id": user_id
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate JWT token")