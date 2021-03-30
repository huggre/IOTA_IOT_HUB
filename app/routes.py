
from sqlalchemy.sql import func
from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify, abort, make_response

# Imports form objects
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import DeviceForm

# Imports IOTA IOT Hub db
from app import db

# Imports flask_login 
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

# Imports model objects
from app.models import tbl_devices
from app.models import tbl_members


### HOME ###

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html',title="Home")


### LOGINS AND MEMBER REGISTRATION ###

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = tbl_members.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = tbl_members(name=form.username.data, email=form.email.data, phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# List devices
@app.route('/devices')
def devices():
    devices = (db.session.query(tbl_devices)
    .add_columns(tbl_devices.id.label('device_id'), 
    tbl_devices.name.label('device_name'), 
    tbl_devices.price.label('device_price'), 
    tbl_devices.payment_address.label('device_payment_address'), 
    tbl_devices.remaining_time.label('device_remaining_time'), 
    tbl_devices.status.label('device_status'))
    )
    return render_template("devices.html",devices = devices)

# Save device function
def save_device(device, form, new=False):
    device.name = form.device_name.data
    device.price = form.device_price.data
    device.payment_address = form.device_payment_address.data
    if new:
        # Add the new asset to the database
        device.status = False
        device.remaining_time = 0
        device.created_on = func.now()
        device.created_by = current_user.id
        device.modified_on = func.now()
        device.modified_by = current_user.id
        db.session.add(device)
    else:
        device.modified_on = func.now()
        device.modified_by = current_user.id
    # commit the data to the database
    db.session.commit()
    return True

# Create new device
@app.route('/new_device', methods=['GET', 'POST'])
def new_device():

    form = DeviceForm()
    
    # Add tag types to SelectField
    #form.tag_type.choices = [(tagtype_row.id, tagtype_row.name) for tagtype_row in tbl_tag_types.query.all()]

    # Add user accounts to SelectField
    #form.tag_account.choices = [(acc_row.id, acc_row.name) for acc_row in tbl_accounts.query.filter_by(owner=current_user.id)]

    if form.validate_on_submit():
        device = tbl_devices()
        save_device(device, form, new=True)
        flash('New device created sucessfully!!')
        return redirect(url_for('devices'))
    return render_template('device.html', title='New device', form=form)


# Edit existing device
@app.route('/edit_device/<int:id>', methods=['GET', 'POST'])
def edit_device(id):

    device = tbl_devices.query.filter_by(id=id).first_or_404()

    if device:

        form = DeviceForm()

        # Add sensor types to SelectField
        #form.sensor_type.choices = [(senstype_row.id, senstype_row.name) for senstype_row in tbl_sensor_types.query.all()]

        # Add user assets to SelectField
        #form.parent_asset.choices = [(parass_row.id, parass_row.name) for parass_row in tbl_assets.query.filter_by(owner=current_user.id)]

        if form.validate_on_submit():
            save_device(device, form)
            flash('Device updated successfully!')
            return redirect(url_for('devices'))
        elif request.method == 'GET':
            # Populate form fields here
            form.device_name.data = device.name
            form.device_price.data = device.price
            form.device_payment_address.data = device.payment_address

        return render_template('device.html', title='Edit device', form=form)

    else:
        return 'Error loading #{id}'.format(id=id)

