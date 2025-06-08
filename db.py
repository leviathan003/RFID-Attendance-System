import sqlite3
import datetime

DB_NAME = 'student_attendance.db'
MASTER_TABLE = 'master_attendance'

# Initialize master table

def initialize_master_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {MASTER_TABLE} (
            tag_id TEXT PRIMARY KEY,
            student_roll TEXT UNIQUE,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_newTagID(tag, roll, name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO {MASTER_TABLE} 
                   (tag_id, student_roll, name) VALUES (?,?,?)'''
                   ,(tag, roll, name))
    conn.commit()
    conn.close()
    print(str(tag)+name+roll+" Registered")

# Create a new copy of the master table for the day

def create_or_connect_daily_table(date_str):
    table_name = f"attendance_{date_str}"
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute(f'''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', (table_name,))
    exists = cursor.fetchone()

    if not exists:
        # Create the table from master_attendance
        cursor.execute(f'''
            CREATE TABLE {table_name} AS 
            SELECT tag_id, student_roll, name, "" AS in_time, "" AS out_time FROM master_attendance
        ''')
    
    cursor.execute(f'''INSERT INTO {table_name} (tag_id, student_roll, name) 
                   SELECT m.tag_id, m.student_roll, m.name
                   FROM {MASTER_TABLE} m LEFT JOIN {table_name} c ON m.tag_id=c.tag_id 
                   WHERE c.tag_id IS NULL''')

    conn.commit()
    conn.close()
    return table_name

# Mark in or out time on tag

def record_entry_exit(tag_id, time, date_str):
    table_name = create_or_connect_daily_table(date_str)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT in_time, out_time FROM {table_name} WHERE tag_id = ?", (tag_id,))
    result = cursor.fetchone()
    status="LOGIN"
    if result:
        in_time, out_time = result
        if not in_time:
            cursor.execute(f"UPDATE {table_name} SET in_time = ? WHERE tag_id = ?", (time, tag_id))
        elif not out_time:
            cursor.execute(f"UPDATE {table_name} SET out_time = ? WHERE tag_id = ?", (time, tag_id))
            status="LOGOUT"
    conn.commit()
    conn.close()
    return status

# Fetch records from a specific date table

def retrieve_daily_attendance(date_str):
    try:
        table_name = f"attendance_{date_str}"
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        conn.close()
        return records
    except sqlite3.OperationalError as e:
        if datetime.datetime.strptime(date_str.replace("_", "/"), "%d/%m/%Y") <= datetime.datetime.now():
            create_or_connect_daily_table(date_str)
        else:
            pass

def get_all_valid_tags():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT tag_id FROM master_attendance")
    tags = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tags

def get_tag_roll_dict():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT tag_id, student_roll FROM master_attendance")
    tag_roll_map = {tag: roll for tag, roll in cursor.fetchall()}
    conn.close()
    return tag_roll_map

# # Usage example
# if __name__ == "__main__":
#     initialize_master_table()

#     # Prompt for date to create daily attendance table
#     user_date = input("Enter date for attendance table (DD/MM/YYYY): ")
#     user_date = user_date.replace("/","_")
#     table_name = create_or_connect_daily_table(user_date)
    
#     record_entry_exit("03 46 67 92", user_date)
#     record_entry_exit("03 46 67 92", user_date)  # simulate exit

#     # Print attendance
#     for row in retrieve_daily_attendance(user_date):
#         print(row)
