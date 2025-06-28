from sqlalchemy import create_engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String


engine = create_engine("sqlite://sqlite.db")


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

