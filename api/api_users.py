from flask import request, make_response, jsonify
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from app import app, db
from app.models.tables import User


@app.route('/user_api', methods=['GET'])
def all_users():
    users = User.query.all()
    
    data_user = []
    for u in users:
        data = {}
        data['id'] = u.id
        data['username'] = u.username
        data['password'] = u.password
        data['name'] = u.name
        data['admin'] = u.admin

        data_user.append(data)
    
    return jsonify({'users': data_user})

@app.route('/user_api/<user_id>', methods=['GET'])
def one_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    if not user:
        return jsonify({'message': 'User not found!'})
    
    data_user = {}
    data_user['id'] = user.id
    data_user['username'] = user.username
    data_user['password'] = user.password
    data_user['name'] = user.name
    data_user['admin'] = user.admin

    return jsonify(data_user)

@app.route('/user_api', methods=['POST'])
def create_user():
    data = request.get_json()
    hp = generate_password_hash(data['password'])

    user = User(username = data['username'], password = hp, name = data['name'], admin = False)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})

@app.route('/user_api/<user_id>', methods=['PUT'])
def edit_user(user_id):
    
    return '' 

@app.route('/user_api/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id = user_id). first()
    if not user:
        return jsonify({'message': 'User not found!'})
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})
