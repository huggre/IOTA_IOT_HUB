import datetime

import requests

import json

#import iota_wallet as iw

from sqlalchemy.sql import func
from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify, abort, make_response

from app.ha_interact import call_service
#from app.wallet_interact import get_account
#from app.wallet_interact import get_acc_addr
#from app.wallet_interact import start_worker
#from thread_test2 import start_threads
#from wallet_worker import start_worker

# Get wallet account
#account = get_account(iw)

# Start Worker
#start_worker(account)

# Imports form objects
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import AssetForm
from app.forms import EndpointForm
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
from app.models import tbl_endpoints
from app.models import tbl_services
from app.models import tbl_transactions
from app.models import tbl_transaction_statuses
from app.models import tbl_settlements


# Get new address from worker API
def get_addr():
    url = 'http://localhost:5001/iotago_api/v1.0/get_addr'
    # Get API response
    resp = requests.get(url)
    if resp.status_code == 200:
        # Get response content
        response = json.loads(resp.text)

        return response['address']['inner']
        #print(response)

        # Update global asset_price var from response
        #global asset_price
        #asset_price = float(response['price'])
        # Add respose to asset details and activate Purchase tab
        #txt_asset_details.delete(1.0,"end")
        #txt_asset_details.insert(1.0, resp.text)
        #app_notebook.select(1)
    else:

        print('hey')
        # Write error to error log
        #txt_get_asset_log.delete(1.0,"end")
        #txt_get_asset_log.insert(1.0, resp.status_code)


@app.template_filter('make_datetime')
def make_datetime_from_seconds(seconds):
    return datetime.timedelta(seconds=seconds)

@app.template_filter('make_miota')
def make_miota_from_iota(iota):
    return iota/1000000

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


### ENDPOINTS

# List endpoints
@app.route('/my_endpoints')
def my_endpoints():
    endpoints = (db.session.query(tbl_endpoints)
    .filter(tbl_endpoints.owner == current_user.id)
    .add_columns(tbl_endpoints.id.label('id'), 
    tbl_endpoints.name.label('name'), 
    tbl_endpoints.endpoint.label('endpoint'), 
    tbl_endpoints.enabled.label('enabled')) 
    )
    return render_template("my_endpoints.html",endpoints = endpoints)

# Save endpoint function
def save_endpoint(endpoint, form, new=False):
    endpoint.name = form.name.data
    endpoint.description = form.description.data
    endpoint.endpoint = form.endpoint.data
    endpoint.token = form.token.data
    endpoint.enabled = form.enabled.data

    if new:
        # Add the new asset to the database
        #device.status = False
        #device.remaining_time = 0
        endpoint.owner = current_user.id
        #device.created_on = func.now()
        #device.created_by = current_user.id
        #device.modified = func.now()
        #device.modified_by = current_user.id
        db.session.add(endpoint)
    else:
        endpoint.modified_on = func.now()
        #device.modified_by = current_user.id
    # commit the data to the database
    db.session.commit()
    return True

# Create new endpoint
@app.route('/new_endpoint', methods=['GET', 'POST'])
def new_endpoint():

    form = EndpointForm()

    # Get new address from wallet and assign to payment address field
    #addr = get_acc_addr(account)
    #form.asset_address.data = addr
    
    # Add endpoints to SelectField
    #form.endpoint.choices = [(endpoint_row.id, endpoint_row.name) for endpoint_row in tbl_endpoints.query.all()]

    # Add services to SelectField
    #form.service.choices = [(service_row.id, service_row.name) for service_row in tbl_services.query.all()]

    # Add user accounts to SelectField
    #form.tag_account.choices = [(acc_row.id, acc_row.name) for acc_row in tbl_accounts.query.filter_by(owner=current_user.id)]

    if form.validate_on_submit():
        endpoint = tbl_endpoints()
        save_endpoint(endpoint, form, new=True)
        flash('New endpoint created sucessfully!!')
        return redirect(url_for('my_endpoints'))
    return render_template('endpoint.html', title='New endpoint', form=form)


