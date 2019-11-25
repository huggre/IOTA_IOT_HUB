import os
clear = lambda: os.system('cls')

from sqlalchemy.sql import func

from app import db

from app.models import tbl_sensor_types
from app.models import tbl_asset_types

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


clear()

print("""

The db_init.py tools helps you add new tag, sensor and asset types to the IotaGo database.

Common tag types are: RFID Tag etc.
Common sensor types are: RFID Reader etc.
Common asset types are: Parking Lot, Sports Venue etc.

""")

ans=True
while ans:
    print ("""
    2.Add Sensor Type
    3.Add Asset Type
    4.Exit/Quit
    """)
    ans=input("What would you like to do? ") 
    if ans=="1":
        sensor_type_name = input("\n Specify Sensor Type Name:")
        add_sensortype(sensor_type_name)
    elif ans=="2":
        asset_type_name = input("\n Specify Asset Type Name:")
        add_assettype(asset_type_name)
    elif ans=="3":
      exit()
    elif ans !="":
      print("\n Not Valid Choice Try again") 