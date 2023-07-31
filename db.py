#!/usr/bin/python
import sqlite3
import datetime
import chore_config

USER_COLS = ['user_id', 'name']
CHORE_COLS = ['chore_id', 'name', 'description', 'config']
CHORE_LOG_COLS = ['chore_id', 'user_id', 'completion_date']


def jsonify_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print('%s Error: %s' % (func.__name__, e))
            result = {'error': str(e)}
        return result
    return inner


def row_to_dict(row, keys):
    result = {}
    for key in keys:
        result[key] = row[key]
    return result


def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn


def create_tables():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL
            );''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Chores (
                chore_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                config TEXT NOT NULL
            );''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS ChoreLogs (
                chore_id INTEGER NOT NULL,
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


# Users
@jsonify_error
def insert_user(user):
    result = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Users (name) VALUES (?)", (user['name'],))
        conn.commit()
        result = get_user_by_id(cur.lastrowid)
    except Exception as e:
        conn.rollback()
        result['error'] = str(e)
    finally:
        conn.close()
    return result


@jsonify_error
def get_users():
    result = {}
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
        result['users'] = users
    except Exception as e:
        result['error'] = str(e)
    return result


@jsonify_error
def get_user_by_id(user_id):
    result = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE user_id = ?",
                    (user_id,))
        row = cur.fetchone()
        if not row:
            return {'error': "No user found with id '%s'" % user_id}
        result = row_to_dict(row, USER_COLS)
    except Exception as e:
        result = {'error': str(e)}
        raise
    return result


@jsonify_error
def update_user(user):
    result = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Users SET name = ? WHERE user_id = ?",
                    (user["name"], user["user_id"],))
        conn.commit()
        # return the user
        result = get_user_by_id(user["user_id"])
    except Exception as e:
        conn.rollback()
        result['error'] = str(e)
    finally:
        conn.close()
    return result


@jsonify_error
def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Users WHERE user_id = ?",
                     (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception as e:
        conn.rollback()
        message["status"] = "Cannot delete user - %s" % e
    finally:
        conn.close()
    return message

# Chores


@jsonify_error
def insert_chore(chore):
    result = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        config = chore_config.ChoreConfig()
        cur.execute("INSERT INTO Chores (name, description, config) VALUES (?, ?, ?)",
                    (chore['name'],
                     chore['description'],
                     repr(config)))
        conn.commit()
        result = get_chore_by_id(cur.lastrowid)
    except Exception as e:
        conn.rollback()
        result['error'] = str(e)
    finally:
        conn.close()
    return result


@jsonify_error
def get_chores():
    result = {}
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
        result['chores'] = chores
    except Exception as e:
        result['error'] = str(e)
    return result


@jsonify_error
def get_chore_by_id(chore_id):
    result = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Chores WHERE chore_id = ?",
                    (chore_id,))
        row = cur.fetchone()
        if not row:
            return {'error': "No chore found with id '%s'" % chore_id}
        result = row_to_dict(row, CHORE_COLS)
    except Exception as e:
        result = {'error': str(e)}
    return result


@jsonify_error
def update_chore(chore):
    result = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Chores SET name = ?, description = ?, users = ? WHERE chore_id = ?",
                    (chore["name"], chore["description"], chore["users"], chore["chore_id"],))
        conn.commit()
        # return the chore
        result = get_chore_by_id(chore["chore_id"])
    except Exception as e:
        conn.rollback()
        result['error'] = str(e)
    finally:
        conn.close()
    return result


@jsonify_error
def delete_chore(chore_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Chores WHERE chore_id = ?", (chore_id,))
        conn.commit()
        message["status"] = "chore deleted successfully"
    except Exception as e:
        conn.rollback()
        message["status"] = "Cannot delete chore - %s" % e
    finally:
        conn.close()
    return message


@jsonify_error
def log_chore(chore_id, user_id):
    result = {}
    completion_date = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    try:
        user = get_user_by_id(user_id)
        chore = get_chore_by_id(chore_id)
        conn = connect_to_db()
        cur = conn.cursor()
        # Log chore completion.
        cur.execute("INSERT INTO ChoreLogs (chore_id, user_id, completion_date) VALUES (?, ?)",
                    (chore_id, user_id, completion_date))
        conn.commit()
        result['message'] = '%s completed %s at %s' % (
            user['name'], chore['name'], completion_date)
    except Exception as e:
        conn.rollback()
        result['error'] = str(e)
    finally:
        conn.close()
    return result


@jsonify_error
def get_chore_logs(chore_id=None, user_id=None):
    result = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        filters = []
        values = []
        if chore_id is not None:
            filters.append('chore_id = ?')
            values.append(chore_id)
        if user_id is not None:
            filters.append('user_id = ?')
            values.append(user_id)
        query = "SELECT * FROM ChoreLogs"
        query.append(' WHERE ' + ' AND '.join(filters))
        cur.execute(query, values)
        rows = cur.fetchall()
        logs = []
        for row in rows:
            logs.append(row_to_dict(row, CHORE_LOG_COLS))
        result['logs'] = logs
    except Exception as e:
        result = {'error': str(e)}
    return result


@jsonify_error
def get_user_chores(user_id):
    chores = get_chores()
    if 'error' in chores:
        return chores
    chores = []
    for chore in chores:
        if chore['rotation'].assignee() == user_id:
            chores.append(chores)
    return {'chores': chores}
