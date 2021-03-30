from app import db
from datetime import datetime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return tbl_members.query.get(int(id))

# Define the Members table
class tbl_members(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    created = db.Column(db.DateTime, index=True, default=func.now())
    modified = db.Column(db.DateTime, index=True, default=func.now())

    def __repr__(self):
        return '<Member {}>'.format(self.member_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Define Devices table
class tbl_devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    status = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float)
    remaining_time = db.Column(db.Integer)
    payment_address = db.Column(db.String(64))
    created_on = db.Column(db.DateTime, index=True, default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))
    modified_on = db.Column(db.DateTime, index=True, default=func.now())
    modified_by = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))

    def __repr__(self):
        return '<Service {}>'.format(self.name)

