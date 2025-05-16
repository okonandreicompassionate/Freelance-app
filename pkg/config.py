# ADMIN_EMAIL="admin@blogger.com"
# SECRET_KEY="59InUNHh4Yqh2yzW_ieqv5CBOJnmW0Z73E2hZhPT8Ss"

class BaseConfig(object):
    API_KEY="sample key"
    SECRET_KEY='1234'
    CONTACT_PHONE="09088645334"


class TestConfig(BaseConfig):
    DBCONN = "connect to TEST "


class LiveConfig(BaseConfig):
    DBCONN="connect to LIVE db"