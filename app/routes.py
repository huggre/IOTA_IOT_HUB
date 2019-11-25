
from sqlalchemy.sql import func
from app import app
from flask import render_template, flash, redirect, url_for, request

# Imports the Flask Google-Maps library
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDFg_Ffjib_aMSSju_6Y5uo12xdjg4679c"
GoogleMaps(app)

# Imports form objects
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import AssetForm
from app.forms import SensorForm
from app.forms import AccountForm
from app.forms import TagForm
from app.forms import DepositForm
from app.forms import WithdrawalForm

# Imports table objects
from app.tables import AccountsTable
from app.tables import AssetsTable
from app.tables import MembersTable
from app.tables import SensorsTable
from app.tables import TagsTable
from app.tables import TransactionsTable
from app.tables import DepositsTable
from app.tables import WithdrawalsTable

# Imports IotaGo db
from app import db

# Imports flask_login 
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

# Imports model objects
from app.models import tbl_members
from app.models import tbl_assets
from app.models import tbl_asset_types
from app.models import tbl_tags
#from app.models import tbl_tag_types
from app.models import tbl_sensors
from app.models import tbl_sensor_types
#from app.models import tbl_accounts
from app.models import tbl_transactions
#from app.models import tbl_deposits
#from app.models import tbl_withdrawals
from app.models import tbl_transaction_errors


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


### ASSETS MAP (Google Maps) ###

@app.route('/asset_map')
def asset_map():

    assets = (db.session.query(tbl_assets, tbl_asset_types)
        .join(tbl_asset_types)
        .add_columns(tbl_assets.id.label('asset_id'), 
        tbl_assets.name.label('asset_name'), 
        tbl_assets.latitude.label('asset_latitude'), 
        tbl_assets.longitude.label('asset_longitude'), 
        tbl_assets.price.label('asset_price'), 
        tbl_asset_types.name.label('asset_type'))
        )

    my_markers=[]
    for asset in assets:
        marker_data = (asset.asset_latitude, asset.asset_longitude, asset.asset_name, 'http://maps.google.com/mapfiles/ms/icons/green-dot.png')
        my_markers.append(marker_data)

    mymap = Map(
        identifier="mymap",
        #style=(
        #    "height:500px;"
        #    "width:500px;"
        #    "margin:0;"
        #),
        lat=58.252785,
        lng=8.071328,
        markers=my_markers,
        center_on_user_location=True
        )

    return render_template('asset_map.html',title="Asset Map", mymap=mymap)


### DEPOSITS ###

""" # List my deposits
@app.route('/deposits')
def deposits():
    deposits = (db.session.query(tbl_deposits, tbl_accounts)
        .join(tbl_accounts)
        .filter(tbl_deposits.owner == current_user.id)
        .add_columns(tbl_deposits.id.label('deposit_id'), 
        tbl_accounts.id.label('deposit_account_id'), 
        tbl_accounts.name.label('deposit_account_name'), 
        tbl_deposits.value.label('deposit_value'), 
        tbl_deposits.timestamp.label('deposit_timestamp'))
        )
    return render_template("deposits.html",deposits = deposits)

# Create new deposit
@app.route('/new_deposit', methods=['GET', 'POST'])
def new_deposit():

    form = DepositForm()

    # Add user accounts to SelectField
    form.account.choices = [(acc_row.id, acc_row.name) for acc_row in tbl_accounts.query.filter_by(owner=current_user.id)]

    if form.validate_on_submit():
        
        # Add deposit to account balance
        #accounts = tbl_accounts()
        account = tbl_accounts.query.filter_by(id=form.account.data).first_or_404()
        account.balance = account.balance + float(form.value.data)

        # Add deposit to deposit history
        deposit=tbl_deposits()
        deposit.account = form.account.data
        deposit.value = float(form.value.data)
        deposit.owner = current_user.id
        db.session.add(deposit)

        # Commit to database
        db.session.commit()

        flash('New deposit created sucessfully!!')
        return redirect(url_for('deposits'))
    return render_template('deposit.html', title='New deposit', form=form)

### WITHDRAWALS ###

# List my withdrawals
@app.route('/withdrawals')
def withdrawals():
    withdrawals = (db.session.query(tbl_withdrawals, tbl_accounts)
        .join(tbl_accounts)
        .filter(tbl_withdrawals.owner == current_user.id)
        .add_columns(tbl_withdrawals.id.label('withdrawal_id'), 
        tbl_accounts.id.label('withdrawal_account_id'), 
        tbl_accounts.name.label('withdrawal_account_name'), 
        tbl_withdrawals.value.label('withdrawal_value'), 
        tbl_withdrawals.timestamp.label('withdrawal_timestamp'))
        )
    return render_template("withdrawals.html",withdrawals = withdrawals)

# Create new withdrawal
@app.route('/new_withdrawal', methods=['GET', 'POST'])
def new_withdrawal():

    form = WithdrawalForm()

    # Add user accounts to SelectField
    form.account.choices = [(acc_row.id, acc_row.name) for acc_row in tbl_accounts.query.filter_by(owner=current_user.id)]

    if form.validate_on_submit():

        # Add deposit to account balance
        #accounts = tbl_accounts()
        account = tbl_accounts.query.filter_by(id=form.account.data).first_or_404()
        account.balance = account.balance - float(form.value.data)

        # Add deposit to deposit history
        withdrawal=tbl_withdrawals()
        withdrawal.account = form.account.data
        withdrawal.value = float(form.value.data)
        withdrawal.owner = current_user.id
        db.session.add(withdrawal)

        # Commit to database
        db.session.commit()

        flash('New withdrawal created sucessfully!!')
        return redirect(url_for('withdrawals'))
    return render_template('withdrawal.html', title='New withdrawal', form=form)
 """

