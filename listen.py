
from datetime import date, datetime

# import paho.mqtt.client as mqtt

from sqlalchemy.sql import func

from app import db

from app.models import tbl_members
from app.models import tbl_assets
from app.models import tbl_asset_types
from app.models import tbl_tags
from app.models import tbl_tag_types
from app.models import tbl_sensors
from app.models import tbl_sensor_types
from app.models import tbl_accounts
from app.models import tbl_transactions
from app.models import tbl_deposits
from app.models import tbl_withdrawals
from app.models import tbl_transaction_errors

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # Decode and split MQTT payload into tag_ID and asset_ID
    tag_UID, sensor_UID = msg.payload.decode("utf-8").split(",")

    # Get tag ID from DB
    tag_id = GetTagData(tag_UID)
    sensor_id = GetSensorData(sensor_UID)
    
    save_trans(tag_id,sensor_id,100)

    print('new transaction added')

def new_trans_error(mqtt_msg, error_desc):
    trans_error = tbl_transaction_errors()
    trans_error.mqtt_msg = mqtt_msg
    trans_error.error_desc = error_desc
    db.session.add(trans_error)
    db.session.commit()

def new_trans(mqtt_msg):

    # Check for valid mqtt message syntax
    mqtt_split = mqtt_msg.split(",")
    if len(mqtt_split) == 3:
        mqtt_tag_UID = mqtt_split[0]
        mqtt_tag_KEY = mqtt_split[1]
        mqtt_sensor_UID = mqtt_split[2]
    else:
        new_trans_error(mqtt_msg, 'Invalid mqtt syntax')
        return

    # Get tag data from DB
    tag = (db.session.query(tbl_tags, tbl_accounts)
        .join(tbl_accounts)
        .filter(tbl_tags.UID == mqtt_tag_UID)
        .add_columns(tbl_tags.id.label('tag_id'), tbl_tags.KEY.label('tag_KEY'), tbl_accounts.id.label('tag_account_id'), tbl_accounts.balance.label('tag_account_balance'))
        .first())

    if tag is None:

        new_trans_error(mqtt_msg, 'Tag UID not found')
        return

    # Get sensor data from DB
    sensor = (db.session.query(tbl_sensors, tbl_assets, tbl_accounts)
        .join(tbl_assets, tbl_sensors.parent_asset == tbl_assets.id)
        .join(tbl_accounts)
        .filter(tbl_sensors.UID == mqtt_sensor_UID)
        .add_columns(tbl_sensors.id.label('sensor_id'), tbl_assets.id.label('asset_id'), tbl_accounts.id.label('asset_account_id'), tbl_accounts.balance.label('asset_account_balance'), tbl_assets.price.label('asset_price'))
        .first())

    if sensor is None:

        new_trans_error(mqtt_msg, 'Sensor UID not found')
        return

    # Check for valid KEY
    if mqtt_tag_KEY != tag.tag_KEY:
        new_trans_error(mqtt_msg, 'Invalid KEY')
        return

    # Get accounts
    sender_account = tbl_accounts.query.filter_by(id=tag.tag_account_id).first_or_404()
    reciever_account = tbl_accounts.query.filter_by(id=sensor.asset_account_id).first_or_404()

    # If sufficient funds, perform token transfer
    if  sender_account.balance < float(sensor.asset_price):
        new_trans_error(mqtt_msg, 'Insufficient funding')
        return
    else:
        sender_account.balance = sender_account.balance - float(sensor.asset_price)
        reciever_account.balance = reciever_account.balance + float(sensor.asset_price)

    # Add new transaction to the transactions table
    trans = tbl_transactions()
    trans.tag_id = tag.tag_id
    trans.tag_account_id = tag.tag_account_id
    trans.sensor_id = sensor.sensor_id
    trans.asset_id = sensor.asset_id
    trans.asset_account_id = sensor.asset_account_id
    trans.timestamp = func.now()
    trans.transaction_value = sensor.asset_price
    db.session.add(trans)

    # Commit new transaction to DB
    db.session.commit()


# Syntax: TAG_UID,TAG_KEY,SENSOR_UID
mqtt_msg = 'NO XXX,MYKEY,CAM10'

new_trans(mqtt_msg)