# Edit existing endpoint
@app.route('/edit_endpoint/<int:id>', methods=['GET', 'POST'])
def edit_endpoint(id):

    endpoint = tbl_endpoints.query.filter_by(id=id).first_or_404()

    if endpoint:

        # Check ownership
        if endpoint.owner == current_user.id:

            form = EndpointForm()

            # Add endpoints to SelectField
            #form.endpoint.choices = [(endpoint_row.id, endpoint_row.name) for endpoint_row in tbl_endpoints.query.all()]

            # Add services to SelectField
            #form.service.choices = [(service_row.id, service_row.name) for service_row in tbl_services.query.all()]


            # Add user assets to SelectField
            #form.parent_asset.choices = [(parass_row.id, parass_row.name) for parass_row in tbl_assets.query.filter_by(owner=current_user.id)]

            if form.validate_on_submit():
                save_endpoint(endpoint, form)
                flash('Endpoint updated successfully!')
                return redirect(url_for('my_endpoints'))
            elif request.method == 'GET':
                # Populate form fields here
                form.name.data = endpoint.name
                form.description.data = endpoint.description
                form.endpoint.data = endpoint.endpoint
                form.token.data = endpoint.token
                form.enabled.data = endpoint.enabled

            return render_template('endpoint.html', title='Edit endpoint', form=form)

        else:
            flash('You are not authorized to edit this asset!!')
            return render_template('authorization_error.html', title='Not authorized!!')

    else:
        return 'Error loading #{id}'.format(id=id)


# Show endpoint details
@app.route('/endpoint_details/<int:id>')
def endpoint_details(id):
       
    endpoint = (db.session.query(tbl_endpoints)
        .filter(tbl_endpoints.id == id)
        .add_columns(tbl_endpoints.id.label('id'), 
        tbl_endpoints.name.label('name'),
        tbl_endpoints.description.label('description'),
        tbl_endpoints.endpoint.label('endpoint'),
        tbl_endpoints.token.label('token'),
        tbl_endpoints.enabled.label('enabled'),
        tbl_endpoints.created_on.label('created_on'),
        tbl_endpoints.modified_on.label('modified_on'))
        ).one_or_none()

    if endpoint:
        return render_template("endpoint_details.html", title='Endpoint Details', endpoint = endpoint)
    else:
        flash('Endpoint ID: ' + str(id) + ' does not exist!!')
        #return render_template('item_does_not_exist.html', title='Item does not exist!!')



### ASSETS

# List assets
@app.route('/my_assets')
def my_assets():
    assets = (db.session.query(tbl_assets)
    .filter(tbl_assets.owner == current_user.id)
    .add_columns(tbl_assets.id.label('id'), 
    tbl_assets.name.label('name'), 
    tbl_assets.price.label('price'), 
    tbl_assets.asset_address.label('payment_address'), 
    tbl_assets.enabled.label('enabled'))
    )
    return render_template("my_assets.html",assets = assets)


# Test service function
def test_service(form):
    # Get endpoint & token
    endpoint = (db.session.query(tbl_endpoints)
        .filter(tbl_endpoints.id == form.endpoint.data)
        .add_columns(tbl_endpoints.endpoint.label('endpoint'),
        tbl_endpoints.token.label('token'))
        ).one_or_none()

    service = (db.session.query(tbl_services)
        .filter(tbl_services.id == form.service.data)
        .add_columns(tbl_services.tech_name.label('tech_name'))
        ).one_or_none()   

    response = call_service(endpoint.endpoint, endpoint.token, service.tech_name, form.service_data.data)
    flash(response.text)

