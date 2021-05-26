import iota_wallet as iw

import requests
import json

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

asset_price = 0.000000 # MIOTA pr hour

### Connect to wallet account or create account if it does not exist

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

except ValueError:

    # Account not found, create it

    account_manager.store_mnemonic("Stronghold")

    # an account is generated with the given alias via `account_initialiser`
    account_initialiser = account_manager.create_account(client_options)
    account_initialiser.alias(account_name)

    # initialise account based via `account_initialiser`
    # store it to db and sync with Tangle
    account = account_initialiser.initialise()



# Get account balance
def get_acc_bal(account):

    #account = wallet_connect()
    #account = con_test()

    synced = account.sync().execute()

    #print(account.balance())

    # get total balance for the account
    #print("Total balance:")
    #print(account.balance())
    acc_bal_dict = account.balance()
    #print(acc_bal_dict)
    available_balance_iota = int(acc_bal_dict['available'])
    available_balance_miota = available_balance_iota/1000000
    lbl_balance_txt.configure(text="{:10.6f}".format(available_balance_miota))
    
# Get latest unused address
def get_acc_addr(account):

    #account = wallet_connect()

    # generate new address
    #address = account.generate_address()
    #print(f'New address: {address}')

    # You can also get the latest unused address
    #last_address_obj = account.latest_address()
    #print(last_address_obj)
    #print(f"Last address: {last_address_obj['address']}")
    #print(type(last_address_obj))

    synced = account.sync().execute()

    addr_dict = account.latest_address()
    addr = addr_dict['address']['inner']
    txt_receive_addr.delete(1.0,"end")
    txt_receive_addr.insert(1.0, addr)


def get_asset_detail(key):
    asset_details = json.loads(txt_asset_details.get("1.0",END))
    return asset_details[key]

def send_tokens(account):

    # Get reciever address
    reciever_address = get_asset_detail('payment_address')

    # Get price and convert IOTA
    tokens_to_send = int(round((float(lbl_price_txt['text'])*1000000),6))

    # Clear log
    txt_purchase_log.delete(1.0,"end")

    # Sync account
    txt_purchase_log.insert(1.0, 'Syncing account...')
    synced = account.sync().execute()

    try:

        # Create transfer
        transfer = iw.Transfer(
            amount=tokens_to_send,
            address=reciever_address,
            remainder_value_strategy='ReuseAddress'
        )


        # Propogate the Transfer to Tangle
        # and get a response from the Tangle
        node_response = account.transfer(transfer)
        #print(
        #    node_response
        #)
        txt_purchase_log.insert(2.0, str(tokens_to_send) + ' IOTA was sendt to address: ' + reciever_address)

    except ValueError as e:
        txt_purchase_log.insert(2.0, str(e) + ' , aborting transaction')




# Get asset details from server API
def get_asset_details(asset_id):
    url = 'http://localhost:5000/iotago_api/v1.0/get_asset_info/' + str(asset_id)
    # Get API response
    resp = requests.get(url)
    if resp.status_code == 200:
        # Get response content
        response = json.loads(resp.text)
        # Update global asset_price var from response
        global asset_price
        asset_price = float(response['price'])
        # Add respose to asset details and activate Purchase tab
        txt_asset_details.delete(1.0,"end")
        txt_asset_details.insert(1.0, resp.text)
        app_notebook.select(1)
    else:
        # Write error to error log
        txt_get_asset_log.delete(1.0,"end")
        txt_get_asset_log.insert(1.0, resp.status_code)

# Calculat total price in MIOTA based on selected DD:HH:MM and display result in price label
def price_calc():
    total_hours = (int(sb_day.get()) * 24) + int(sb_hrs.get()) + (int(sb_min.get()) / 60)
    total_price = total_hours * asset_price
    total_price_rounded = round(total_price,6)
    lbl_price_txt.configure(text="{:10.6f}".format(total_price_rounded))


# Define main window
root = Tk()
root.title("IOTA IOT Hub Client")
#root.iconbitmap('c:/gui/codemy.ico')
root.geometry('626x626')

# Define main window background image 
background_image=PhotoImage(file='Mobile-Transparent-Free-PNG.png')
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Define notebook size and placement
app_notebook = ttk.Notebook(root, height=372, width=212)
app_notebook.place(x=206, y=117)

# Define "Get Asset" frame with 3 columns
frm_get_asset = Frame(app_notebook)
frm_get_asset.columnconfigure(0, weight=1)
frm_get_asset.columnconfigure(1, weight=1)
frm_get_asset.columnconfigure(3, weight=1)

# Define "Purchase" frame with 3 columns
frm_purchase = Frame(app_notebook, bg="red")
frm_purchase.columnconfigure(0, weight=1)
frm_purchase.columnconfigure(1, weight=1)
frm_purchase.columnconfigure(2, weight=1)

# Define "Wallet" frame with 3 columns
frm_wallet = Frame(app_notebook, bg="yellow")
frm_wallet.columnconfigure(0, weight=1)
frm_wallet.columnconfigure(1, weight=1)
frm_wallet.columnconfigure(2, weight=1)

