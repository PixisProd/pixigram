from pydantic import BaseModel, Field, EmailStr


class RegisterUser(BaseModel):
    login: str = Field(min_length=3, max_length=12, examples=["pixie26"])
    password: str = Field(min_length=5, max_length=30, examples=["Trixie123"])
    username: str = Field(min_length=3, max_length=15, examples=["pixiS"])
    email: EmailStr = Field(max_length=40, examples=["trix@pixis.com"]) 