from pydantic import BaseModel


class UserModel(BaseModel):
    # TODO validation for lengh
    username: str
    hashed_password: str


class SalaryModel(BaseModel):
    salary_data: int
    user: UserModel
    disabled: bool
