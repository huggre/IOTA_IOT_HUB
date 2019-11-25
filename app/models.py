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
    assets = db.relationship('tbl_assets', backref='member', lazy='dynamic')
    #tags = db.relationship('tbl_tags', backref='member', lazy='dynamic')
    #accounts = db.relationship('tbl_accounts', backref='member', lazy='dynamic')
    sensors = db.relationship('tbl_sensors', backref='member', lazy='dynamic')

    def __repr__(self):
        return '<Member {}>'.format(self.member_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define the Sensor types table
class tbl_sensor_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    sensors = db.relationship('tbl_sensors', backref='stype', lazy='dynamic')

    def __repr__(self):
        return '<SensorType {}>'.format(self.name)

# Define the Sensors table
class tbl_sensors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UID = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64))
    created = db.Column(db.DateTime, index=True, default=func.now())
    modified = db.Column(db.DateTime, index=True, default=func.now())
    sensor_type = db.Column(db.Integer, db.ForeignKey('tbl_sensor_types.id'))
    parent_asset = db.Column(db.Integer, db.ForeignKey('tbl_assets.id'))
    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))
    transactions = db.relationship('tbl_transactions', backref='trans_sensor_id', lazy='dynamic')

    def __repr__(self):
        return '<Sensor {}>'.format(self.name)

# Define the Asset types table
class tbl_asset_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    assets = db.relationship('tbl_assets', backref='atype', lazy='dynamic')

    def __repr__(self):
        return '<AssetType {}>'.format(self.name)

# Define the Assets table
class tbl_assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    KEY = db.Column(db.String(64))
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    price = db.Column(db.Float)
    balance = db.Column(db.Float)
    created = db.Column(db.DateTime, index=True, default=func.now())
    modified = db.Column(db.DateTime, index=True, default=func.now())
    asset_type = db.Column(db.Integer, db.ForeignKey('tbl_asset_types.id'))
    #account = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))
    sensors = db.relationship('tbl_sensors', backref='sensor_asset', lazy='dynamic')

    def __repr__(self):
        return '<Asset {}>'.format(self.name)

# Define the Asset Tags table (many-to-many)
class tbl_asset_tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('tbl_assets.id'))
    tag_UID = db.Column(db.Integer, db.ForeignKey('tbl_tags.tag_UID'))
    asset_tag_balance = db.Column(db.Float)

    #name = db.Column(db.String(64), index=True, unique=True)
    #assets = db.relationship('tbl_assets', backref='atype', lazy='dynamic')

    def __repr__(self):
        return '<AssetTag {}>'.format(self.name)

# Define the Tag types table
#class tbl_tag_types(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(64), index=True, unique=True)
#    tags = db.relationship('tbl_tags', backref='ttype', lazy='dynamic')

#    def __repr__(self):
#        return '<TagType {}>'.format(self.name)

# Define the Tags table
class tbl_tags(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #UID = db.Column(db.String(64), index=True, unique=True)
    tag_UID = db.Column(db.String(64), primary_key=True)
    #KEY = db.Column(db.String(64))
    #name = db.Column(db.String(64))
    created = db.Column(db.DateTime, index=True, default=func.now())
    #modified = db.Column(db.DateTime, index=True, default=func.now())
    #tag_type = db.Column(db.Integer, db.ForeignKey('tbl_tag_types.id'))
    #account = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
    #owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))
    transactions = db.relationship('tbl_transactions', backref='trans_tag_id', lazy='dynamic')

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

# Define the Transaction types table
class tbl_transaction_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    #tags = db.relationship('tbl_tags', backref='ttype', lazy='dynamic')
    transactions = db.relationship('tbl_transactions', backref='trans_type', lazy='dynamic')


    def __repr__(self):
        return '<TransType {}>'.format(self.name)

# Define the Transactions table
class tbl_transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_UID = db.Column(db.Integer, db.ForeignKey('tbl_tags.tag_UID'))
    #tag_account_id = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('tbl_sensors.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('tbl_assets.id'))
    #asset_account_id = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('tbl_transaction_types.id'))
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    transaction_value = db.Column(db.Float)

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)

# Define the Transaction Errors table
class tbl_transaction_errors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mqtt_msg = db.Column(db.String(64))
    error_desc = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=func.now())

    def __repr__(self):
        return '<TransactionError {}>'.format(self.id)

# Define the Accounts table
#class tbl_accounts(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(64))
#    balance = db.Column(db.Float)
#    created = db.Column(db.DateTime, index=True, default=func.now())
#    modified = db.Column(db.DateTime, index=True, default=func.now())
#    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))
#    assets = db.relationship('tbl_assets', backref='asset_account', lazy='dynamic')
    #tags = db.relationship('tbl_tags', backref='tag_account', lazy='dynamic')

#    def __repr__(self):
#        return '<Account {}>'.format(self.name)

# Define the Deposits table
#class tbl_deposits(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    account = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
#    value = db.Column(db.Float)
#    timestamp = db.Column(db.DateTime, index=True, default=func.now())
#    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))

#    def __repr__(self):
#        return '<Deposit {}>'.format(self.id)

# Define the Withdrawals table
#class tbl_withdrawals(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    account = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
#    value = db.Column(db.Float)
#    timestamp = db.Column(db.DateTime, index=True, default=func.now())
#    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))

#    def __repr__(self):
#        return '<Withdrawal {}>'.format(self.id)