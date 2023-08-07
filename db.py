#!/usr/bin/python
import sqlite3
import datetime
import json
import random

USER_COLS = ['id', 'name']
CHORE_COLS = ['id', 'name', 'description', 'assignee', ('config', 'json')]
CHORE_LOG_COLS = ['id', 'user_id', ('completion_date', 'date')]


def formatDate(s):
    return s.strftime('%m/%d/%Y %H:%M:%S')


def parseDate(s):
    return datetime.datetime.strptime(s, '%m/%d/%Y %H:%M:%S')


def row_to_dict(row, keys):
    result = {}
    for key in keys:
        if isinstance(key, tuple):
            key, vtype = key
            if vtype == 'json':
                val = json.loads(row[key])
            elif vtype == 'date':
                val = parseDate(row[key])
        else:
            val = row[key]
        result[key] = val
    return result


def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn


def create_tables():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL
            );''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Chores (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                assignee INTEGER NOT NULL,
                config TEXT NOT NULL
            );''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS ChoreLogs (
                id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                completion_date TEXT NOT NULL
            );''')
        conn.commit()
        print("Tables created successfully")
    except Exception as e:
        print("Tables creation failed - %s" % e)
    finally:
        conn.close()


def drop_tables():
    try:
        conn = connect_to_db()
        conn.execute('DROP TABLE Users;')
        conn.execute('DROP TABLE Chores;')
        conn.execute('DROP TABLE ChoreLogs;')
        conn.commit()
        print("Tables dropped successfully")
    except Exception as e:
        print("Tables drop failed - %s" % e)
    finally:
        conn.close()


def execute(command, *args):
    try:
        conn = connect_to_db()
        conn.execute(command, *args)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


# Users
def insert_user(user):
    users = get_users()

    for existing_user in users:
        if existing_user['name'] == user['name']:
            return existing_user

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Users (name) VALUES (?)", (user['name'],))
        conn.commit()
        return get_user_by_id(cur.lastrowid)
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_users():
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()

        users = []
        # convert row objects to dictionary
        for row in rows:
            users.append(row_to_dict(row, USER_COLS))
        return users
    except Exception as e:
        raise


def get_user_by_id(user_id):
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE id = ?",
                    (user_id,))
        row = cur.fetchone()
        if not row:
            raise Exception("No user found with id '%s'" % user_id)
        return row_to_dict(row, USER_COLS)
    except Exception as e:
        raise


def update_user(user):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Users SET name = ? WHERE id = ?",
                    (user["name"], user["id"],))
        conn.commit()
        # return the user
        return get_user_by_id(user["id"])
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_user(user_id):
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Users WHERE id = ?",
                     (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

# Chores


def insert_chore(chore):
    chores = get_chores()
    for existing_chore in chores:
        if existing_chore['name'] == chore['name']:
            return existing_chore

    if 'config' not in chore:
        chore['config'] = {}

    if 'users' not in chore['config']:
        chore['config']['users'] = [user['id'] for user in get_users()]

    if 'assignee' not in chore:
        chore['assignee'] = random.choice(chore['config']['users'])
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        config = chore.get('config', {})
        cur.execute("INSERT INTO Chores (name, description, assignee, config) VALUES (?, ?, ?, ?)",
                    (chore['name'],
                     chore['description'],
                     chore['assignee'],
                     json.dumps(config)))
        conn.commit()
        return get_chore_by_id(cur.lastrowid)
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_chores():
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Chores")
        rows = cur.fetchall()
        chores = []
        # convert row objects to dictionary
        for row in rows:
            chores.append(row_to_dict(row, CHORE_COLS))
        return chores
    except Exception as e:
        raise


def get_chore_by_id(chore_id):
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Chores WHERE id = ?",
                    (chore_id,))
        row = cur.fetchone()
        if not row:
            raise Exception("No chore found with id '%s'" % chore_id)
        result = row_to_dict(row, CHORE_COLS)

        latest = get_chore_logs(chore_id=chore_id)
        if latest:
            result['latest'] = latest[0]

        return result
    except Exception as e:
        raise


def update_chore(chore):
    existing_chore = get_chore_by_id(chore['id'])
    if 'config' in chore:
        existing_chore['config'].update(chore['config'])
    else:
        chore['config'] = existing_chore['config']

    if 'assignee' in chore:
        existing_chore['assignee'] = chore['assignee']
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Chores SET assignee = ?, config = ? WHERE id = ?",
                    (chore['assignee'], json.dumps(chore['config']), chore["id"]))
        conn.commit()
        # return the chore
        return get_chore_by_id(chore["id"])
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_chore(chore_id):
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM Chores WHERE id = ?", (chore_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


# Chore Logs
def log_chore(chore_id, user_id):
    completion_date = formatDate(datetime.datetime.now())
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # Log chore completion.
        cur.execute("INSERT INTO ChoreLogs (id, user_id, completion_date) VALUES (?, ?, ?)",
                    (chore_id, user_id, completion_date))
        conn.commit()

        user = get_user_by_id(user_id)
        chore = get_chore_by_id(chore_id)
        message = '%s completed %s at %s' % (
            user['name'], chore['name'], completion_date)
        return {'status': message}
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_chore_logs(chore_id=None, user_id=None):
    users = {user['id']: user for user in get_users()}
    chores = {chore['id']: chore for chore in get_chores()}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        filters = []
        values = []
        if chore_id is not None:
            filters.append('id = ?')
            values.append(chore_id)
        if user_id is not None:
            filters.append('user_id = ?')
            values.append(user_id)
        query = "SELECT * FROM ChoreLogs"
        if filters:
            query += ' WHERE ' + ' AND '.join(filters)
        query += ' ORDER BY completion_date DESC'
        cur.execute(query, values)
        rows = cur.fetchall()
        logs = []
        for row in rows:
            log_row = row_to_dict(row, CHORE_LOG_COLS)
            log_row['chore'] = chores[log_row['id']]
            log_row['user'] = users[log_row['user_id']]
            del log_row['user_id']
            del log_row['id']
            logs.append(log_row)
        return logs
    except Exception as e:
        raise


def get_user_chores(user_id):
    chores = get_chores()
    chores = []
    for chore in chores:
        if chore['rotation'].assignee() == user_id:
            chores.append(chores)
    return chores
