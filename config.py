import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class DevConfig(object):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + os.path.join(BASE_DIR, "db.sqlite3")
    SECRET_KEY = "36we241c-39a1hw567-87dc03dc-685b35ce6b"


app_config = {
        "development": DevConfig,
}