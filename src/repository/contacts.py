from typing import List
from sqlalchemy import and_
from datetime import date, datetime
from sqlalchemy.orm import Session
import sys

sys.path.append("..")

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, user: User, limit: int, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_days_to_birthday(skip: int, user: User, limit: int, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts, whose birthday is this week, for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    birthday_days = []
    nowdays_date = datetime.now().date()
    days = db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()
    for i in days:
        birtday_year = date(year=i.birthday.year+(nowdays_date.year-i.birthday.year), month=i.birthday.month, day=i.birthday.day)
        if (birtday_year-nowdays_date).days <=7 and (birtday_year-nowdays_date).days >=0:
            birthday_days.append(i)
    return birthday_days

async def get_by_name(skip: int, user: User, limit: int, name: str, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts by specified name for a specific user.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param name: The name of the contact to retrieve.
    :type name: str
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The list of contacts where each of them has the specified name, or None if it does not exist.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(and_(Contact.name == name, Contact.user_id == user.id)).offset(skip).limit(limit).all()

async def get_by_surname(skip: int, user: User, limit: int, surname: str, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts by specified surname for a specific user.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param surname: The surname of the contact to retrieve.
    :type surname: str
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The list of contacts where each of them has the specified surname, or None if it does not exist.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(and_(Contact.surname == surname, Contact.user_id == user.id)).offset(skip).limit(limit).all()

async def get_by_email(skip: int, user: User, limit: int, email: str, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts by specified email for a specific user.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param email: The email of the contact to retrieve.
    :type email: str
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The list of contacts where each of them has the specified email, or None if it does not exist.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).offset(skip).limit(limit).all()

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(name=body.name, surname=body.surname, phone_number=body.phone_number,\
                      email=body.email, birthday=body.birthday, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactModel
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name=body.name, 
        contact.surname=body.surname, 
        contact.phone_number=body.phone_number,
        contact.email=body.email, 
        contact.birthday=body.birthday
        db.commit()
    return contact
