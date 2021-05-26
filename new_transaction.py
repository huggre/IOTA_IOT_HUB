import datetime

from app import db

from app.models import tbl_assets
from app.models import tbl_endpoints
from app.models import tbl_services
from app.models import tbl_transactions
from app.models import tbl_settlements


from app.ha_interact import call_ha_service

def add_settlement(payment_address, recieve_address, value):
    settlement = tbl_settlements()
    settlement.payment_address=payment_address
    settlement.recieve_address=recieve_address
    settlement.value=value
    db.session.add(settlement)
    db.session.commit()

    return settlement.id


def add_transaction(asset, status, message_id, payment_address, recieve_address, value):
    transaction = tbl_transactions()
    transaction.asset = asset
    transaction.status = status
    transaction.message_id = message_id
    transaction.settlement = add_settlement(payment_address, recieve_address, value)

    db.session.add(transaction)
    db.session.commit()



# Get inbound transaction data
message_id = 'XXX'
customer_address = 'get from wallet' # customer from address
payment_address = 'xtoi1qzt0nhsf38nh6rs4p6zs5knqp6psgha9wsv74uajqgjmwc75ugupx3y7x0r' # iotago recieve address
value = 1000001

# get asset data from payment address
asset = (db.session.query(tbl_assets, tbl_endpoints, tbl_services)
    .join(tbl_endpoints)
    .join(tbl_services)
    .filter(tbl_assets.payment_address == payment_address)
    .add_columns(tbl_assets.id.label('id'), 
    tbl_assets.price.label('price'),
    tbl_assets.recieve_address.label('recieve_address'),
    tbl_endpoints.endpoint.label('endpoint'),
    tbl_endpoints.token.label('token'),
    tbl_services.tech_name.label('tech_name'),
    tbl_assets.service_data.label('service_data'))
    ).one_or_none()

# Check if asset exist
if asset == None:
    # Asset was not found, return payment with error
    add_transaction(None, 1, message_id, payment_address, customer_address, value)
    quit()

# Check value = price
if value != asset.price*1000000:
    # Recived amount does not match price, return payment with error
    add_transaction(asset.id, 2, message_id, payment_address, customer_address, value)
    quit()

# Call Home Assistant service
response = call_ha_service(asset.endpoint, asset.token, asset.tech_name, asset.service_data)
print(response.text)

# All is good, forward payment to asset owner
add_transaction(asset.id, 0, message_id, payment_address, asset.recieve_address, value)
