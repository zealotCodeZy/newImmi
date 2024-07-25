import sqlite3

def get_db_connection():
    conn = sqlite3.connect('blacklist.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_addresses_rent(zipcode):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT address FROM rent_info WHERE zipcode = ?", (zipcode,))
    addresses = [row['address'] for row in cursor.fetchall()]
    conn.close()
    return addresses

def get_info_rent(address):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT zipcode, address, content FROM rent_info WHERE address = ?", (address,))
    info = cursor.fetchone()
    conn.close()
    return dict(info) if info else None

def get_name_work(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM work_info WHERE name like ?", ('%' + name + '%',))
    names = [row['name'] for row in cursor.fetchall()]
    conn.close()
    return names

def get_info_work(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM work_info WHERE name = ?", (name,))
    info = cursor.fetchone()
    conn.close()
    return dict(info) if info else None