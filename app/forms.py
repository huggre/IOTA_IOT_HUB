from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

#from flask_sqlalchemy import SQLAlchemy
#from wtforms.ext.sqlalchemy.fields import QuerySelectField
#from wtforms_sqlalchemy.fields import QuerySelectField

from app.models import tbl_members
#from app.models import tbl_sensor_types

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = tbl_members.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = tbl_members.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
	
#def choice_query():
#    return tbl_sensor_types.query

#class Choiceform(FlaskForm):
#    opts = QuerySelectField(query_factory=choice_query,allow_blank=True)

class AssetForm(FlaskForm):
    asset_name = StringField('Name', validators=[DataRequired()])
    asset_type = SelectField('Type', coerce=int)
    asset_city = StringField('City', validators=[DataRequired()])
    asset_country = StringField('Country', validators=[DataRequired()])
    asset_latitude = FloatField('Latitude', default='0.0', validators=[DataRequired()])
    asset_longitude = FloatField('Longitude', default='0.0', validators=[DataRequired()])
    asset_account = SelectField('Account', coerce=int)
    asset_price = FloatField('Price', default='0.0', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SensorForm(FlaskForm):
    sensor_name = StringField('Name', validators=[DataRequired()])
    sensor_type = SelectField('Type', coerce=int)
    parent_asset = SelectField('Parent asset', coerce=int)
    sensor_UID = StringField('UID', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AccountForm(FlaskForm):
    account_name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TagForm(FlaskForm):
    tag_name = StringField('Name', validators=[DataRequired()])
    tag_type = SelectField('Type', coerce=int)
    tag_account = SelectField('Account', coerce=int)
    tag_UID = StringField('UID', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DepositForm(FlaskForm):
    account = SelectField('Account', coerce=int)
    #value = StringField('Value', validators=[DataRequired()])
    deposit_address = StringField('IOTA Deposit Address', validators=[DataRequired()])
    value = FloatField('Amount', default='0.0', validators=[DataRequired()])
    submit = SubmitField('Submit')

class WithdrawalForm(FlaskForm):
    account = SelectField('Account', coerce=int)
    value = FloatField('Amount', default='0.0', validators=[DataRequired()])
    submit = SubmitField('Submit')