### TAGS ###

""" # List my tags
@app.route('/tags')
def tags():
    tags = (db.session.query(tbl_tags, tbl_accounts, tbl_tag_types)
        .join(tbl_accounts)
        .join(tbl_tag_types)
        .filter(tbl_tags.owner == current_user.id)
        .add_columns(tbl_tags.id.label('tag_id'), 
        tbl_tags.UID.label('tag_UID'), 
        tbl_tags.name.label('tag_name'), 
        tbl_accounts.id.label('tag_account_id'), 
        tbl_accounts.name.label('tag_account_name'), 
        tbl_tag_types.name.label('tag_type'))
        )
    return render_template("tags.html",tags = tags)

# Show tag details
@app.route('/tag_details/<int:id>')
def tag_details(id):
        
    tag = (db.session.query(tbl_tags, tbl_accounts, tbl_tag_types)
        .join(tbl_accounts, tbl_tags.account == tbl_accounts.id)
        .join(tbl_tag_types, tbl_tags.tag_type == tbl_tag_types.id)
        .join(tbl_members, tbl_tags.owner == tbl_members.id)
        .filter(tbl_tags.id == id)
        .add_columns(tbl_tags.id.label('tag_id'), 
        tbl_tags.created.label('tag_created'), 
        tbl_tags.modified.label('tag_modified'), 
        tbl_tags.name.label('tag_name'), 
        tbl_tags.UID.label('tag_UID'), 
        tbl_accounts.id.label('tag_account_id'), 
        tbl_accounts.name.label('tag_account_name'), 
        tbl_tag_types.name.label('tag_type'), 
        tbl_members.id.label('tag_owner_id'),
        tbl_members.name.label('tag_owner_name'))
        ).one_or_none()

    if tag:
        return render_template("tag_details.html",tag = tag)
    else:
        flash('Tag ID: ' + str(id) + ' does not exist!!')
        return render_template('item_does_not_exist.html', title='Item does not exist!!')


# Save tag function
def save_tag(tag, form, new=False):

    # Check that the Sensor UID is unique and save to db
    UID_tag = tbl_tags.query.filter_by(UID=form.tag_UID.data).first()

    # In case user has not changed UID then its OK to save
    if tag.UID == form.tag_UID.data:
        UID_tag = None

    if UID_tag is None:
        tag.UID = form.tag_UID.data
        tag.KEY = form.tag_KEY.data
        tag.name = form.tag_name.data
        tag.tag_type = form.tag_type.data
        tag.account = form.tag_account.data
        if new:
            # Add the new asset to the database
            tag.owner = current_user.id
            db.session.add(tag)
        else:
            tag.modified = func.now()
        # commit the data to the database
        db.session.commit()
        return True
    else:
        flash('A tag with UID: ' + form.tag_UID.data + ' already exist in the IotaGo database')
        return False

# Create new tag
@app.route('/new_tag', methods=['GET', 'POST'])
def new_tag():

    form = TagForm()
    
    # Add tag types to SelectField
    form.tag_type.choices = [(tagtype_row.id, tagtype_row.name) for tagtype_row in tbl_tag_types.query.all()]

    # Add user accounts to SelectField
    form.tag_account.choices = [(acc_row.id, acc_row.name) for acc_row in tbl_accounts.query.filter_by(owner=current_user.id)]

    if form.validate_on_submit():
        tag = tbl_tags()
        retval = save_tag(tag, form, new=True)
        if retval == True:
            flash('New tag created sucessfully!!')
            return redirect(url_for('tags'))
    return render_template('tag.html', title='New tag', form=form)

# Edit existing tag
@app.route('/edit_tag/<int:id>', methods=['GET', 'POST'])
def edit_tag(id):

    tag = tbl_tags.query.filter_by(id=id).first_or_404()

    if tag:

        if tag.owner == current_user.id:

            form = TagForm()

            # Add tag types to SelectField
            form.tag_type.choices = [(tagtype_row.id, tagtype_row.name) for tagtype_row in tbl_tag_types.query.all()]

            # Add user accounts to SelectField
            form.tag_account.choices = [(acc_row.id, acc_row.name) for acc_row in tbl_accounts.query.filter_by(owner=current_user.id)]

            if form.validate_on_submit():
                retval = save_tag(tag, form)
                if retval == True:
                    flash('Tag updated successfully!')
                    return redirect(url_for('tags'))
            elif request.method == 'GET':
                # Populate form fields here
                form.tag_UID.data = tag.UID
                form.tag_KEY.data = tag.KEY
                form.tag_name.data = tag.name
                form.tag_type.data = tag.tag_type
                form.tag_account.data = tag.account
            return render_template('tag.html', title='Edit tag', form=form)
        else:
            flash('You are not authorized to edit this tag!!')
            return render_template('authorization_error.html', title='Not authorized!!')
    else:
        return 'Error loading #{id}'.format(id=id)    
 """
