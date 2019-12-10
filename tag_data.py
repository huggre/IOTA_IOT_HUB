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
#from app.models import tbl_sensors
#from app.models import tbl_sensor_types
#from app.models import tbl_accounts
from app.models import tbl_transactions
#from app.models import tbl_deposits
#from app.models import tbl_withdrawals
from app.models import tbl_transaction_errors
from app.models import tbl_asset_tags
from app.models import tbl_asset_sensors

assetID = 1
tagUID = 'T2'

""" tag = (db.session.query(tbl_tags)
    .filter(tbl_tags.tag_UID == tagUID)
    .add_columns(tbl_tags.description.label('tag_description'))
    ).one()

print(tag.tag_description)
#return render_template("member_details.html",member = member) """

asset_tag = (db.session.query(tbl_asset_tags)
    .filter(tbl_asset_tags.tag_UID == tagUID, tbl_asset_tags.asset_id == assetID)
    .add_columns(tbl_asset_tags.asset_tag_balance.label('asset_tag_balance'))
    ).one()

print(asset_tag.asset_tag_balance)