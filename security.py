from sqlalchemy import create_engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import Dict
from dotenv import dotenv_values
import datetime
import jwt


# engine = create_engine("sqlite://sqlite.db")
secret_values = dotenv_values(".env")
salt = secret_values["SALT"]
jwt_secret = secret_values["SECRET"]
jwt_alg = secret_values["ALG"]


def token_response(token: str):
    return {
        "access_token": token
    }


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token, jwt_secret, algorithms=[jwt_alg])
    if datetime.datetime.strptime(decoded_token["expires"], '%Y:%m:%d:%H:%M') >= datetime.datetime.now():
        return decoded_token
    else:
        return {}


def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime('%Y:%m:%d:%H:%M')
    }
    # date = datetime.datetime.strptime('smt', '%Y:%m:%d:%H:%M')
    token = jwt.encode(payload, jwt_secret, algorithm=jwt_alg)

    return token_response(token)


def hash_password(password: str):
    return password


def check_token(token):
    return True


def check_password(password, realpw):
    return True


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str] = mapped_column(String(128))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



