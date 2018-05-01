from application.extensions import db
from werkzeug.security import (
        generate_password_hash,
        check_password_hash
)

class UserInfo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    display_name = db.Column(db.String)
    password = db.Column(db.String, nullable=False)


    def update_password(self, new_password):
        self.password = generate_password_hash(new_password)

    def has_password(self, passwd):
        return check_password_hash(self.password, passwd)






