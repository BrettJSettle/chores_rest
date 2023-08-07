from flask import Flask, request, jsonify #added to top of file
from flask_cors import CORS #added to top of file
import db
import datetime
import random

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, origins="*")

# Users
@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(db.get_users())

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(db.get_user_by_id(user_id))

@app.route('/api/users/add',  methods = ['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(db.insert_user(user))

@app.route('/api/users/update',  methods = ['PUT'])
def api_update_user():
    user = request.get_json(force=True)
    return jsonify(db.update_user(user))

@app.route('/api/users/delete/<user_id>',  methods = ['DELETE'])
def api_delete_user(user_id):
    return jsonify(db.delete_user(user_id))

# Chores
@app.route('/api/chores', methods=['GET'])
def api_get_chores():
    chores = db.get_chores()
    return jsonify(db.get_chores())

@app.route('/api/chores/<chore_id>', methods=['GET'])
def api_get_chore(chore_id):
    return jsonify(db.get_chore_by_id(chore_id))

@app.route('/api/chores/add',  methods = ['POST'])
def api_add_chore():
    chore = request.get_json()
    return jsonify(db.insert_chore(chore))

@app.route('/api/chores/update',  methods = ['PUT'])
def api_update_chore():
    chore = request.get_json()
    return jsonify(db.update_chore(chore))

@app.route('/api/chores/delete/<chore_id>',  methods = ['DELETE'])
def api_delete_chore(chore_id):
    return jsonify(db.delete_chore(chore_id))

@app.route('/api/chores/<chore_id>/skip', methods=['POST'])
def api_skip(chore_id):
    chore = db.get_chore_by_id(chore_id)
    return jsonify(update_assignee(chore_id, exclude=[chore['assignee']]))

# Chore Logs
@app.route('/api/chore_logs', methods = ['GET'])
def api_get_logs():
    return jsonify(db.get_chore_logs())

@app.route('/api/chores/<chore_id>/log', methods = ['POST'])
def api_log_chore(chore_id):
    info = request.get_json()
    db.log_chore(chore_id, info['user_id'])
    return jsonify(update_assignee(chore_id))

def update_assignee(chore_id, exclude=None):
    if not exclude:
        exclude = []
    chore = db.get_chore_by_id(chore_id)
    user_ids = chore['config']['users']
    chore_logs = db.get_chore_logs(chore_id=chore_id)
    history = {user_id: datetime.datetime.min for user_id in user_ids if user_id not in exclude}
    for log in chore_logs:
        user_id = log['user']['id']
        if user_id in exclude:
            continue
        if history[user_id] > log['completion_date']:
            continue
        history[user_id] = log['completion_date']
        if all([v > datetime.datetime.min for v in history.values()]):
            break
    longest_since_users = sorted(history, key=lambda user_id: history[user_id])
    new_assignee = longest_since_users[0]
    chore = db.update_chore({
        'id': chore_id,
        'assignee': new_assignee
    })
    return chore

@app.route('/api/chores/<chore_id>/logs', methods = ['GET'])
def api_get_chore_logs(chore_id):
    return jsonify(db.get_chore_logs(chore_id=chore_id))

@app.route('/api/users/<user_id>/logs', methods = ['GET'])
def api_get_user_logs(user_id):
    return jsonify(db.get_chore_logs(user_id=user_id))

@app.route('/api/chores/<chore_id>/users/<user_id>/logs', methods = ['GET'])
def api_get_user_chore_logs(chore_id, user_id):
    return jsonify(db.get_chore_logs(chore_id=chore_id, user_id=user_id))


if __name__ == "__main__":
    db.create_tables()
    # app.debug = True
    app.run(host="192.168.1.167", port=5000)