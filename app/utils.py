import sqlite3

def get_db_connection():
    conn = sqlite3.connect('rentBlacklist.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_addresses_by_zipcode(zipcode):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT address FROM zipcode_info WHERE zipcode = ?", (zipcode,))
    addresses = [row['address'] for row in cursor.fetchall()]
    conn.close()
    return addresses

def get_info_by_address(address):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT zipcode, address, content FROM zipcode_info WHERE address = ?", (address,))
    info = cursor.fetchone()
    conn.close()
    return dict(info) if info else None