import json
import db


def add_housemates():
    resp = db.insert_user({'name': 'Brett'})
    resp = db.insert_user({'name': 'Cassidy'})
    resp = db.insert_user({'name': 'Tuesday'})
    resp = db.insert_user({'name': 'Calvin'})


def add_chores():
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
        'name': 'Unload Dishwasher',
        'description': 'Unload dishes from dishwasher'
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
        'description': 'Take out kitchen trash and recycle'
    })


def add_special_chores():
    users = db.get_users()['users']
    brett_id = [user['id']
                for user in users if user['name'] == 'Brett'][0]
    cass_id = [user['id']
               for user in users if user['name'] == 'Cassidy'][0]
    # Cass and Brett only
    db.insert_chore({
        'name': 'Refill Water',
        'description': 'Refill container in fridge',
        'config': {'users': [cass_id, brett_id]}
    })
    db.insert_chore({
        'name': 'Water Plants',
        'description': 'Water indoor and outdoor plants',
        'config': {'users': [cass_id, brett_id], 'interval': 2},
        
    })


if __name__ == '__main__':
    db.create_tables()
    add_housemates()
    print(db.get_users())
    add_chores()
    add_special_chores()
    print(db.get_chores())
