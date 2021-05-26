from requests import post
import json

from app import db

from app.models import tbl_assets
from app.models import tbl_endpoints
from app.models import tbl_services


payment_address = 'ADDRRRRR'

# Get required data from DB
asset = (db.session.query(tbl_assets, tbl_endpoints, tbl_services)
    .join(tbl_endpoints)
    .join(tbl_services)
    .filter(tbl_assets.payment_address == payment_address)
    .add_columns(tbl_assets.service_data.label('service_data'),
    tbl_endpoints.endpoint.label('endpoint'),
    tbl_endpoints.token.label('token'),
    tbl_services.tech_name.label('tech_name')
    )
    .first())

tech_name_list = asset.tech_name.split(".")

url = asset.endpoint + '/api/services/' + tech_name_list[0] + '/' + tech_name_list[1]

headers = {
    "Authorization": "Bearer " + asset.token,
    "content-type": "application/json",
}

response = post(url, headers=headers, data=asset.service_data)

print("Rest API Response\n")
print(response.text)
print(response.status_code)
