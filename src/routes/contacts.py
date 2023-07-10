from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import sys, os
sys.path.append(os.path.abspath('..'))

from src.services.auth import auth_service
from src.database.models import User
from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts

from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Processing the / route - pages to view all user contacts.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param current_user: User data.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Returns the user's contact list.
    :rtype: list
    """
    contacts = await repository_contacts.get_contacts(skip, current_user, limit, db)
    return contacts

@router.get("/days_to_birthday", response_model=List[ContactResponse])
async def read_birthdays(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Processing the /days_to_birthday route - pages to view a user's contacts who have a birthday this week.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param current_user: User data.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Returns the user's contact list whose birthday is this week.
    :rtype: list
    """
    contacts = await repository_contacts.get_days_to_birthday(skip, current_user, limit, db)
    return contacts

@router.get("/get_by_name", response_model=List[ContactResponse])
async def read_names(skip: int = 0, limit: int = 100, name: str = "Olya", db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Processing the /get_by_name route - pages to view a user's contacts with a specific name.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param name: The name by which to search for contacts.
    :type name: str
    :param current_user: User data.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Returns the user's contact list with given name.
    :rtype: list
    """
    contacts = await repository_contacts.get_by_name(skip, current_user, limit, name, db)
    return contacts

@router.get("/get_by_surname", response_model=List[ContactResponse])
async def read_surname(skip: int = 0, limit: int = 100, surname: str = "Ivanov", db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Processing the /get_by_surname route - pages to view a user's contacts with a specific surname.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param surname: The surname by which to search for contacts.
    :type surname: str
    :param current_user: User data.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Returns the user's contact list with given surname.
    :rtype: list
    """
    contacts = await repository_contacts.get_by_surname(skip, current_user, limit, surname, db)
    return contacts

@router.get("/get_by_email", response_model=List[ContactResponse])
async def read_email(skip: int = 0, limit: int = 100, email: str = "TestEmail@gmail.com", db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Processing the /get_by_email route - pages to view a user's contacts with a specific email.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param email: The email by which to search for contacts.
    :type email: str
    :param current_user: User data.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Returns the user's contact list with given email.
    :rtype: list
    """
    contacts = await repository_contacts.get_by_email(skip, current_user, limit, email, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Processing the /{contact_id} route - pages to view a specific contact.

    :param contact_id: Unique contact ID.
    :type contact_id: int
    :param current_user: User data.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Returns the specific contact.
    :rtype: Contact
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Processing the / route - pages to create a contact.

    :param body: Form (with fields) for creating a contact.
    :type body: ContactModel
    :param current_user: User data.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Returns created contact.
    :rtype: Contact
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Processing the /{contact_id} route - pages to update a contact.

    :param contact_id: Unique contact ID.
    :type contact_id: int
    :param body: Form (with fields) for updating a contact.
    :type body: ContactModel
    :param current_user: User data.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Returns updated contact.
    :rtype: Contact
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Processing the /{contact_id} route - pages to remove a contact.

    :param contact_id: Unique contact ID.
    :type contact_id: int
    :param current_user: User data.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Returns removed contact.
    :rtype: Contact
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact