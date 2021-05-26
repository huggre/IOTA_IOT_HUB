
# Imports IotaGo form dependencies
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateTimeField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
#from wtforms.fields.html5 import DateField
from wtforms.fields import DateField
#from wtforms import DateTimeLocalField
from wtforms.fields.html5 import DateTimeLocalField

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

# Form for new/edit Asset
class AssetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired()])
    description = TextAreaField('Asset Description')
    price = FloatField('Asset Price (MIOTA)', default='0.0', validators=[DataRequired()])
    asset_address = StringField('Asset Address', render_kw={'readonly': True}, validators=[DataRequired()])
    settlement_address = StringField('Settlement Address', validators=[DataRequired()])
    endpoint = SelectField('Home Assistant Endpoint', coerce=int)
    service = SelectField('Home Assistant Service', coerce=int)
    service_data = TextAreaField('Home Assistant Service Data', default='{}', validators=[DataRequired()])
    test_service = SubmitField('Test Service')
    enabled = BooleanField('Enabled', default=True)
    #endpoint = SelectField('Home Assistant Endpoint', validators=[DataRequired()])
    #parent_asset = SelectField('Parent asset', coerce=int)
    #sensor_UID = StringField('UID', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form for new/edit Device
class EndpointForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    endpoint = StringField('URL', validators=[DataRequired()])
    token = StringField('Token', validators=[DataRequired()])
    enabled = BooleanField('Enabled', default=True)
    submit = SubmitField('Submit')

# Form for new/edit Device
class AppForm(FlaskForm):
    asset_id = IntegerField('AssetID', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form for new Order
class OrderForm(FlaskForm):
    addr = StringField()


