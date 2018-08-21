from flask import request, make_response, jsonify
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from app import app, db
from app.models.tables import Leitor 


@app.route('/leitor_api', methods=['GET'])
def todos_leitores():
    leitores = Leitor.query.all()

    all_leitores = [] 

    for l in leitores:
        data = {} 
        data['id'] = l.id
        data['nome'] = l.nome
        data['username'] = l.username
        data['password'] = l.password
        data['email'] = l.email
        data['endereco'] = l.endereco
        data['situacao'] = l.situacao

        all_leitores.append(data)

    return jsonify({'leitores': all_leitores})

@app.route('/leitor_api/<leitor_id>', methods=['GET'])
def um_leitor(leitor_id):
    leitor = Leitor.query.filter_by(id = leitor_id).first()
    if not leitor:
        return jsonify({'message': 'Leitor not found!'})
    
    leitor_data = {}
    leitor_data['id'] = leitor.id
    leitor_data['nome'] = leitor.nome
    leitor_data['username'] = leitor.username
    leitor_data['password'] = leitor.password
    leitor_data['email'] = leitor.email
    leitor_data['endereco'] = leitor.endereco
    leitor_data['situacao'] = leitor.situacao


    return jsonify(leitor_data)

@app.route('/leitor_api', methods=['POST'])
def criar_leitor():
    data = request.get_json()
    hp = generate_password_hash(data['password'])
    
    new_leitor = Leitor(nome = data['nome'], username = data['username'], password = hp, email = data['email'], endereco = data['endereco'], situacao = True)
    db.session.add(new_leitor) 
    db.session.commit()

    return jsonify({'message': 'Leitor cadastrado com sucesso!'})

@app.route('/leitor_api/<leitor_id>', methods=['PUT'])
def edit_leitor(leitor_id):
    leitor = Leitor.query.filter_by(id = leitor_id).first()
    if not leitor:
        return jsonify({'message': 'Leitor not found!'})
    
    if leitor.situacao == True:
        leitor.situacao = False
        db.session.commit()
    else:
        leitor.situacao = True
        db.session.commit()        

    return jsonify({'message': 'Leitor alterado com sucesso!'})

@app.route('/leitor_api/<leitor_id>', methods=['DELETE'])
def delete_leitor(leitor_id):
    leitor = Leitor.query.filter_by(id = leitor_id).first()
    if not leitor:
        return jsonify({'message': 'Leitor not found!'})
    
    db.session.delete(leitor)
    db.session.commit()

    return jsonify({'message': 'Leitor deletado com sucesso!'})