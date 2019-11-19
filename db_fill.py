from app import db
from app.models import tbl_members
from app.models import tbl_sensor_types
#from app.models import tbl_sensor_models
from app.models import tbl_sensors
from app.models import tbl_accounts
from app.models import tbl_assets
from app.models import tbl_tags
from app.models import tbl_transactions

# Add member
def add_member(tbl_members):
    #mem = tbl_members(name='Stine', email='stine@example.com', password_hash='STINE_HASH')
    mem = tbl_members(name='Stine2', email='stine2@example.com')
    mem.set_password("cat")
    db.session.add(mem)
    db.session.commit()

# Add sensor type
def add_sensor_type(tbl_sensor_types):
    sens_type = tbl_sensor_types(name='Generic RFID Reader')
    db.session.add(sens_type)
    db.session.commit()

# Add sensor model
def add_sensor_model(tbl_sensor_types,tbl_sensor_models):
    sens_type = tbl_sensor_types.query.get(1)
    sens_model = tbl_sensor_models(sensor_model_name='MFRC522', sensor_type=sens_type)
    db.session.add(sens_model)
    db.session.commit()

# Add sensor
def add_sensor(tbl_sensor_types,tbl_assets,tbl_members):
    sens_type = tbl_sensor_types.query.get(1)
    mem = tbl_members.query.get(1)
    par_asset = tbl_assets = tbl_assets.query.get(1)
    #sens = tbl_sensors(UID="HHHHH", name='Stine Sensor', stype=sens_type, sensor_asset=par_asset, member=mem)
    sens = tbl_sensors(UID="HHHHH", name='Stine Sensor', stype=sens_type, member=mem)
    db.session.add(sens)
    db.session.commit()

# Add Account
def add_account(tbl_accounts,tbl_members):
    mem = tbl_members.query.get(1)
    acc = tbl_accounts(name='STINE ACCOUNT', balance=200, member=mem)
    db.session.add(acc)
    db.session.commit()

# Add Asset
def add_asset(tbl_assets,tbl_members, tbl_accounts, tbl_sensors):
    mem = tbl_members.query.get(1)
    acc = tbl_accounts.query.get(1)
    ass = tbl_assets(name='Stine Asset', price=500, asset_account=acc, member=mem)
    db.session.add(ass)
    db.session.commit()

# Add Tag
def add_tag(tbl_tags,tbl_members, tbl_accounts):
    mem = tbl_members.query.get(1)
    acc = tbl_accounts.query.get(1)
    tag = tbl_tags(UID='FR BD CC RP', name='Stine Tag', tag_account=acc, member=mem)
    db.session.add(tag)
    db.session.commit()

# Add Transaction
def add_transaction(tbl_transactions, tbl_tags, tbl_sensors):
    sens = tbl_sensors.query.get(1)
    tag = tbl_tags.query.get(1)
    trans = tbl_transactions(trans_sensor_id=sens,trans_tag_id=tag,value=10)
    db.session.add(trans)
    db.session.commit()

choice ='0'
while choice =='0':
    print("1. add member")
    print("2. add sensor type")
    print("3. add sensor model")
    print("4. add sensor")
    print("5. add account")
    print("6. add asset")
    print("7. add tag")
    print("8. add transaction")

    choice = input ("Please make a choice: ")

    if choice == "1":
        add_member(tbl_members)
    elif choice == "2":
        add_sensor_type(tbl_sensor_types)
    elif choice == "3":
        add_sensor_model(tbl_sensor_types,tbl_sensor_models)
    elif choice == "4":
        add_sensor(tbl_sensor_types,tbl_assets,tbl_members)
    elif choice == "5":
        add_account(tbl_accounts,tbl_members)
    elif choice == "6":
        add_asset(tbl_assets,tbl_members, tbl_accounts, tbl_sensors)
    elif choice == "7":
        add_tag(tbl_tags,tbl_members, tbl_accounts)
    elif choice == "8":
        add_transaction(tbl_transactions, tbl_tags, tbl_sensors)

