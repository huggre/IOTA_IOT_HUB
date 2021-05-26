import iota_wallet as iw

import threading

from app.wallet_interact import get_account

account = get_account(iw)

# Always sync before doing anything with the account
print('Syncing...')
synced = account.sync().execute()

def main():
    try:
        event = threading.Event()
        thread = threading.Thread(target=f, args=(event,))
        thread.daemon=True
        thread.start()
        event.wait()  # wait forever but without blocking KeyboardInterrupt
    except KeyboardInterrupt:
        print ("Ctrl+C pressed...")
        event.set()  # inform the child thread that it should exit
        sys.exit(1)

def new_transaction_event_processing(event):
    print(f'On new transaction: {event}')
    #result_available.set()

def f(event):
    while not event.is_set():
        print("starting listener")
        iw.on_new_transaction(new_transaction_event_processing)

if __name__ == "__main__":
    # execute only if run as a script
    main()
