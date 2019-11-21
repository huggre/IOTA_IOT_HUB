
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
    if len(mqtt_split) == 2:
        mqtt_tag_UID = mqtt_split[0]
        mqtt_sensor_UID = mqtt_split[1]
    else:
        new_trans_error(mqtt_msg, 'Invalid mqtt syntax')
        return

    # Get tag data from DB
    tags = (db.session.query(tbl_tags, tbl_accounts)
        .join(tbl_accounts)
        .filter(tbl_tags.UID == mqtt_tag_UID)
        .add_columns(tbl_tags.id.label('tag_id'), tbl_accounts.id.label('tag_account_id'), tbl_accounts.balance.label('tag_account_balance'))
        .first())

    if tags:
        # Assign tag values
        tag_id = tags.tag_id
        tag_account_id = tags.tag_account_id
        tag_account_balance = tags.tag_account_balance
    else:
        new_trans_error(mqtt_msg, 'Tag UID not found')
        return


    # Get sensor data from DB
    sensors = (db.session.query(tbl_sensors, tbl_assets, tbl_accounts)
        .join(tbl_assets, tbl_sensors.parent_asset == tbl_assets.id)
        .join(tbl_accounts)
        .filter(tbl_sensors.UID == mqtt_sensor_UID)
        .add_columns(tbl_sensors.id.label('sensor_id'), tbl_assets.id.label('asset_id'), tbl_accounts.id.label('asset_account_id'), tbl_accounts.balance.label('asset_account_balance'), tbl_assets.price.label('asset_price'))
        .first())

    if sensors:
        # Assign sensor values
        sensor_id = sensors.sensor_id
        asset_id = sensors.asset_id
        asset_account_id = sensors.asset_account_id
        asset_account_balance = sensors.asset_account_balance
        asset_price = sensors.asset_price
    else:
        new_trans_error(mqtt_msg, 'Sensor UID not found')
        return

    # Check that there is enough funds to pay for the transaction
    if tag_account_balance < asset_price:
        valid_trans = False
        new_trans_error(mqtt_msg, 'Insufficient funding')
        return

    # Subtract transaction value from tag account
    sender_account = tbl_accounts.query.filter_by(id=tag_account_id).first_or_404()
    sender_account.balance = sender_account.balance - asset_price

    # Add transaction value to asset account
    reciever_account = tbl_accounts.query.filter_by(id=asset_account_id).first_or_404()
    reciever_account.balance = reciever_account.balance + asset_price

    # Add new transaction to the transactions table
    trans = tbl_transactions()
    trans.tag_id = tag_id
    trans.tag_account_id = tag_account_id
    trans.sensor_id = sensor_id
    trans.asset_id = asset_id
    trans.asset_account_id = asset_account_id
    trans.timestamp = func.now()
    trans.transaction_value = asset_price
    db.session.add(trans)

    # Commit new transaction to DB
    db.session.commit()


# Syntax: TAG_UID, SENSOR_UID
mqtt_msg = 'NO XXX,CAM10'

new_trans(mqtt_msg)

#trans = tbl_transactions()
#trans.mqtt_tag_UID = "NO 1234567"
#trans.mqtt_sensor_UID = "CCC"
#trans.tag_id = 3
#trans.tag_account_id = 4
#trans.sensor_id = 3
#trans.asset_id = 4
#trans.asset_account_id = 4
#trans.timestamp = func.now()
#trans.transaction_value = 10
#db.session.add(trans)

#db.session.commit()

#client = mqtt.Client()
#client.on_connect = on_connect
#client.on_message = on_message
#client.connect("145.14.157.62", 1883, 60)
#client.loop_forever()