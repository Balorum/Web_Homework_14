import unittest
from unittest.mock import MagicMock
import sys
import os
from datetime import date

sys.path.append(os.path.abspath('../..'))

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    get_by_name,
    get_by_surname,
    get_by_email,
    )


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_note_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(name="test name", surname="test surname", phone_number="+38097789815", email="test@gmail.com",\
                            birthday=date(2003, 12, 29))
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = ContactModel(name="test name", surname="test surname", phone_number="+38097789815", email="test@gmail.com",\
                            birthday=date(2003, 12, 29))
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, db=self.session, user=self.user)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_note_found(self):
        body = ContactModel(name="test name", surname="test surname", phone_number="+38097789815", email="test@gmail.com",\
                            birthday=date(2003, 12, 29))
        contact = Contact(name="test2")
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_note_not_found(self):
        body = ContactModel(name="test name", surname="test surname", phone_number="+38097789815", email="test@gmail.com",\
                            birthday=date(2003, 12, 29))
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_by_name(self):
        contacts = [Contact(name="Nikita"), Contact(name="Ivan"), Contact(name="Boris")]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_by_name(skip=0, limit=10, user=self.user, name="Ivan", db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_by_surname(self):
        contacts = [Contact(surname="Ivanov"), Contact(surname="Petrov"), Contact(surname="Hun")]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_by_surname(skip=0, limit=10, user=self.user, surname="Petrov", db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_by_email(self):
        contacts = [Contact(email="test@gmail.com"), Contact(email="test1@gmail.com"), Contact(email="test2@gmail.com")]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_by_email(skip=0, limit=10, user=self.user, email="test1@gmail.com", db=self.session)
        self.assertEqual(result, contacts)



if __name__ == '__main__':
    unittest.main()