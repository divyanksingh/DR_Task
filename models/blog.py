from application.extensions import db
import datetime

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    last_updated = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    deleted = db.Column(db.BOOLEAN, default = False)


