from threading import Thread
from app import app
# ...

def get_async_addr(app, account):
    with app.app_context():
            # Sync account
        synced = account.sync().execute()

        addr_dict = account.generate_address()

        addr = addr_dict['address']['inner']

    return addr


def get_addr(account):
    addr = Thread(target=get_async_addr, args=(app, account)).start()
    return addr