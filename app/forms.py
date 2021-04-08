# Imports IotaGo form dependencies
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

# Imports the IotaGo members table
from app.models import tbl_members

# IotaGo login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Registration form for new IotaGo members
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

# Form for new/edit Device
class AssetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price (MIOTA pr. hour)', default='0.0', validators=[DataRequired()])
    payment_address = StringField('IOTA Address', validators=[DataRequired()])
    #parent_asset = SelectField('Parent asset', coerce=int)
    #sensor_UID = StringField('UID', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form for new/edit Device
class AppForm(FlaskForm):
    asset_id = IntegerField('AssetID', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form for new Order
class OrderForm(FlaskForm):
    hours = StringField('Specify the amount of time you plan to use the asset [Days]:[Hours]:[Minutes]', default='00:00:00', validators=[DataRequired()])
    submit = SubmitField('Submit')


