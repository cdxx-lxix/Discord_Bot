import sqlite3

# Static connection, always open
conn = sqlite3.connect('botvideos.db')  # Connection
cur = conn.cursor()

# videobase - name : url : owner \\\ The one and only
cur.execute(f'''CREATE TABLE IF NOT EXISTS videobase (name text NOT NULL UNIQUE, url blob NOT NULL,
owner integer NOT NULL )''')


def newRecord(name, url, owner):
    try:
        cur.execute(f'INSERT INTO videobase VALUES ("{name}", "{url}", "{owner}")')
        conn.commit()
        return True
    except sqlite3.Error:
        return False


def sendRecord(search_query):
    try:
        cur.execute(f''' SELECT name, url FROM videobase WHERE name LIKE "{search_query}" ''')
        result = cur.fetchone()
        return result[1]
    except TypeError:
        return False
    except sqlite3.Error:
        return False


def eraseRecord(erase_query, owner):
    cur.execute(f"""SELECT * FROM videobase WHERE name LIKE "{erase_query}" """)
    delete_candidate = cur.fetchone()
    owner_id = delete_candidate[2]
    if owner == owner_id:
        try:
            cur.execute(f''' DELETE FROM videobase WHERE name LIKE "{erase_query}" AND owner LIKE "{owner}" ''')
            conn.commit()
            return True
        except sqlite3.Error:
            return False
    else:
        return False


def adminShowAll():
    cur.execute(f"""SELECT name, owner FROM videobase""")
    result = cur.fetchall()
    return result


def showUserRecords(owner):
    cur.execute(f"""SELECT name FROM videobase WHERE owner LIKE '{owner}' """)
    result = cur.fetchall()
    return result