### ASSETS ###

# List my assets
@app.route('/assets')
def assets():
    assets = (db.session.query(tbl_assets, tbl_asset_types)
        #.join(tbl_accounts)
        .join(tbl_asset_types)
        .filter(tbl_assets.owner == current_user.id)
        .add_columns(tbl_assets.id.label('asset_id'), 
        tbl_assets.name.label('asset_name'), 
        tbl_assets.balance.label('asset_balance'), 
        #tbl_accounts.id.label('asset_account_id'), 
        #tbl_accounts.name.label('asset_account_name'), 
        tbl_asset_types.name.label('asset_type'))
        )
    return render_template("assets.html",assets = assets)

# Show asset details
@app.route('/asset_details/<int:id>')
def asset_details(id):
       
    asset = (db.session.query(tbl_assets, tbl_asset_types)
        .join(tbl_asset_types, tbl_assets.asset_type == tbl_asset_types.id)
        .join(tbl_members, tbl_assets.owner == tbl_members.id)
        .filter(tbl_assets.id == id)
        .add_columns(tbl_assets.id.label('asset_id'), 
        tbl_assets.created.label('asset_created'), 
        tbl_assets.modified.label('asset_modified'), 
        tbl_assets.name.label('asset_name'), 
        tbl_assets.city.label('asset_city'), 
        tbl_assets.country.label('asset_country'), 
        tbl_assets.latitude.label('asset_latitude'), 
        tbl_assets.longitude.label('asset_longitude'), 
        tbl_assets.price.label('asset_price'), 
        #tbl_accounts.id.label('asset_account_id'), 
        #tbl_accounts.name.label('asset_account_name'), 
        tbl_asset_types.name.label('asset_type'), 
        tbl_members.id.label('asset_owner_id'),
        tbl_members.name.label('asset_owner_name'),
        tbl_assets.latitude.label('asset_latitude'),
        tbl_assets.longitude.label('asset_longitude'))
        ).one_or_none()

    if asset:

        my_marker = [(asset.asset_latitude, asset.asset_longitude, asset.asset_name, 'http://maps.google.com/mapfiles/ms/icons/green-dot.png')]

        mymap = Map(
            identifier="mymap",
            #style=(
            #    "height:500px;"
            #    "width:500px;"
            #    "margin:0;"
            #),
            lat=asset.asset_latitude,
            lng=asset.asset_longitude,
            markers=my_marker,
            center_on_user_location=False
            )
        return render_template("asset_details.html",asset = asset, mymap = mymap)
    else:
        flash('Asset ID: ' + str(id) + ' does not exist!!')
        return render_template('item_does_not_exist.html', title='Item does not exist!!')


