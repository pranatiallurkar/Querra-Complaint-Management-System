import os
import mariadb

def get_connection():
    config = {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "autocommit": True,
        "ssl": True
    }

    try:
        return mariadb.connect(**config)
    except mariadb.Error as e:
        raise RuntimeError(f"Database connection error: {e}")