# Add tabs to notebok
app_notebook.add(frm_get_asset, text="Get Asset")
app_notebook.add(frm_purchase, text="Purchase")
app_notebook.add(frm_wallet, text="Wallet")

### Define "Get Asset" frame elements

camera_image = Image.open('camera.png')
camera_image = camera_image.resize((100,100))
photoImg =  ImageTk.PhotoImage(camera_image)
camera_label = Label(frm_get_asset, image=photoImg, width=150, height=150)
camera_label.grid(row=0, column=0, columnspan=3, sticky="N,E,S,W")

btn_camera = Button(frm_get_asset, text='Scan Asset QR code')
btn_camera.grid(row=1, column=0, columnspan=3, sticky="N,E,S,W")

lbl_or_get_by_asset_id = Label(frm_get_asset, text="or get Asset by Asset ID")
lbl_or_get_by_asset_id.grid(row=2, column=0, columnspan=3, sticky="N,E,S,W")

lbl_asset_id = Label(frm_get_asset, text="Asset ID:")
lbl_asset_id.grid(row=3, column=0, sticky="N,E,S,W")

ent_asset_id = Entry(frm_get_asset)
ent_asset_id.grid(row=3, column=1, sticky="N,E,S,W")

btn_get_asset_details = Button(frm_get_asset, text="Get", command= lambda: get_asset_details(ent_asset_id.get()))
btn_get_asset_details.grid(row=3, column=2, sticky="N,E,S,W")

lbl_get_asset_log = Label(frm_get_asset, text="Log:")
lbl_get_asset_log.grid(row=4, column=0, columnspan=3, sticky="N,E,S,W")

txt_get_asset_log = Text(frm_get_asset, height=7)
txt_get_asset_log.grid(row=5, column=0, columnspan=3, sticky="N,E,S,W")

### Define "Purchase" frame elements

lbl_asset_details = Label(frm_purchase, text="Asset Details:")
lbl_asset_details.grid(row=0, column=0, columnspan=3, sticky="N,E,S,W")

txt_asset_details = Text(frm_purchase, height=5)
txt_asset_details.grid(row=1, column=0, columnspan=3, sticky="N,E,S,W")

lbl_spec_time = Label(frm_purchase, text="Specify Time")
lbl_spec_time.grid(row=2, column=0, columnspan=3, sticky="N,E,S,W")

lbl_days = Label(frm_purchase, text="Days")
lbl_days.grid(row=3, column=0, sticky="N,E,S,W")

lbl_hours = Label(frm_purchase, text="Hours")
lbl_hours.grid(row=3, column=1, sticky="N,E,S,W")

lbl_minutes = Label(frm_purchase, text="Minutes")
lbl_minutes.grid(row=3, column=2, sticky="N,E,S,W")

sb_day = Spinbox(frm_purchase, from_=0, to=99, command= lambda: price_calc())
sb_day.grid(row=4, column=0, sticky="N,E,S,W")

sb_hrs = Spinbox(frm_purchase, from_=0, to=24, command= lambda: price_calc())
sb_hrs.grid(row=4, column=1, sticky="N,E,S,W")

sb_min = Spinbox(frm_purchase, from_=0, to=60, command= lambda: price_calc())
sb_min.grid(row=4, column=2, sticky="N,E,S,W")

lbl_price = Label(frm_purchase, text="PRICE:")
lbl_price.grid(row=5, column=0, sticky="N,E,S,W")

lbl_price_txt = Label(frm_purchase, text="0.000000")
lbl_price_txt.grid(row=5, column=1, sticky="N,E,S,W")

lbl_price_units = Label(frm_purchase, text="MIOTA")
lbl_price_units.grid(row=5, column=2, sticky="N,E,S,W")

btn_send = Button(frm_purchase, text="Send", command= lambda: send_tokens(account))
btn_send.grid(row=6, column=0, columnspan=3, sticky="N,E,S,W")

txt_purchase_log = Text(frm_purchase, height=7)
txt_purchase_log.grid(row=7, column=0, columnspan=3, sticky="N,E,S,W")


### Define "Wallet" frame elements

lbl_balance = Label(frm_wallet, text="Balance(MI):")
lbl_balance.grid(row=0, column=0, sticky="N,E,S,W")

lbl_balance_txt = Label(frm_wallet, text="0.000000")
lbl_balance_txt.grid(row=0, column=1, sticky="N,E,S,W")

btn_refresh = Button(frm_wallet, text="Refresh", command= lambda: get_acc_bal(account))
btn_refresh.grid(row=0, column=2, sticky="N,E,S,W")

btn_receive = Button(frm_wallet, text="Receive", command= lambda: get_acc_addr(account))
btn_receive.grid(row=1, column=0, columnspan=3, sticky="N,E,S,W")

txt_receive_addr = Text(frm_wallet, height=5)
txt_receive_addr.grid(row=2, column=0, columnspan=3, sticky="N,E,S,W")


root.mainloop()




