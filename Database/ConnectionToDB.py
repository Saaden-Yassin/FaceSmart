import sqlite3

try:
    conn = sqlite3.connect(database='../../Database/FaceSmartDB.db', check_same_thread=False)
    cursor = conn.cursor()
except sqlite3.Error as sqlerror:
    print("Error !!!", sqlerror)
