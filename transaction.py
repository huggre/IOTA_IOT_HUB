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
#from app.models import tbl_tag_types
from app.models import tbl_sensors
#from app.models import tbl_sensor_types
#from app.models import tbl_accounts
from app.models import tbl_transactions
#from app.models import tbl_deposits
#from app.models import tbl_withdrawals
from app.models import tbl_transaction_errors
from app.models import tbl_asset_tags
from app.models import tbl_asset_sensors

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

def register_tag(tag_UID, assetID, tag_description):
    # Check if tag UID already exist
    tag = (db.session.query(tbl_tags)
        .filter(tbl_tags.tag_UID == tag_UID)
        .add_columns(tbl_tags.tag_UID.label('tag_UID'))
        .first())

    if tag is None:
        tag = tbl_tags()
        tag.tag_UID = tag_UID
        db.session.add(tag)

        # Commit new transaction to DB
        db.session.commit()

        print("Tag sucessfully created")

    else:
        print("Tag UID already exist")

    # Assign tag to Asset
    asset_tag = tbl_asset_tags()
    asset_tag.asset_id = assetID
    asset_tag.tag_UID = tag_UID
    asset_tag.description = tag_description
    asset_tag.asset_tag_balance = 0.0
    db.session.add(asset_tag)
    db.session.commit()

def register_sensor(sensor_UID, assetID, sensor_description):
    # Check if tag UID already exist
    sensor = (db.session.query(tbl_sensors)
        .filter(tbl_sensors.sensor_UID == sensor_UID)
        .add_columns(tbl_sensors.sensor_UID.label('sensor_UID'))
        .first())

    if sensor is None:
        sensor = tbl_sensors()
        sensor.sensor_UID = sensor_UID
        db.session.add(sensor)

        # Commit new transaction to DB
        db.session.commit()

        print("Sensor sucessfully created")

    else:
        print("Sensor UID already exist")

    # Assign sensor to Asset
    asset_sensor = tbl_asset_sensors()
    asset_sensor.asset_id = assetID
    asset_sensor.sensor_UID = sensor_UID
    asset_sensor.description = sensor_description
    db.session.add(asset_sensor)
    db.session.commit()

def add_transaction(sensor_UID, tag_UID, assetID, trans_type, value):
    
    # Add new transaction to the transactions table
    trans = tbl_transactions()
    trans.tag_UID = tag_UID
    trans.sensor_UID = sensor_UID
    trans.asset_id = assetID
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

sensor_UID = 'SENS2'
assetID = 1

ans=True
while ans:
    print ("""
    0.Register Sensor
    1.Register Tag
    2.Deposit
    3.Exit/Quit
    """)
    ans=input("What would you like to do? ") 
    if ans=="0":
        sensor_UID = input("\n Specify Sensor UID:")
        sensor_description = input("\n Specify Sensor Description:")
        register_sensor(sensor_UID, assetID, sensor_description)
    elif ans=="1":
        tag_UID = input("\n Specify Tag UID:")
        tag_description = input("\n Specify Tag Description:")
        register_tag(tag_UID, assetID, tag_description)
    elif ans=="2":
        #sensor_UID = input("\n Specify Sensor UID:")
        tag_UID = input("\n Specify Tag UID:")
        trans_type = 1
        value = input("\n Specify Value:")
        add_transaction(sensor_UID, tag_UID, assetID, trans_type, value)
    elif ans=="3":
      exit()
    elif ans !="":
      print("\n Not Valid Choice Try again") 