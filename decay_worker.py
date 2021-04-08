
import time
import sqlite3
con = sqlite3.connect('iota_iot_hub.db')
cur = con.cursor()

# Main loop that executes every 1 second
while True:
    cur.execute("UPDATE tbl_devices SET remaining_time=remaining_time-1 WHERE remaining_time>0")
    con.commit()
    time.sleep(1)

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
#con.close()

