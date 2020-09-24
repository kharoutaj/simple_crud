from flask import Flask, jsonify, request, make_response
from uuid import uuid4

seven_app = Flask(__name__)

# -- this dictionary will serve as in-memory db for this exercise
user_db = {}

# -- These API endpoints provide a REST CRUD interface for a simple user entity
# -- The user entity has the following fields:
# -- first_name, last_name, email
# -- These entries are stored in memory within a hash table that is keyed by uuid generated at user creation


@seven_app.route('/users/create', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'No user data provided'}), 400)
    new_user = request.get_json()
    new_id = uuid4()
    user_db[new_id] = new_user
    return jsonify({'data': new_id}), 200


@seven_app.route('/users/update/<uuid:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'No user data provided'}), 400)
    if user_id in user_db:
        user_db[user_id] = request.get_json()
        return jsonify(request.get_json()), 200
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


@seven_app.route('/users/delete/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not user_db.pop(user_id, []):
        return jsonify({'data': ''}), 404
    return jsonify({'data': 'True'}), 200


@seven_app.route('/users/info/<uuid:user_id>', methods=['GET'])
def info_user(user_id):
    if user_id in user_db:
        return jsonify({'data': user_db[user_id]}), 200
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


seven_app.run()
