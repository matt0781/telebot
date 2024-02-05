import sqlite3

# Connect to the database
conn = sqlite3.connect('userData.db')

# Create a cursor
cursor = conn.cursor()

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Token_table (
        telegram_username TEXT PRIMARY KEY,
        token_filename TEXT,
        is_connecting_to_google_calendar INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Events (
        id INTEGER PRIMARY KEY,
        username TEXT,
        notification INTEGER,
        start_dateTime TEXT,
        end_dateTime TEXT,
        location TEXT,
        summary TEXT,
        FOREIGN KEY (username) REFERENCES Token_table(telegram_username)
    )
""")


# Commit and close the connection
conn.commit()
conn.close()