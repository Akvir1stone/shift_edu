import sqlalchemy
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from security import check_password, hash_password, check_token, sign_jwt, decode_jwt, token_response
from models import User, session


app = FastAPI()





class JWTBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        valid_token: bool = False
        try:
            print('success')
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            valid_token = True

        return valid_token


@app.post('/')
async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = 'request to db for user by username' + form_data.username
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    hashed_password = 'request hashed_password of found user from db'
    if not check_password(hashed_password, hash_password(form_data.password)):
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    return {"access_token": 'got token somehow :P', "token_type": "bearer"}


# async def get_user(token: Annotated[str, Depends(None)]):
#     user = check_token(token)
#     if not user:
#         raise HTTPException()
#     return user
#
#
# async def get_active_user(current_user: Annotated[UserModel, Depends(get_user)]):
#     if current_user.disabled:
#         raise HTTPException()
#     return current_user


@app.get('/salaries')
async def get_salaries(dependencies=Depends(JWTBearer())):
    salaries = []
    return {'salaries': salaries}


@app.post('/signup')
async def sign_up(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    new_user = sqlalchemy.insert(User)
    user = session.query(User).filter(User.c.username == username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists")
    session.execute(new_user, {"username": username, "password": hash_password(password)})
    user = session.query(User).filter(User.c.username == username).first()
    session.commit()
    session.close()
    return sign_jwt(token_response(user.id))


@app.post('/signin')
async def sign_in(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = session.query(User).filter(User.c.username == username).first()
    session.close()
    if user:
        if check_password(user.password, hash_password(password)):
            return sign_jwt(token_response(user.id))
        else:
            return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="wrong username or password")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="wrong username or password")



