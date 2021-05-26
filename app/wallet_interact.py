#import iota_wallet as iw

import threading
import queue
import time
import os

# The queue to store received events
#q = queue.Queue()


# Get wallet account (create if not exist) and return wallet account object
def get_account(iw):

    account_manager = iw.AccountManager(
        storage_path='./alice-database'
    ) #note: `storage` and `storage_path` have to be declared together

    account_manager.set_stronghold_password("password")

    # mnemonic (seed) should be set only for new storage
    # once the storage has been initialized earlier then you should omit this step
    #account_manager.store_mnemonic("Stronghold")

    account_name = 'AliceX'

    # general Tangle specific options
    client_options = {
        "nodes": [
            {
                "url": "https://api.hornet-0.testnet.chrysalis2.com",
                "auth": None,
                "disabled": False
            }
        ],
        "local_pow": True
    }

    try:

        account = account_manager.get_account(account_name)

        return account

    except ValueError:

        # Account not found, create it

        account_manager.store_mnemonic("Stronghold")

        # an account is generated with the given alias via `account_initialiser`
        account_initialiser = account_manager.create_account(client_options)
        account_initialiser.alias(account_name)

        # initialise account based via `account_initialiser`
        # store it to db and sync with Tangle
        account = account_initialiser.initialise()

        return account

# Get new address
def get_acc_addr(account):

    # Sync account
    synced = account.sync().execute()

    addr_dict = account.generate_address()

    addr = addr_dict['address']['inner']

    return addr
 

### WORKER

'''

def worker():
    """The worker to process the queued events.
    """
    while True:
        item = q.get(True)
        print(f'Get event: {item}')
        q.task_done()


def balance_changed_event_processing(event):
    """Processing function when event is received.
    """
    print(f'On balanced changed: {event}')
    q.put(event)


def new_transaction_event_processing(event):
    """Processing function when event is received.
    """
    print(f'On new transaction: {event}')
    q.put(event)



def start_worker(account):

    # Get the acount manager
    #manager = iota_wallet.AccountManager(
    #    storage_path='./alice-database')

    # NOTE: In real use cases you need to set the password in a safer way, like getting it from env variables
    #manager.set_stronghold_password(STRONGHOLD_PASSWORD)

    # Get the account
    #account = manager.get_account('Alice')
    #account = get_account()
    #print(f'Account: {account.alias()}')

    # Always sync before doing anything with the account
    print('Syncing...')
    synced = account.sync().execute()

    # Get the latest unused address
    last_address_obj = account.latest_address()
    print(f"Address: {last_address_obj['address']}")

    # turn-on the worker thread
    threading.Thread(target=worker, daemon=True).start()

    # listen to the on_balance_change event
    #iw.on_balance_change(balance_changed_event_processing)
    iw.on_new_transaction(new_transaction_event_processing)

    # Use the Chrysalis Faucet to send testnet tokens to your address:
    print(
        f"Fill your Address ({last_address_obj['address']['inner']}) with the Faucet: https://faucet.tanglekit.de/")
    print("To see how the on_balance_change is called, please send tokens to the address in 1 min")
    #time.sleep(60)

    # block until all tasks are done
    #q.join()
    #print('All work completed')

    '''