# Save asset function
def save_asset(asset, form, new=False):
    asset.name = form.asset_name.data
    asset.KEY = form.asset_KEY.data
    asset.city = form.asset_city.data
    asset.country = form.asset_country.data
    asset.latitude = form.asset_latitude.data
    asset.longitude = form.asset_longitude.data
    asset.price = form.asset_price.data
    asset.asset_type = form.asset_type.data
    #asset.account = form.asset_account.data
    if new:
        # Add the new asset to the database
        asset.owner = current_user.id
        asset.balance = 0.0
        db.session.add(asset)
    else:
        asset.modified = func.now()
    # commit the data to the database
    db.session.commit()

# Create new asset
@app.route('/new_asset', methods=['GET', 'POST'])
def new_asset():

    form = AssetForm()
    
    # Add asset types to SelectField
    form.asset_type.choices = [(asstype_row.id, asstype_row.name) for asstype_row in tbl_asset_types.query.all()]

    # Add user accounts to SelectField
    #form.asset_account.choices = [(acc_row.id, acc_row.name) for acc_row in tbl_accounts.query.filter_by(owner=current_user.id)]

    if form.validate_on_submit():
        asset = tbl_assets()
        save_asset(asset, form, new=True)
        flash('New asset created sucessfully!!')
        return redirect(url_for('assets'))
    return render_template('asset.html', title='New asset', form=form)

# Edit existing asset
@app.route('/edit_asset/<int:id>', methods=['GET', 'POST'])
def edit_asset(id):

    asset = tbl_assets.query.filter_by(id=id).first_or_404()

    if asset:

        # Check ownership
        if asset.owner == current_user.id:

            form = AssetForm()

            # Add asset types to SelectField
            form.asset_type.choices = [(asstype_row.id, asstype_row.name) for asstype_row in tbl_asset_types.query.all()]

            # Add user accounts to SelectField
            #form.asset_account.choices = [(acc_row.id, acc_row.name) for acc_row in tbl_accounts.query.filter_by(owner=current_user.id)]

            if form.validate_on_submit():
                save_asset(asset, form)
                flash('Asset updated successfully!')
                return redirect(url_for('assets'))
            elif request.method == 'GET':
                # Populate form fields here
                form.asset_name.data = asset.name
                form.asset_KEY.data = asset.KEY
                form.asset_city.data = asset.city
                form.asset_country.data = asset.country
                form.asset_latitude.data = asset.latitude
                form.asset_longitude.data = asset.longitude
                form.asset_price.data = asset.price
                form.asset_type.data = asset.asset_type
                #form.asset_account.data = asset.account

            return render_template('asset.html', title='Edit asset', form=form)

        else:
            flash('You are not authorized to edit this asset!!')
            return render_template('authorization_error.html', title='Not authorized!!')
            
    else:
        return 'Error loading #{id}'.format(id=id)


### SENSORS ###

# List my sensors
@app.route('/sensors')
def sensors():
    sensors = (db.session.query(tbl_sensors, tbl_sensor_types, tbl_assets)
        .join(tbl_sensor_types)
        .join(tbl_assets)
        .filter(tbl_sensors.owner == current_user.id)
        .add_columns(tbl_sensors.id.label('sensor_id'), 
        tbl_sensors.name.label('sensor_name'), 
        tbl_sensor_types.name.label('sensor_type'), 
        tbl_sensors.UID.label('sensor_UID'), 
        tbl_assets.id.label('sensor_asset_id'), 
        tbl_assets.name.label('sensor_asset_name'))
        )
    return render_template("sensors.html",sensors = sensors)

