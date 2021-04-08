import sqlite3

def hello(x):
    print(Hello)

con = sqlite3.connect(":memory:")
con.create_function("hello", 1, hello)
cur = con.cursor()
cur.execute("CREATE TABLE t(x)")
cur.execute("CREATE TRIGGER tt AFTER INSERT ON t BEGIN SELECT hello(NEW.x); END;")
cur.execute("INSERT INTO t VALUES(1)")