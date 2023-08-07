import json
import db


def add_housemates():
    users = []
    users.append(db.insert_user({'name': 'Brett'}))
    users.append(db.insert_user({'name': 'Cassidy'}))
    users.append(db.insert_user({'name': 'Tuesday'}))
    users.append(db.insert_user({'name': 'Calvin'}))
    return users


def add_chores(users):
    db.insert_chore({
        'name': 'Clean Kitchen',
        'description': 'Wipe down counters and sweep/mop floors',
        'config': {'interval': 14}
    })
    db.insert_chore({
        'name': 'Vacuum Living Room',
        'description': 'Vacuum living room carpet',
        'config': {'interval': 14}
    })
    db.insert_chore({
        'name': 'Clean Downstairs Bathroom',
        'description': 'Clean floors, toilet, sink',
        'config': {'interval': 14}
    })
    db.insert_chore({
        'name': 'Clean Washer/Dryer',
        'description': 'Clean stains from washer and dryer',
        'config': {'interval': 14}
    })
    db.insert_chore({
        'name': 'Take Out Trash',
        'description': 'Take out kitchen trash and recycle',
    })
    db.insert_chore({
        'name': 'Unload Dishwasher',
        'description': 'Unload dishes from dishwasher',
    })
    cass_brett = [user['id']
                  for user in users if user['name'] in ('Brett', 'Cassidy')]
    # Cass and Brett only
    db.insert_chore({
        'name': 'Refill Water',
        'description': 'Refill container in fridge',
        'config': {'users': cass_brett}
    })
    db.insert_chore({
        'name': 'Water Plants',
        'description': 'Water indoor and outdoor plants',
        'config': {'users': cass_brett, 'interval': 2},

    })


def setup():
    db.create_tables()
    users = db.get_users()
    if not users:
        users = add_housemates()
    if not db.get_chores():
        add_chores(users)


if __name__ == '__main__':
    # Delete history
    # db.execute('DELETE FROM ChoreLogs WHERE 1;')
    setup()