# Save asset function
def save_asset(asset, form, new=False):
    asset.name = form.name.data
    asset.description = form.description.data
    asset.price = form.price.data*1000000
    asset.asset_address = form.asset_address.data
    asset.settlement_address = form.settlement_address.data
    asset.endpoint = form.endpoint.data
    asset.service = form.service.data
    asset.service_data = form.service_data.data
    asset.enabled = form.enabled.data

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

    # Get new address from wallet and assign to payment address field

    #addr = get_acc_addr(account)

    addr=get_addr()

    form.asset_address.data = addr
    
    # Add endpoints to SelectField
    form.endpoint.choices = [(endpoint_row.id, endpoint_row.name) for endpoint_row in tbl_endpoints.query.all()]

    # Add services to SelectField
    form.service.choices = [(service_row.id, service_row.name) for service_row in tbl_services.query.all()]

    # Add user accounts to SelectField
    #form.tag_account.choices = [(acc_row.id, acc_row.name) for acc_row in tbl_accounts.query.filter_by(owner=current_user.id)]

    if form.validate_on_submit():
        if form.test_service.data:
            #print("hei")
            test_service(form)
        elif form.submit.data:
            asset = tbl_assets()
            save_asset(asset, form, new=True)
            flash('New asset created sucessfully!!')
            return redirect(url_for('my_assets'))
    return render_template('asset.html', title='New asset', form=form)


# Edit existing asset
@app.route('/edit_asset/<int:id>', methods=['GET', 'POST'])
def edit_asset(id):

    asset = tbl_assets.query.filter_by(id=id).first_or_404()

    if asset:

        # Check ownership
        if asset.owner == current_user.id:

            form = AssetForm()

            # Add endpoints to SelectField
            form.endpoint.choices = [(endpoint_row.id, endpoint_row.name) for endpoint_row in tbl_endpoints.query.all()]

            # Add services to SelectField
            form.service.choices = [(service_row.id, service_row.name) for service_row in tbl_services.query.all()]


            # Add user assets to SelectField
            #form.parent_asset.choices = [(parass_row.id, parass_row.name) for parass_row in tbl_assets.query.filter_by(owner=current_user.id)]

            if form.validate_on_submit():
                if form.test_service.data:
                    test_service(form)
                    #print("hei")
                elif form.submit.data:
                    save_asset(asset, form)
                    flash('Asset updated successfully!')
                    return redirect(url_for('my_assets'))
            elif request.method == 'GET':
                # Populate form fields here
                form.name.data = asset.name
                form.description.data = asset.description
                form.price.data = asset.price/1000000
                form.asset_address.data = asset.asset_address
                form.settlement_address.data = asset.settlement_address
                form.endpoint.data = asset.endpoint
                form.service.data = asset.service
                form.service_data.data = asset.service_data
                form.enabled.data = asset.enabled

            return render_template('asset.html', title='Edit asset', form=form)

        else:
            flash('You are not authorized to edit this asset!!')
            return render_template('authorization_error.html', title='Not authorized!!')

    else:
        return 'Error loading #{id}'.format(id=id)


# Show asset details
@app.route('/asset_details/<int:id>')
def asset_details(id):
       
    asset = (db.session.query(tbl_assets, tbl_endpoints, tbl_services)
        .join(tbl_endpoints)
        .join(tbl_services)
        .filter(tbl_assets.id == id)
        .add_columns(tbl_assets.id.label('id'), 
        tbl_assets.name.label('name'), 
        tbl_assets.description.label('description'), 
        tbl_assets.price.label('price'), 
        tbl_assets.enabled.label('enabled'), 
        tbl_assets.asset_address.label('asset_address'),
        tbl_assets.settlement_address.label('settlement_address'),
        tbl_endpoints.id.label('endpoint_id'),
        tbl_endpoints.name.label('endpoint_name'),
        tbl_services.name.label('service_name'),
        tbl_assets.service_data.label('service_data'),
        tbl_assets.created_on.label('created_on'),
        tbl_assets.modified_on.label('modified_on'))
        ).one_or_none()

    if asset:
        return render_template("asset_details.html", title='Asset Details', asset = asset)
    else:
        flash('Asset ID: ' + str(id) + ' does not exist!!')
        #return render_template('item_does_not_exist.html', title='Item does not exist!!')


