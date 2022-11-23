import sqlite3
from utils import logging
def connect(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    return c, conn

def add_row(my_dict, db, table):
    try : 
        c, conn = connect(db)
        columns = ', '.join(my_dict.keys())
        placeholders = ':'+', :'.join(my_dict.keys())
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (table, columns, placeholders)
        c.execute(query, my_dict)
        conn.commit()
        logging.info(f"Data Added to {table}")
    except sqlite3.Error as error:
        raise(f"Coudln't add to table {error}")

def select_last_id(db, table):
    c, conn = connect(db)
    query = f"SELECT PATIENT_NUM FROM {table} ORDER BY PATIENT_NUM DESC LIMIT 1"
    c.execute(query)
    conn.commit()
    return c.fetchall()[0][0]
