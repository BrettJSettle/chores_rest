from flask import Flask, request, jsonify, Response #added to top of file
from flask_cors import CORS #added to top of file
import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def flaskify(data):
    print(data)
    if 'error' in data:
        return Response(data['error'], data.get('code', 500))
    return jsonify(data)

# Users
@app.route('/api/users', methods=['GET'])
def api_get_users():
    return flaskify(db.get_users())

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return flaskify(db.get_user_by_id(user_id))

@app.route('/api/users/add',  methods = ['POST'])
def api_add_user():
    user = request.get_json()
    return flaskify(db.insert_user(user))

@app.route('/api/users/update',  methods = ['PUT'])
def api_update_user():
    user = request.get_json()
    return flaskify(db.update_user(user))

@app.route('/api/users/delete/<user_id>',  methods = ['DELETE'])
def api_delete_user(user_id):
    return flaskify(db.delete_user(user_id))

# Chores
@app.route('/api/chores', methods=['GET'])
def api_get_chores():
    return flaskify(db.get_chores())

@app.route('/api/chores/<chore_id>', methods=['GET'])
def api_get_chore(chore_id):
    return flaskify(db.get_chore_by_id(chore_id))

@app.route('/api/chores/add',  methods = ['POST'])
def api_add_chore():
    chore = request.get_json()
    return flaskify(db.insert_chore(chore))

@app.route('/api/chores/update',  methods = ['PUT'])
def api_update_chore():
    chore = request.get_json()
    return flaskify(db.update_chore(chore))

@app.route('/api/chores/delete/<chore_id>',  methods = ['DELETE'])
def api_delete_chore(chore_id):
    return flaskify(db.delete_chore(chore_id))

# Chore Logs
@app.route('/api/chores/<chore_id>/log', methods = ['POST'])
def api_log_chore(chore_id):
    info = request.get_json()
    return flaskify(db.log_chore(chore_id, info['user_id']))

@app.route('/api/chores/<chore_id>/logs', methods = ['GET'])
def api_get_chore_logs(chore_id):
    return flaskify(db.get_chore_logs(chore_id=chore_id))

@app.route('/api/users/<user_id>/logs', methods = ['GET'])
def api_get_user_logs(user_id):
    return flaskify(db.get_chore_logs(user_id=user_id))

@app.route('/api/chores/<chore_id>/users/<user_id>/logs', methods = ['GET'])
def api_get_user_chore_logs(chore_id, user_id):
    return flaskify(db.get_chore_logs(chore_id=chore_id, user_id=user_id))


if __name__ == "__main__":
    # app.run(host="192.168.1.165", port=5000)
    db.create_tables()
    app.debug = True
    app.run(port=5000)