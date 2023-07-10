import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.append(os.path.abspath('../..'))

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    )


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email(self):
        users = [User(email="test1@gmail.com"), User(email="test2@gmail.com"), User(email="test3@gmail.com")]
        self.session.query().filter().first.return_value = users
        result = await get_user_by_email(email="test2@gmail.com", db=self.session)
        self.assertEqual(result, users)

    async def test_create_user(self):
        body=UserModel(username="test.test", email="test#gmail.com", password="test.test")
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_token(self):
        token="test"
        refresh_token="test2"
        user = User(refresh_token=token)
        result = await update_token(user=user, token=refresh_token, db=self.session)
        self.assertEqual(user.refresh_token, refresh_token)


if __name__ == '__main__':
    unittest.main()