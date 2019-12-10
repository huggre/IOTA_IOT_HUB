import os
clear = lambda: os.system('cls')

from sqlalchemy.sql import func

from app import db


from datetime import date, datetime

# import paho.mqtt.client as mqtt

from app.models import tbl_members
from app.models import tbl_assets
from app.models import tbl_asset_types
from app.models import tbl_tags
from app.models import tbl_tag_types
from app.models import tbl_sensors
from app.models import tbl_sensor_types
#from app.models import tbl_accounts
from app.models import tbl_transactions
#from app.models import tbl_deposits
#from app.models import tbl_withdrawals
from app.models import tbl_transaction_errors
from app.models import tbl_asset_tags
#from app.models import tbl_asset_sensors

def add_sensortype(sensor_type_name):

    sensor_type = tbl_sensor_types()
    sensor_type.name = sensor_type_name 

    db.session.add(sensor_type)

    # Commit tagtype to DB
    db.session.commit()

    print("\n Sensor Type: " + sensor_type_name + " added to DB")

def add_assettype(asset_type_name):

    asset_type = tbl_asset_types()
    asset_type.name = asset_type_name 

    db.session.add(asset_type)

    # Commit tagtype to DB
    db.session.commit()

    print("\n Asset Type: " + asset_type_name + " added to DB")

def register_tag(tag_UID, tag_name, tag_type, tag_owner):

    # Check if tag UID already exist
    tag = (db.session.query(tbl_tags)
        .filter(tbl_tags.tag_UID == tag_UID)
        .add_columns(tbl_tags.tag_UID.label('tag_UID'))
        .first())

    if tag is None:
        tag = tbl_tags()
        tag.tag_UID = tag_UID
        tag.name = tag_name
        tag.tag_type = tag_type
        tag.owner = tag_owner
        db.session.add(tag)

        # Commit new transaction to DB
        db.session.commit()

        print("Tag sucessfully created")

    else:
        print("Tag UID already exist")

def assign_tag(tag_UID, assetID):

    # Get tag_id based on tag_UID
    tag = (db.session.query(tbl_tags)
        .filter(tbl_tags.tag_UID == tag_UID)
        .add_columns(tbl_tags.id.label('tag_id'))
        .first())

    tag_id = tag.tag_id

    # Check if tag is allready assigned to asset

    # Assign tag to Asset
    asset_tag = tbl_asset_tags()
    asset_tag.asset_id = assetID
    asset_tag.tag_id = tag_id
    asset_tag.asset_tag_balance = 0.0
    db.session.add(asset_tag)
    db.session.commit()

    print("Done")

def register_sensor(sensor_UID, assetID, sensor_type, sensor_name, sensor_owner):

    # Create and assign sensor to asset
    sensor = tbl_sensors()
    sensor.sensor_UID = sensor_UID
    sensor.name = sensor_name
    sensor.sensor_type = sensor_type
    sensor.owner = sensor_owner
    sensor.parent_asset = assetID
    db.session.add(sensor)
    db.session.commit()

def add_transaction(sensor_UID, tag_UID, trans_type, value):

    # Get sensor and asset id from sensor_UID
    sensor = (db.session.query(tbl_sensors)
        .filter(tbl_sensors.sensor_UID == sensor_UID)
        .add_columns(tbl_sensors.id.label('sensor_id'),
        tbl_sensors.parent_asset.label('parent_asset_id'))
        .first())
    
    sensor_id = sensor.sensor_id
    asset_id = sensor.parent_asset_id

    # Get tag_id based on tag_UID
    tag = (db.session.query(tbl_tags)
        .filter(tbl_tags.tag_UID == tag_UID)
        .add_columns(tbl_tags.id.label('tag_id'))
        .first())

    tag_id = tag.tag_id
    
    # Add new transaction to the transactions table
    trans = tbl_transactions()
    trans.tag_id = tag_id
    trans.sensor_id = sensor_id
    trans.asset_id = asset_id
    trans.transaction_type_id = trans_type
    trans.transaction_value = value

    # Perform value transaction
    

    db.session.add(trans)

    # Commit new transaction to DB
    db.session.commit()



clear()

print("""

The db_init.py tools helps you add new tag, sensor and asset types to the IotaGo database.

Common tag types are: RFID Tag etc.
Common sensor types are: RFID Reader etc.
Common asset types are: Parking Lot, Sports Venue etc.

""")

sensor_UID = 'SENSUID'
assetID = 1
sensorID = 3
sensor_type = 1
tag_owner = 1
sensor_owner = 1

ans=True
while ans:
    print ("""
    1.Register Sensor
    2.Register Tag
    3.Assign Tag to Asset
    4.Deposit
    5.Exit/Quit
    """)
    ans=input("What would you like to do? ") 
    if ans=="1":
        sensor_UID = input("\n Specify Sensor UID:")
        sensor_name = input("\n Specify Sensor Name:")
        register_sensor(sensor_UID, assetID, sensor_type, sensor_name, sensor_owner)
    elif ans=="2":
        tag_UID = input("\n Specify Tag UID:")
        tag_name = input("\n Specify Tag Name:")
        tag_type = input("\n Specify Tag Type")
        if tag_name == "":
            tag_name = "None"
        register_tag(tag_UID, tag_name, tag_type, tag_owner)
    elif ans=="3":
        tag_UID = input("\n Specify Tag UID:")
        assign_tag(tag_UID, assetID)
    elif ans=="4":
        sensor_UID = input("\n Specify Sensor UID:")
        tag_UID = input("\n Specify Tag UID:")
        trans_type = 1
        value = input("\n Specify Value:")
        add_transaction(sensor_UID, tag_UID, trans_type, value)
    elif ans=="5":
      exit()
    elif ans !="":
      print("\n Not Valid Choice Try again") 