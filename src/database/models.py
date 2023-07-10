from sqlalchemy import Column, Integer, String, Boolean, func, Table, ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Contact(Base):
    """
    This is the class that describes the user's contact 

    :param id: Unique contact ID.
    :type id: int
    :param name: Contact name.
    :type name: str
    :param surname: Contact surname.
    :type surname: str
    :param phone_number: Contact phone number.
    :type phone_number: str
    :param email: Contact email.
    :type email: str
    :param birthday: User's date of birth.
    :type birthday: Date
    :param user_id: ID of the user who owns this contact.
    :type user_id: int
    :param user: The user who owns the contact.
    :type user: User
    """
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname  = Column(String(50), nullable=False)
    phone_number = Column(String(12), nullable=False)
    email = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(Base):
    """
    This is the class that describes the user - the owner of the contacts

    :param id: Unique user ID.
    :type id: int
    :param username: Username.
    :type username: str
    :param email: User`s email.
    :type email: str
    :param password: User password to access the contact list.
    :type password: str
    :param created_at: User account creation time.
    :type created_at: DateTime
    :param birthday: User's date of birth.
    :type birthday: Date
    :param avatar: Variable with which the user's avatar will be created.
    :type avatar: str
    :param refresh_token: Unique token for access to the user account.
    :type refresh_token: str
    :param confirmed: Variable that checks if the user's mail is confirmed.
    :type confirmed: bool
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)