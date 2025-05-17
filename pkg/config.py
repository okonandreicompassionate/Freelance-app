

class BaseConfig(object):
    SECRET_KEY = "59InUNHh4Yqh2yzW_ieqv5CBOJnmW0Z73E2hZhPT8Ss"
    ADMIN_EMAIL = "blogger@blogger.com"
    ADMIN_NAME = "james henry"
    SQLALCHEMY_DATABASE_URI = 'postgresql://freelance_9we4_user:Geh9UJ8TXAqKAoDZS05ZWKKCpayWUu2V@dpg-d0jraqje5dus73b7v3k0-a.oregon-postgres.render.com/freelance_9we4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CONTACT_PHONE = "09088645334"
    API_KEY = "sample key"

class TestConfig(BaseConfig):
    DEBUG = True

class LiveConfig(BaseConfig):
    DEBUG = False
