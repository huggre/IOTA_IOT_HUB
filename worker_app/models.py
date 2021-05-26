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
    assets = db.relationship('tbl_assets', backref='member', lazy='dynamic')
    created_on = db.Column(db.DateTime, index=True, default=func.now())
    modified_on = db.Column(db.DateTime, index=True, default=func.now())

    def __repr__(self):
        return '<Member {}>'.format(self.member_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Define Assets table
class tbl_assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text())
    price = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=True)
    asset_address = db.Column(db.String(64), unique=True)
    settlement_address = db.Column(db.String(64))
    endpoint = db.Column(db.Integer, db.ForeignKey('tbl_endpoints.id'))
    service = db.Column(db.Integer, db.ForeignKey('tbl_services.id'))
    service_data = db.Column(db.Text())
    created_on = db.Column(db.DateTime, index=True, default=func.now())
    modified_on = db.Column(db.DateTime, index=True, default=func.now())
    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))

    def __repr__(self):
        return '<Asset {}>'.format(self.name)


# Define HA Endpoints table
class tbl_endpoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text())
    endpoint = db.Column(db.String(64))
    token = db.Column(db.String(256))
    enabled = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.DateTime, index=True, default=func.now())
    modified_on = db.Column(db.DateTime, index=True, default=func.now())
    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))

    def __repr__(self):
        return '<Endpoint {}>'.format(self.name)


# Define HA Services table
class tbl_services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    tech_name = db.Column(db.String(64))

    def __repr__(self):
        return '<Service {}>'.format(self.name)


# Define Transaction Statuses table
class tbl_transaction_statuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<TransactionStatus {}>'.format(self.name)

# Define Transactions table
class tbl_transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset = db.Column(db.Integer, db.ForeignKey('tbl_assets.id'))
    transaction_price = db.Column(db.Integer)
    recieved_amount = db.Column(db.Integer)
    asset_address = db.Column(db.String(64))
    settlement_address = db.Column(db.String(64))
    endpoint = db.Column(db.Integer, db.ForeignKey('tbl_endpoints.id'))
    service = db.Column(db.Integer, db.ForeignKey('tbl_services.id'))
    service_data = db.Column(db.Text())
    status = db.Column(db.Integer, db.ForeignKey('tbl_transaction_statuses.id'))
    message_id = db.Column(db.String(64))
    created_on = db.Column(db.DateTime, index=True, default=func.now())
    settlement_id = db.Column(db.Integer, db.ForeignKey('tbl_settlements.id'))

    def __repr__(self):
        return '<Transaction {}>'.format(self.name)


# Define Settlements table
class tbl_settlements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64))
    value = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    completed_on = db.Column(db.DateTime, index=True)
    message_id = db.Column(db.String(64))
    created_on = db.Column(db.DateTime, index=True, default=func.now())

    def __repr__(self):
        return '<Settlement {}>'.format(self.name)