# Show sensor details
@app.route('/sensor_details/<int:id>')
def sensor_details(id):
       
    sensor = (db.session.query(tbl_sensors, tbl_sensor_types, tbl_assets)
        .join(tbl_assets, tbl_sensors.parent_asset == tbl_assets.id)
        .join(tbl_sensor_types, tbl_sensors.sensor_type == tbl_sensor_types.id)
        .join(tbl_members, tbl_sensors.owner == tbl_members.id)
        .filter(tbl_sensors.id == id)
        .add_columns(tbl_sensors.id.label('sensor_id'), 
        tbl_sensors.created.label('sensor_created'), 
        tbl_sensors.modified.label('sensor_modified'), 
        tbl_sensors.name.label('sensor_name'), 
        tbl_sensors.UID.label('sensor_UID'), 
        tbl_sensor_types.name.label('sensor_type'), 
        tbl_assets.id.label('parent_asset_id'), 
        tbl_assets.name.label('parent_asset_name'), 
        tbl_members.id.label('sensor_owner_id'),
        tbl_members.name.label('sensor_owner_name'))
        ).one_or_none()

    if sensor:
        return render_template("sensor_details.html",sensor = sensor)
    else:
        flash('Sensor ID: ' + str(id) + ' does not exist!!')
        return render_template('item_does_not_exist.html', title='Item does not exist!!')

# Save sensor function
def save_sensor(sensor, form, new=False):

    # Check that the Sensor UID is unique and save to db
    UID_sensor = tbl_sensors.query.filter_by(UID=form.sensor_UID.data).first()

    # In case user has not changed UID then its OK to save
    if sensor.UID == form.sensor_UID.data:
        UID_sensor = None

    if UID_sensor is None:
        sensor.UID = form.sensor_UID.data
        sensor.name = form.sensor_name.data
        sensor.sensor_type = form.sensor_type.data
        sensor.parent_asset = form.parent_asset.data
        if new:
            # Add the new sensor to the database
            sensor.owner = current_user.id
            db.session.add(sensor)
        else:
            sensor.modified = func.now()
        # commit the data to the database
        db.session.commit()
        return True
    else:
        flash('A sensor with UID: ' + form.sensor_UID.data + ' already exist in the IotaGo database')
        return False

# Create new sensor
@app.route('/new_sensor', methods=['GET', 'POST'])
def new_sensor():

    form = SensorForm()
    
    # Add sensor types to SelectField
    form.sensor_type.choices = [(senstype_row.id, senstype_row.name) for senstype_row in tbl_sensor_types.query.all()]

    # Add user assets to SelectField
    form.parent_asset.choices = [(parass_row.id, parass_row.name) for parass_row in tbl_assets.query.filter_by(owner=current_user.id)]

    if form.validate_on_submit():
        sensor = tbl_sensors()
        retval = save_sensor(sensor, form, new=True)
        if retval == True:
            flash('New sensor created sucessfully!!')
            return redirect(url_for('sensors'))
    return render_template('sensor.html', title='New sensor', form=form)

# Edit existing sensor
@app.route('/edit_sensor/<int:id>', methods=['GET', 'POST'])
def edit_sensor(id):
    sensor = tbl_sensors.query.filter_by(id=id).first_or_404()
    if sensor:

        if sensor.owner == current_user.id:

            form = SensorForm()

            # Add sensor types to SelectField
            form.sensor_type.choices = [(senstype_row.id, senstype_row.name) for senstype_row in tbl_sensor_types.query.all()]

            # Add user assets to SelectField
            form.parent_asset.choices = [(parass_row.id, parass_row.name) for parass_row in tbl_assets.query.filter_by(owner=current_user.id)]

            if form.validate_on_submit():
                retval = save_sensor(sensor, form)
                if retval == True:
                    flash('Sensor updated successfully!')
                    return redirect(url_for('sensors'))
            elif request.method == 'GET':
                # Populate form fields here
                form.sensor_UID.data = sensor.UID
                form.sensor_name.data = sensor.name
                form.sensor_type.data = sensor.sensor_type
                form.parent_asset.data = sensor.parent_asset

            return render_template('sensor.html', title='Edit sensor', form=form)
        else:
            flash('You are not authorized to edit this sensor!!')
            return render_template('authorization_error.html', title='Not authorized!!')

    else:
        return 'Error loading #{id}'.format(id=id)


### ACCOUNTS ###

