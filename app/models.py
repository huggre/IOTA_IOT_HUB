from app import db
from datetime import datetime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return tbl_members.query.get(int(id))

class tbl_members(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created = db.Column(db.DateTime, index=True, default=func.now())
    modified = db.Column(db.DateTime, index=True, default=func.now())
    assets = db.relationship('tbl_assets', backref='member', lazy='dynamic')
    tags = db.relationship('tbl_tags', backref='member', lazy='dynamic')
    accounts = db.relationship('tbl_accounts', backref='member', lazy='dynamic')
    sensors = db.relationship('tbl_sensors', backref='member', lazy='dynamic')

    def __repr__(self):
        return '<Member {}>'.format(self.member_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class tbl_sensor_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    sensors = db.relationship('tbl_sensors', backref='stype', lazy='dynamic')

    def __repr__(self):
        return '<SensorType {}>'.format(self.name)

#class tbl_sensor_models(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    sensor_model_name = db.Column(db.String(64), index=True, unique=True)
#    sensor_model_type = db.Column(db.Integer, db.ForeignKey('tbl_sensor_types.id'))
#    sensors = db.relationship('tbl_sensors', backref='sens_model', lazy='dynamic')   

#    def __repr__(self):
#        return '<SensorModel {}>'.format(self.sensor_model_name)

class tbl_sensors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UID = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64))
    created = db.Column(db.DateTime, index=True, default=func.now())
    modified = db.Column(db.DateTime, index=True, default=func.now())
    sensor_type = db.Column(db.Integer, db.ForeignKey('tbl_sensor_types.id'))
    parent_asset = db.Column(db.Integer, db.ForeignKey('tbl_assets.id'))
    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))
    #assets = db.relationship('tbl_assets', backref='sensor', lazy='dynamic')
    transactions = db.relationship('tbl_transactions', backref='trans_sensor_id', lazy='dynamic')

    def __repr__(self):
        return '<Sensor {}>'.format(self.name)

class tbl_asset_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    assets = db.relationship('tbl_assets', backref='atype', lazy='dynamic')

    def __repr__(self):
        return '<AssetType {}>'.format(self.name)

class tbl_assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    price = db.Column(db.Float)
    created = db.Column(db.DateTime, index=True, default=func.now())
    modified = db.Column(db.DateTime, index=True, default=func.now())
    asset_type = db.Column(db.Integer, db.ForeignKey('tbl_asset_types.id'))
    account = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))
    sensors = db.relationship('tbl_sensors', backref='sensor_asset', lazy='dynamic')
    #transactions = db.relationship('tbl_transactions', backref='asset_trans', lazy='dynamic')

    def __repr__(self):
        return '<Asset {}>'.format(self.name)

class tbl_tag_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    tags = db.relationship('tbl_tags', backref='ttype', lazy='dynamic')

    def __repr__(self):
        return '<TagType {}>'.format(self.name)

class tbl_tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UID = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64))
    created = db.Column(db.DateTime, index=True, default=func.now())
    modified = db.Column(db.DateTime, index=True, default=func.now())
    tag_type = db.Column(db.Integer, db.ForeignKey('tbl_tag_types.id'))
    account = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))
    transactions = db.relationship('tbl_transactions', backref='trans_tag_id', lazy='dynamic')

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

class tbl_transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mqtt_sensor_UID = db.Column(db.String(64))
    mqtt_tag_UID = db.Column(db.String(64))
    tag_id = db.Column(db.Integer, db.ForeignKey('tbl_tags.id'))
    tag_account_id = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('tbl_sensors.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('tbl_assets.id'))
    asset_account_id = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    transaction_value = db.Column(db.Float)

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)

class tbl_transaction_errors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mqtt_msg = db.Column(db.String(64))
    error_desc = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=func.now())

    def __repr__(self):
        return '<TransactionError {}>'.format(self.id)

class tbl_accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    balance = db.Column(db.Float)
    created = db.Column(db.DateTime, index=True, default=func.now())
    modified = db.Column(db.DateTime, index=True, default=func.now())
    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))
    assets = db.relationship('tbl_assets', backref='asset_account', lazy='dynamic')
    tags = db.relationship('tbl_tags', backref='tag_account', lazy='dynamic')


    def __repr__(self):
        return '<Account {}>'.format(self.name)


class tbl_deposits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
    transaction_hash = db.Column(db.String(128))
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))

    def __repr__(self):
        return '<Deposit {}>'.format(self.id)

class tbl_withdrawals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.Integer, db.ForeignKey('tbl_accounts.id'))
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    owner = db.Column(db.Integer, db.ForeignKey('tbl_members.id'))

    def __repr__(self):
        return '<Withdrawal {}>'.format(self.id)