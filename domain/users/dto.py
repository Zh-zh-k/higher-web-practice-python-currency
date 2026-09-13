from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUserDTO(BaseModel):
    email: EmailStr
    password: str


class UpdateUserDTO(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
