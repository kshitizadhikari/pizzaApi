from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from database import Session, engine
from models import User
from schemas import SignupModel, Token
from utils import get_current_user, authenticate_user, create_access_token, bcrypt_context, get_db

auth_router = APIRouter(
    prefix="/new_auth",
    tags=["Test Auth"]
)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@auth_router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@auth_router.post("/signup", response_model=SignupModel, status_code=status.HTTP_201_CREATED)
async def signup(db: db_dependency, user: SignupModel):
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with {user.email} already exists"
                            )
    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with {user.username} already exists"
                            )

    new_user = User(
        username=user.username,
        email=user.email,
        password=bcrypt_context.hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    db.add(new_user)
    db.commit()
    return new_user

# @auth_router.get("/protected_endpoint")
# async def protected_route(user: dict = Depends(get_current_user)):
#     return {"message": "Hello, secure world!", "user": user}


# @auth_router.get("/get-user")
# def get_user_data(token: Annotated[str, Depends(oauth2_bearer)]):
#     user = get_current_user(token)
#     return user
