from pydantic import BaseModel, EmailStr, validator


class User(BaseModel):
    email: EmailStr
    password: str
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