""" # List my accounts
@app.route('/accounts')
def accounts():
    accounts = (db.session.query(tbl_accounts)
    .filter(tbl_accounts.owner == current_user.id)
    .add_columns(tbl_accounts.id.label('account_id'), 
    tbl_accounts.name.label('account_name'), 
    tbl_accounts.balance.label('account_balance'))
    )
    return render_template("accounts.html",accounts = accounts)

# Show account details
@app.route('/account_details/<int:id>')
def account_details(id):
    
    account = (db.session.query(tbl_accounts, tbl_members)
        .join(tbl_members, tbl_accounts.owner == tbl_members.id)
        .filter(tbl_accounts.id == id)
        .add_columns(tbl_accounts.id.label('account_id'), 
        tbl_accounts.created.label('account_created'), 
        tbl_accounts.modified.label('account_modified'), 
        tbl_accounts.name.label('account_name'), 
        tbl_accounts.balance.label('account_balance'), 
        tbl_members.id.label('account_owner_id'), 
        tbl_members.name.label('account_owner_name')) 
        ).one_or_none()

    if account:
        if account.account_owner_id == current_user.id:
            return render_template("account_details.html",account = account)
        else:
            flash('You are not authorized to view this account!!')
            return render_template('authorization_error.html', title='Not authorized!!')
    else:
        # no account with this ID
        flash('Account ID: ' + str(id) + ' does not exist!!')
        return render_template('item_does_not_exist.html', title='Item does not exist!!')

# Save account function
def save_account(account, form, new=False):
    account.name = form.account_name.data
    if new:
        # Add the new account to the database
        account.balance = 0
        account.owner = current_user.id
        db.session.add(account)
    else:
        account.modified = func.now()
    # commit the data to the database
    db.session.commit()

# Create new account
@app.route('/new_account', methods=['GET', 'POST'])
def new_account():
    form = AccountForm()  
    if form.validate_on_submit():
        account = tbl_accounts()
        save_account(account, form, new=True)
        flash('New account created sucessfully!!')
        return redirect(url_for('accounts'))
    return render_template('account.html', title='New account', form=form)

# Edit existing account
@app.route('/edit_account/<int:id>', methods=['GET', 'POST'])
def edit_account(id):
    account = tbl_accounts.query.filter_by(id=id).first_or_404()
    if account:
        if account.owner == current_user.id:
            form = AccountForm()
            if form.validate_on_submit():
                save_account(account, form)
                flash('Account updated successfully!')
                return redirect(url_for('accounts'))
            elif request.method == 'GET':
                # Populate form fields here
                form.account_name.data = account.name
            return render_template('account.html', title='Edit account', form=form)
        else:
            flash('You are not authorized to edit this account!!')
            return render_template('authorization_error.html', title='Not authorized!!')
    else:
        return 'Error loading #{id}'.format(id=id)
 """
### TRANSACTIONS ###

# List my transactions
@app.route('/transactions')
def transactions():
    transactions = (db.session.query(tbl_transactions, tbl_tags, tbl_assets)
        .join(tbl_tags)
        .join(tbl_assets)
        .filter((tbl_tags.owner == current_user.id) | (tbl_assets.owner == current_user.id))
        .add_columns(tbl_transactions.id.label('transaction_id'), 
        tbl_tags.id.label('tag_id'), 
        tbl_tags.name.label('tag_name'), 
        tbl_assets.id.label('asset_id'), 
        tbl_assets.name.label('asset_name'), 
        tbl_transactions.timestamp.label('transaction_timestamp'), 
        tbl_transactions.transaction_value.label('transaction_value'))
        )
    return render_template("transactions.html",transactions = transactions)



@app.route('/member_details/<int:id>')
def member_details(id):
    
    member = (db.session.query(tbl_members)
        .filter(tbl_members.id == id)
        .add_columns(tbl_members.id.label('member_id'), 
        tbl_members.created.label('member_created'), 
        tbl_members.modified.label('member_modified'), 
        tbl_members.name.label('member_name'), 
        tbl_members.email.label('member_email'), 
        tbl_members.phone.label('member_phone')) 
        ).one()
    return render_template("member_details.html",member = member)



@app.route('/members')
def members():
    members = tbl_members.query.all()
    table = MembersTable(members)
    table.border = True
    return render_template("members.html",table = table)
