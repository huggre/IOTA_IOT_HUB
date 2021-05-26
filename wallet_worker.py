# Copyright 2020 IOTA Stiftung
# SPDX-License-Identifier: Apache-2.0

import datetime

import json

import iota_wallet as iw
import threading
import queue
import time
import os
from dotenv import load_dotenv

from app import db

from app.models import tbl_assets
from app.models import tbl_endpoints
from app.models import tbl_services
from app.models import tbl_transactions
from app.models import tbl_settlements


from app.ha_interact import call_service


# Load the env variables
#load_dotenv()

# Get the stronghold password
#STRONGHOLD_PASSWORD = os.getenv('STRONGHOLD_PASSWORD')

# This example shows how to listen to on_balance_change event.

from app.wallet_interact import get_account

# The queue to store received events
q = queue.Queue()

# Add settlement to db
def add_settlement(payment_address, recieve_address, value):
    settlement = tbl_settlements()
    settlement.payment_address=payment_address
    settlement.recieve_address=recieve_address
    settlement.value=value
    db.session.add(settlement)
    db.session.commit()

    return settlement.id

# Add transaction to db
def add_transaction(asset, status, message_id, payment_address, recieve_address, value):
    transaction = tbl_transactions()
    transaction.asset = asset
    transaction.status = status
    transaction.message_id = message_id
    transaction.settlement = add_settlement(payment_address, recieve_address, value)

    db.session.add(transaction)
    db.session.commit()

def manage_new_transaction(message_id, customer_addr, asset_addr, amount, confirmed):

    # get asset data from payment address
    asset = (db.session.query(tbl_assets, tbl_endpoints, tbl_services)
        .join(tbl_endpoints)
        .join(tbl_services)
        .filter(tbl_assets.payment_address == asset_addr)
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
        add_transaction(None, 1, message_id, asset_addr, customer_addr, amount)
        return

    # Check value = price
    if amount != asset.price*1000000:
        # Recived amount does not match price, return payment with error
        add_transaction(asset.id, 2, message_id, asset_addr, customer_addr, amount)
        return

    # Call Home Assistant service
    response = call_service(asset.endpoint, asset.token, asset.tech_name, asset.service_data)
    if response.status_code != 200:
        add_transaction(asset.id, 3, message_id, asset_addr, customer_addr, amount)
        return
        #print(response.status_text)

    # All is good, forward payment to asset owner
    add_transaction(asset.id, 0, message_id, asset_addr, asset.recieve_address, amount)



def worker():
    """The worker to process the queued events.
    """
    while True:
        item = q.get(True)
        
        #print(f'Get event: {item}')

        transaction_data = json.loads(item)
        message_id = (transaction_data['message']['id'])
        customer_addr = (transaction_data['message']['payload']['data']['essence']['data']['inputs'][0]['data']['metadata']['address'])
        asset_addr = (transaction_data['message']['payload']['data']['essence']['data']['outputs'][0]['data']['address'])
        amount = (transaction_data['message']['payload']['data']['essence']['data']['outputs'][0]['data']['amount'])
        confirmed = (transaction_data['message']['confirmed'])

        print('Transaction recieved with message id = ' + message_id)

        manage_new_transaction(message_id, customer_addr, asset_addr, amount, confirmed)

        #print('message_id=' + message_id)
        #print('customer=' + customer_addr)
        #print('asset=' + asset_addr)
        #print('amount=' + str(amount))
        #print('confirmed=' + str(confirmed))


        q.task_done()


def new_transaction_event_processing(event):
    """Processing function when event is received.
    """
    #print(f'On new transaction: {event}')
    q.put(event)

def test(account):
    print('Starting task')
    for i in range(10):
        print(i)
        time.sleep(2)
    print('Task completed')
  

def start_worker():
        
    # Get the acount manager
    manager = iw.AccountManager(
        storage_path='./alice-database')

    account = get_account(iw)

    # NOTE: In real use cases you need to set the password in a safer way, like getting it from env variables
    #manager.set_stronghold_password(STRONGHOLD_PASSWORD)

    # Get the account
    #account = manager.get_account('Alice')
    print(f'Account: {account.alias()}')

    # Always sync before doing anything with the account
    print('Syncing...')
    #synced = account.sync().execute()

    # Get the latest unused address
    last_address_obj = account.latest_address()
    print(f"Address: {last_address_obj['address']}")

    # turn-on the worker thread
    t1 = threading.Thread(target=worker, daemon=True)
    t2 = threading.Thread(target=test, daemon=True, args=(account,))

    t1.start()
    t2.start()

    # listen to the on_balance_change event
    #iota_wallet.on_balance_change(balance_changed_event_processing)
    iw.on_new_transaction(new_transaction_event_processing)

    # Use the Chrysalis Faucet to send testnet tokens to your address:
    print(
        f"Fill your Address ({last_address_obj['address']['inner']}) with the Faucet: https://faucet.tanglekit.de/")
    print("To see how the on_balance_change is called, please send tokens to the address in 1 min")
    time.sleep(600)

    # block until all tasks are done
    q.join()
    print('All work completed')