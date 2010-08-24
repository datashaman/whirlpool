import linuxtuples, time

conn = linuxtuples.connect()

while 1:
    conn.log()
    time.sleep(5)
