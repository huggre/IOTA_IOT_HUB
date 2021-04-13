import datetime

from sqlalchemy.sql import func
from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify, abort, make_response

# Imports form objects
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import AssetForm
from app.forms import AppForm
from app.forms import OrderForm


# Imports iotago db
from app import db

# Imports flask_login 
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

# Imports model objects
from app.models import tbl_assets
from app.models import tbl_members

@app.template_filter('make_datetime')
def make_datetime_from_seconds(seconds):
    return datetime.timedelta(seconds=seconds)

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


# List assets
@app.route('/my_assets')
def my_assets():
    assets = (db.session.query(tbl_assets)
    .filter(tbl_assets.owner == current_user.id)
    .add_columns(tbl_assets.id.label('id'), 
    tbl_assets.name.label('name'), 
    tbl_assets.price.label('price'), 
    tbl_assets.payment_address.label('payment_address'), 
    tbl_assets.remaining_time.label('remaining_time'), 
    tbl_assets.status.label('status'))
    )
    return render_template("my_assets.html",assets = assets)

# Save asset function
def save_asset(asset, form, new=False):
    asset.name = form.name.data
    asset.price = form.price.data
    asset.payment_address = form.payment_address.data
    if new:
        # Add the new asset to the database
        #device.status = False
        #device.remaining_time = 0
        asset.owner = current_user.id
        #device.created_on = func.now()
        #device.created_by = current_user.id
        #device.modified = func.now()
        #device.modified_by = current_user.id
        db.session.add(asset)
    else:
        asset.modified_on = func.now()
        #device.modified_by = current_user.id
    # commit the data to the database
    db.session.commit()
    return True

# Create new asset
@app.route('/new_asset', methods=['GET', 'POST'])
def new_asset():

    form = AssetForm()
    
    # Add tag types to SelectField
    #form.tag_type.choices = [(tagtype_row.id, tagtype_row.name) for tagtype_row in tbl_tag_types.query.all()]

    # Add user accounts to SelectField
    #form.tag_account.choices = [(acc_row.id, acc_row.name) for acc_row in tbl_accounts.query.filter_by(owner=current_user.id)]

    if form.validate_on_submit():
        asset = tbl_assets()
        save_asset(asset, form, new=True)
        flash('New asset created sucessfully!!')
        return redirect(url_for('my_assets'))
    return render_template('asset.html', title='New asset', form=form)


# Edit existing device
@app.route('/edit_asset/<int:id>', methods=['GET', 'POST'])
def edit_asset(id):

    asset = tbl_assets.query.filter_by(id=id).first_or_404()

    if asset:

        # Check ownership
        if asset.owner == current_user.id:

            form = AssetForm()

            # Add sensor types to SelectField
            #form.sensor_type.choices = [(senstype_row.id, senstype_row.name) for senstype_row in tbl_sensor_types.query.all()]

            # Add user assets to SelectField
            #form.parent_asset.choices = [(parass_row.id, parass_row.name) for parass_row in tbl_assets.query.filter_by(owner=current_user.id)]

            if form.validate_on_submit():
                save_asset(asset, form)
                flash('Asset updated successfully!')
                return redirect(url_for('my_assets'))
            elif request.method == 'GET':
                # Populate form fields here
                form.name.data = asset.name
                form.price.data = asset.price
                form.payment_address.data = asset.payment_address

            return render_template('asset.html', title='Edit asset', form=form)

        else:
            flash('You are not authorized to edit this asset!!')
            return render_template('authorization_error.html', title='Not authorized!!')

    else:
        return 'Error loading #{id}'.format(id=id)


# Show asset details
@app.route('/asset_details/<int:id>')
def asset_details(id):
       
    asset = (db.session.query(tbl_assets)
        .filter(tbl_assets.id == id)
        .add_columns(tbl_assets.id.label('id'), 
        tbl_assets.name.label('name'), 
        tbl_assets.price.label('price'), 
        tbl_assets.payment_address.label('payment_address')) 
        ).one_or_none()

    if asset:
        return render_template("asset_details.html",asset = asset)
    else:
        flash('Asset ID: ' + str(id) + ' does not exist!!')
        #return render_template('item_does_not_exist.html', title='Item does not exist!!')



# Enter the iotago App
@app.route('/iotago_app', methods=['GET', 'POST'])
def iotago_app():

    form = AppForm()

    if form.validate_on_submit():

        #user = request.form['name']
        asset_id = form.asset_id.data

        #print(device_id)

        #return redirect(url_for('dashboard',name = user))

        # check that device exist
        #flash('Device updated successfully!')
        

        return redirect(url_for('new_order', id=asset_id))


    return render_template('iotago_app.html',title="iotago App", form=form)


# Make new order
@app.route('/new_order/<int:id>', methods=['GET', 'POST'])
def new_order(id):

    form = OrderForm()

    asset = (db.session.query(tbl_assets)
        .filter(tbl_assets.id == id)
        .add_columns(tbl_assets.id.label('id'), 
        tbl_assets.name.label('name'), 
        tbl_assets.price.label('price'), 
        tbl_assets.payment_address.label('payment_address')) 
        ).one_or_none()

    form.addr.data = asset.payment_address

    if asset:
        return render_template("new_order_6.html", title="New order", form=form, asset = asset)
    else:
        flash('Asset ID: ' + str(id) + ' does not exist!!')
        #return render_template('item_does_not_exist.html', title='Item does not exist!!')




# Show order confirmation
@app.route('/order_confirmation')
def order_confirmation():

    return render_template('order_confirmation.html',title="Order confirmation!!!")




### REST API

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

# curl -i http://localhost:5000/iotago_api/v1.0/tasks
@app.route('/iotago_api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Get asset info
# curl -i http://localhost:5000/iotago_api/v1.0/get_asset_info/1
@app.route('/iotago_api/v1.0/get_asset_info/<int:asset_id>', methods=['GET'])
def get_asset_info(asset_id):

    asset = (db.session.query(tbl_assets)
        .filter(tbl_assets.id == asset_id)
        .add_columns(tbl_assets.id.label('id'), 
        tbl_assets.name.label('name'), 
        tbl_assets.price.label('price'), 
        tbl_assets.payment_address.label('payment_address')) 
        ).one_or_none()

    if len(asset) == 0:
        abort(404)
    #return jsonify({'asset_price': asset.asset_price})
    return jsonify({'id': asset.id, 'name': asset.name, 'price': asset.price, 'payment_address': asset.payment_address})

