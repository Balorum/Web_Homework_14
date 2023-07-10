from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import sys, os
sys.path.append(os.path.abspath('..'))

from src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import settings

class Auth:
    """
    A class that describes the security of a user's access to his account.

    :param pwd_context: Helper for hashing passwords.
    :type pwd_context: CryptContext
    :param SECRET_KEY: secret key.
    :type SECRET_KEY: str
    :param ALGORITHM: algorithm of encryption.
    :type ALGORITHM: str
    :param oauth2_scheme: Encrypted user data.
    :type oauth2_scheme: OAuth2PasswordBearer
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def verify_password(self, plain_password, hashed_password):
        """
        Checks for the hashed and plain password match.

        :param self: Auth class instance.
        :type self: Auth
        :param plain_password: Unencrypted password.
        :type plain_password: str
        :param hashed_password: Hashed password.
        :type hashed_password: str
        :return: Returns the hashed and plain password match.
        :rtype: bool
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        Hashes the password.

        :param self: Auth class instance.
        :type self: Auth
        :param password: Unencrypted password.
        :type password: str
        :return: Returns the hashed password.
        :rtype: str
        """
        return self.pwd_context.hash(password)
    
    def create_email_token(self, data: dict):
        """
        Create email token.

        :param self: Auth class instance.
        :type self: Auth
        :param data: Old data.
        :type data: dict
        :return: Returns a new token.
        :rtype: str
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    # define a function to generate a new access token
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Create access token.

        :param self: Auth class instance.
        :type self: Auth
        :param data: Old data.
        :type data: dict
        :param expires_delta: Timer before updating data.
        :type expires_delta: Optional[float]
        :return: Returns a new access token.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Create refresh token.

        :param self: Auth class instance.
        :type self: Auth
        :param data: Old data.
        :type data: dict
        :param expires_delta: Timer before updating data.
        :type expires_delta: Optional[float]
        :return: Returns a new refresh token.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        Decode refresh token.

        :param self: Auth class instance.
        :type self: Auth
        :param refresh_token: refresh token.
        :type refresh_token: str
        :return: Returns email.
        :rtype: str
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        Decode refresh token.

        :param self: Auth class instance.
        :type self: Auth
        :param token: Unique user token.
        :type token: str
        :param db: The database session.
        :type db: Session
        :return: Returns current user.
        :rtype: User
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user


auth_service = Auth()