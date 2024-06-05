from pydantic import BaseModel, EmailStr


class PasswordResetRequestModel(BaseModel):
    email: str
    login_id: str
    new_password: str
    confirm_password: str