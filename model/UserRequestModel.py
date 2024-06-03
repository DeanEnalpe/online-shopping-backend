from pydantic import BaseModel


class UserRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    login_id: str
    password: str
    confirm_password: str
    contact_number: str
