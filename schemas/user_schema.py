from pydantic import BaseModel, field_validator


class UserSchema(BaseModel):
    username: str
    password: str

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError('Password too short')
        return password
