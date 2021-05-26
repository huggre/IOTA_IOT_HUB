import iota_wallet as iw

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
