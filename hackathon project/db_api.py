import sqlite3

def is_username_present(conn, username):
    cursor = conn.cursor()

    # Execute a SELECT query to check if the username is already present
    cursor.execute('''
        SELECT * FROM Token_table
        WHERE telegram_username = ?
    ''', (username,))

    # Fetch one row; if a row is fetched, the username is already present
    existing_data = cursor.fetchone()

    return existing_data is not None

def add_user(username):
    conn = sqlite3.connect('userData.db')
    cursor = conn.cursor()

    row = (username, None, 0)

    # Execute the INSERT command
    if is_username_present(conn, username):
        cursor.execute('''
            INSERT INTO Token_table (telegram_username, token_filename, is_connecting_to_google_calendar)
            VALUES (?, ?)
        ''', row)
        print("Username: " + username + " is successfully added into database.")

    # Commit and close the connection
    conn.commit()
    conn.close()
    
def connect_google_calendar(username, connect: bool):
    conn = sqlite3.connect('userData.db')
    cursor = conn.cursor()
    connect_int = 0 if connect == False else 1
    
    # Execute the UPDATE command
    if is_username_present(conn, username):
        cursor.execute("UPDATE Token_table SET is_connecting_to_google_calendar = ? WHERE telegram_username = ?", (connect_int, username))
        print("Username: " + username + " is successfully added into database.")

    # Commit and close the connection
    conn.commit()
    conn.close()
        
def is_user_connecting_gc(username):
    conn = sqlite3.connect('userData.db')
    cursor = conn.cursor()
    cursor.execute("SELECT is_connecting_to_google_calendar FROM Token_table WHERE telegram_username = ?", (username,))
    result = cursor.fetchone()
    if result == 0: return False
    else: return True
    