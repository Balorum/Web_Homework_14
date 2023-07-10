from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    This is the class that describes private variables for our API

    :param sqlalchemy_database_url: Url of our database.
    :type sqlalchemy_database_url: str
    :param secret_key: Secret key.
    :type secret_key: str
    :param algorithm: Encoding algorithm.
    :type algorithm: str
    :param mail_username: Email username for sending emails.
    :type mail_username: str
    :param mail_password: Email password for sending emails.
    :type mail_password: str
    :param mail_from: Mail from which the mailing occurs.
    :type mail_from: str
    :param mail_port: Mail port for mailing.
    :type mail_port: int
    :param mail_server: Mail domain for mailing.
    :type mail_server: str
    :param redis_host: Redis host.
    :type redis_host: str
    :param redis_port: Redis port.
    :type redis_port: int
    """
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379

    class Config:
        """
        This is the class that describes configuration of our API

        :param env_file: Location of the .env directory.
        :type env_file: str
        :param env_file_encoding: How to encode our configuration.
        :type env_file_encoding: str
        """
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()