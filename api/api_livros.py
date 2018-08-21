from flask import request, make_response, jsonify
from uuid import uuid4
import jwt
import datetime
from functools import wraps
from app import app, db
from app.models.tables import Book

@app.route('/livro_api', methods=['GET'])
def todos_livros():
    livros = Book.query.all()
    all_books = [] 

    for bk in livros:
        book_data = {}
        book_data['id'] = bk.id
        book_data['nome_book'] = bk.nome_book
        book_data['genero'] = bk.genero
        book_data['autor'] = bk.autor
        book_data['ano'] = bk.ano

        all_books.append(book_data)

    return jsonify({'books': all_books})

@app.route('/livro_api/<book_id>', methods=['GET'])
def um_livro(book_id):
    livro = Book.query.filter_by(id = book_id).first()
    if not livro:
        return jsonify({'message': 'Book not found!'})
    
    book_data = {}
    book_data['id'] = livro.id
    book_data['nome_book'] = livro.nome_book
    book_data['genero'] = livro.genero
    book_data['autor'] = livro.autor
    book_data['ano'] = livro.ano

    return jsonify(book_data)

@app.route('/livro_api', methods=['POST'])
def criar_livro():
    data = request.get_json()

    livro = Book(nome_book = data['nome_book'], genero = data['genero'], autor = data['autor'], ano = data['ano'])
    db.session.add(livro)
    db.session.commit()

    return jsonify({'message': 'Livro criado com sucesso!'})


@app.route('/livro_api/<book_id>', methods=['DELETE'])
def delete_livro(book_id):
    livro = Book.query.filter_by(id = book_id).first()
    if not livro:
        return jsonify({'message': 'Book not found!'})
    
    db.session.delete(livro)
    db.session.commit()

    return jsonify({'message': 'Book deleted with sucessful!'})
