# miloslavovy
# constants
import select
import datetime

DEFAULT_MESAGE = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
INSERT_TEXT_MESSAGE = """INSERT INTO text (value) VALUES (%s) RETURNING id;"""
INSERT_BIN_MESSAGE = """INSERT INTO bin (id, value) VALUES (%s, %s);"""
UPDATE_TEXT = """UPDATE text SET value = 'changed';"""
DELETE_TEXT = """DELETE FROM text WHERE id = %s;"""

#listen
def listen(cursor): 
    cursor.execute("LISTEN q_event")
    cursor.execute("LISTEN q_event_bin;")

# notify
def notify(connection):
    connection.poll()
    while connection.notifies:
        notify = connection.notifies.pop()
        #print("Got NOTIFY:", datetime.datetime.now(), notify.pid, notify.channel, notify.payload)

def notifyEndless(conn, cursor):
    seconds_passed = 0
    print ("Waiting for notifications on channel 'test'")
    while 1:
        conn.commit()
        if select.select([conn],[],[],5) == ([],[],[]):
            seconds_passed += 5
            print ("{} seconds passed without a notification...".format(seconds_passed))
        else:
            seconds_passed = 0
            conn.poll()
            conn.commit()
            while conn.notifies:
                notify = conn.notifies.pop()
                print("Got NOTIFY:", datetime.datetime.now(), notify.pid, notify.channel, notify.payload)


# DB connection function
def DBConnect(psycopg2):
    connection_string = "host='localhost' dbname='postgres' user='xsedla0k' password='bejbojsu8m'"
    connection = psycopg2.connect(connection_string)
    return connection.cursor()

# delete function
def delete(cursor, connection):
    cursor.execute('DELETE FROM text')
    cursor.execute('DELETE FROM bin')
    connection.commit()

# insert naive
def insertNaive(cursor, connection):
    cursor.execute(INSERT_TEXT_MESSAGE, (DEFAULT_MESAGE,))
    connection.commit()
    id_of_new_row = cursor.fetchone()[0]
    return id_of_new_row

# insert more
def insert(cursor, connection, data):
    cursor.execute(INSERT_TEXT_MESSAGE, (data,))
    connection.commit()

# insert bin
def insertBin(cursor, connection, data, insert_id):
    cursor.execute(INSERT_BIN_MESSAGE, (insert_id, data))
    connection.commit()

# update naive
def updateNaive(cursor, connection):
    cursor.execute(UPDATE_TEXT)
    connection.commit()

#delete
def deleteFromTable(cursor, connection, insert_id):
    cursor.execute(DELETE_TEXT, (insert_id,))
    connection.commit()

#getScore
def getScore(sumTimingResult, number):
    score = 0
    for x in range(len(sumTimingResult)): 
        score += sumTimingResult[x]/number
    return score
