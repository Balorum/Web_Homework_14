from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ContactBase(BaseModel):
    """
    This is the class that describes the required contact fields.

    :param name: Contact name.
    :type name: str
    :param surname: Contact surname.
    :type surname: str
    :param phone_number: Contact phone number.
    :type phone_number: str
    """
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    phone_number: str = Field(max_length=12)

class ContactModel(ContactBase):
    """
    This is the class that describes the optional contact fields.

    :param email: Contact email.
    :type email: str
    :param birthday: Contact birthday date.
    :type birthday: date
    """
    email: str = Field(max_length=50)
    birthday: date = Field()

class ContactResponse(ContactBase):
    """
    Contact model when returning a result.

    :param id: Contact id.
    :type id: int
    :param email: Contact email.
    :type email: str
    :param birthday: Contact birthday date.
    :type birthday: date
    """
    id: int
    email: str
    birthday: date

    class Config:
            orm_mode = True

class UserModel(BaseModel):
    """
    User display model in API.

    :param username: Username.
    :type username: str
    :param email: User email.
    :type email: str
    :param password: User password.
    :type password: str
    """
    username: str = Field(min_length=5, max_length=20)
    email: str
    password: str = Field(min_length=6, max_length=20)


class UserDb(BaseModel):
    """
    User mapping model in the database.

    :param id: User id.
    :type id: int
    :param username: Username.
    :type username: str
    :param email: User email.
    :type email: str
    :param created_at: Exact date of account registration.
    :type created_at: datetime
    :param avatar: Field for creating a user avatar.
    :type avatar: str
    """
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    """
    User model when returning a result.

    :param user: User model.
    :type user: UserDb
    :param detail: Detail about operation.
    :type detail: str
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Token Model.

    :param access_token: Access token.
    :type access_token: str
    :param refresh_token: Refresh token.
    :type refresh_token: str
    :param token_type: Token type.
    :type token_type: str
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"