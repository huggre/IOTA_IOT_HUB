from flask_table import Table, Col, ButtonCol, LinkCol
 
# Define Accounts table
class AccountsTable(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    balance = Col('Balance [MIOTA]')
    created = Col('Created On')
    modified = Col('Modified On')
    owner = Col('Owner')
    edit=LinkCol('Edit','edit_account',url_kwargs=dict(id='id'))
    delete=LinkCol('Delete','delete_account',url_kwargs=dict(id='id'))

# Define Assets table
class AssetsTable(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    balance = Col('Balance')
    created = Col('Created On')
    modified = Col('Modified On')
    asset_type = Col('Asset Type')
    #account = Col('Account')
    owner = Col('Owner')
    edit=LinkCol('Edit','edit_asset',url_kwargs=dict(id='id'))
    delete=LinkCol('Delete','delete_asset',url_kwargs=dict(id='id'))

# Define Memebrs table
class MembersTable(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    email = Col('Email')
    password_hash = Col('Password', show=False)
    created = Col('Created On')
    modified = Col('Modified On')

# Define Sensors table
class SensorsTable(Table):
    id = Col('Id', show=False)
    UID = Col('UID')
    name = Col('Name')
    created = Col('Created On')
    modified = Col('Modified On')
    sensor_type = Col('Sensor Type')
    parent_asset = Col('Parent Asset')
    owner = Col('Owner')
    edit=LinkCol('Edit','edit_sensor',url_kwargs=dict(id='id'))
    delete=LinkCol('Delete','delete_sensor',url_kwargs=dict(id='id'))

# Define Tags table
class TagsTable(Table):
    id = Col('Id', show=False)
    UID = Col('UID')
    name = Col('Name')
    created = Col('Created On')
    modified = Col('Modified On')
    tag_type = Col('Tag Type')
    account = Col('Account')
    owner = Col('Owner')
    edit=LinkCol('Edit','edit_tag',url_kwargs=dict(id='id'))
    delete=LinkCol('Delete','delete_tag',url_kwargs=dict(id='id'))

# Define Transactions table
class TransactionsTable(Table):
    id = Col('Id', show=False)
    sensor_id = Col('Sensor ID')
    tag_id = Col('Tag ID')
    timestamp = Col('Timestamp')
    value = Col('Value')

# Define Deposits table
class DepositsTable(Table):
    id = Col('Id', show=False)
    account = Col('Account')
    value = Col('Value [MIOTA]')
    timestamp = Col('Timestamp')
    owner = Col('Owner')

# Define Withdrawals table
class WithdrawalsTable(Table):
    id = Col('Id', show=False)
    account = Col('Account')
    value = Col('Value [MIOTA]')
    timestamp = Col('Timestamp')
    owner = Col('Owner')
