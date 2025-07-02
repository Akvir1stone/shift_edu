from sqlalchemy import create_engine, Table, String, Column, Integer, MetaData, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, MappedAsDataclass, DeclarativeBase, Mapped, mapped_column, relationship
from pydantic import BaseModel
from typing import List


engine = create_engine("sqlite:///database.db", echo=True)
metadata_obj = MetaData()
Session = sessionmaker(bind=engine)
session = Session()


User = Table(
    "User",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('username', String(24), unique=True, nullable=False),
    Column('password', String(256), nullable=False),
    Column('admin', Boolean(), nullable=False, default=False),
)


SalaryRecord = Table(
    "SalaryRecord",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('amount', Float, nullable=False),
    Column('user_id', Integer, ForeignKey('User.id'), nullable=False),
)


Tokens = Table(
    "Tokens",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('token', String(), unique=True, nullable=False),
    Column('expire', DateTime(), nullable=False),
)


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(24), unique=True)
    password: Mapped[str] = mapped_column(String(256))


# class AveragePower(BaseModel):
#     Active: float
#     Reactive: float
#
#
# class Array(BaseModel):
#     array: List[AveragePower]


metadata_obj.create_all(engine)


# class SalaryModel(BaseModel):
#     salary_data: int
#     user: UserModel
#     disabled: bool


metadata_obj.create_all(engine)