### TRANSACTIONS


# List my transactions
@app.route('/my_transactions')
def my_transactions():
    transactions = (db.session.query(tbl_transactions, tbl_assets, tbl_transaction_statuses)
    .join(tbl_assets)
    .join(tbl_transaction_statuses)
    .filter(tbl_assets.owner == current_user.id)
    .add_columns(tbl_transactions.id.label('id'), 
    tbl_assets.id.label('asset_id'), 
    tbl_assets.name.label('asset_name'), 
    tbl_transaction_statuses.name.label('status'), 
    tbl_transactions.message_id.label('message_id'), 
    tbl_transactions.created_on.label('created_on'))
    )
    return render_template("my_transactions.html",transactions = transactions)

    '''

    asset = (db.session.query(tbl_assets, tbl_asset_types)
        .join(tbl_asset_types, tbl_assets.asset_type == tbl_asset_types.id)
        .join(tbl_members, tbl_assets.owner == tbl_members.id)
        .filter(tbl_assets.id == id)
        .add_columns(tbl_assets.id.label('asset_id'), 
        tbl_assets.created.label('asset_created'), 
        tbl_assets.modified.label('asset_modified'), 

    '''

# Show transaction details
@app.route('/transaction_details/<int:id>')
def transaction_details(id):
    transaction = (db.session.query(tbl_transactions, tbl_assets, tbl_endpoints, tbl_services, tbl_transaction_statuses)
        .join(tbl_assets, tbl_assets.id == tbl_transactions.asset)
        .join(tbl_endpoints, tbl_endpoints.id == tbl_transactions.endpoint)
        .join(tbl_services, tbl_endpoints.id == tbl_transactions.service)
        .join(tbl_transaction_statuses)
        .filter(tbl_transactions.id == id)
        .add_columns(tbl_transactions.id.label('id'), 
        tbl_assets.id.label('asset_id'), 
        tbl_assets.name.label('asset_name'), 
        tbl_transactions.transaction_price.label('transaction_price'),
        tbl_transactions.recieved_amount.label('recieved_amount'),
        tbl_transactions.asset_address.label('asset_address'),
        tbl_transactions.settlement_address.label('settlement_address'),
        tbl_endpoints.id.label('endpoint_id'),
        tbl_endpoints.name.label('endpoint_name'),
        tbl_services.name.label('service_name'),
        tbl_transactions.service_data.label('service_data'),
        tbl_transaction_statuses.name.label('status'), 
        tbl_transactions.message_id.label('message_id'), 
        tbl_transactions.created_on.label('created_on'), 
        tbl_transactions.settlement_id.label('settlement_id'))
        ).one_or_none()

    if transaction:
        return render_template("transaction_details.html", title='Transaction Details', transaction = transaction)
    else:
        flash('Transaction ID: ' + str(id) + ' does not exist!!')
        #return render_template('item_does_not_exist.html', title='Item does not exist!!')


# SETTLEMENTS

# Show settlement details
@app.route('/settlement_details/<int:id>')
def settlement_details(id):
    settlement = (db.session.query(tbl_settlements)
        .filter(tbl_settlements.id == id)
        .add_columns(tbl_settlements.id.label('id'), 
        tbl_settlements.address.label('address'), 
        tbl_settlements.value.label('value'), 
        tbl_settlements.completed.label('completed'),
        tbl_settlements.completed_on.label('completed_on'),
        tbl_settlements.message_id.label('message_id'), 
        tbl_settlements.created_on.label('created_on'))
        ).one_or_none()

    if settlement:
        return render_template("settlement_details.html", title='Settlement Details', settlement = settlement)
    else:
        flash('Settlement ID: ' + str(id) + ' does not exist!!')
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

