import os

class BaseConfig(object):
    SECRET_KEY = "59InUNHh4Yqh2yzW_ieqv5CBOJnmW0Z73E2hZhPT8Ss"
    ADMIN_EMAIL = "blogger@blogger.com"
    ADMIN_NAME = "james henry"
    # Use environment variable DATABASE_URL if it exists, else fallback to hardcoded URI
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "ppostgresql://neondb_owner:npg_WlT2q6YEZCeH@ep-dawn-snowflake-abnqf7zr-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require" 
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CONTACT_PHONE = "09088645334"
    API_KEY = "sample key"

class TestConfig(BaseConfig):
    DEBUG = True

class LiveConfig(BaseConfig):
    DEBUG = False
