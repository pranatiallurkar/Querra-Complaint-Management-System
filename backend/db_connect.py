import mariadb

# db_connect.py — Database connection helper for MariaDB
# Uses official mariadb driver for native GSSAPI/Windows auth support

def get_connection():
    """Return a new MariaDB connection using the official mariadb module.
    
    Edit the connection settings below to match your environment.
    """
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root123',
        'database': 'complaint_db',
        'autocommit': True
    }
    try:
        conn = mariadb.connect(**config)
        return conn
    except mariadb.Error as e:
        raise RuntimeError(f"Database connection error: {e}")