import requests
import json

URL = 'localhost:5000/api'


def add_housemates():
    requests.post(URL + '/users/add',
                  data=json.dumps({
                      'name': 'Brett',
                  }))
    requests.post(URL + '/users/add',
                  data=json.dumps({
                      'name': 'Cassidy',
                  }))
    requests.post(URL + '/users/add',
                  data=json.dumps({
                      'name': 'Tuesday',
                  }))
    requests.post(URL + '/users/add',
                  data=json.dumps({
                      'name': 'Calvin',
                  }))


def add_chores():
    requests.post(URL + '/chores/add', data=json.dumps({
        'name': 'Clean Kitchen',
        'description': 'Wipe down counters and sweep/mop floors',
    }))
    requests.post(URL + '/chores/add', data=json.dumps({
        'name': 'Vacuum Living Room',
        'description': 'Vacuum living room carpet'
    }))
    requests.post(URL + '/chores/add', data=json.dumps({
        'name': 'Unload Dishwasher',
        'description': 'Unload dishes from dishwasher'
    }))
    requests.post(URL + '/chores/add', data=json.dumps({
        'name': 'Clean Downstairs Bathroom',
        'description': 'Clean floors, toilet, sink'
    }))
    requests.post(URL + '/chores/add', data=json.dumps({
        'name': 'Clean Washer/Dryer',
        'description': 'Clean stains from washer and dryer'
    }))
    requests.post(URL + '/chores/add', data=json.dumps({
        'name': 'Take Out Trash',
        'description': 'Take out kitchen trash and recycle'
    }))

def add_special_chores():
    users = requests.get(URL + '/users')
    brett_id = [user['user_id'] for user in users if user['name'] == 'Brett'][0]
    cass_id = [user['user_id'] for user in users if user['name'] == 'Cassidy'][0]
    # Cass and Brett only
    requests.post(URL + '/chores/add', data=json.dumps({
        'name': 'Refill Water',
        'description': 'Refill container in fridge',
        'users': [cass_id, brett_id]
    }))
    requests.post(URL + '/chores/add', data=json.dumps({
        'name': 'Water Plants',
        'description': 'Water indoor and outdoor plants',
        'users': [cass_id, brett_id]
    }))
