from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def register_extension(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    return app