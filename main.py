from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from security import check_password, hash_password, check_token
from models import UserModel


app = FastAPI
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post('/')
async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = 'request to db for user by username' + form_data.username
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    hashed_password = 'request hashed_password of found user from db'
    if not check_password(hashed_password, hash_password(form_data.password)):
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    return {"access_token": 'got token somehow :P', "token_type": "bearer"}


async def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = check_token(token)
    if not user:
        raise HTTPException()
    return user


async def get_active_user(current_user: Annotated[UserModel, Depends(get_user)]):
    if current_user.disabled:
        raise HTTPException()
    return current_user


@app.get('/salaries')
async def get_salaries(request: Request, current_user: Annotated[UserModel, Depends(get_active_user)]):
    salaries = []
    return templates.TemplateResponse(request, context={'salaries': salaries}, name='salaries.html')

