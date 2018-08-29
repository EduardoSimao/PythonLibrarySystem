from app import db
from flask_login import UserMixin
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    admin = db.Column(db.Boolean)
   

    @property
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return False
    
    def is_anonymous(self):
        return True
    
    def get_id(self): 
        return str(self.id)


    def __init__(self, username, password, name, email, admin):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.admin = admin
       

    def __repr__(self):
        return '<User %r>' % self.username

class Leitor(db.Model):
    __tablename__ = 'leitor'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    endereco = db.Column(db.String)
    situacao = db.Column(db.Boolean)
    foto = db.Column(db.String)
       
    def __init__(self, nome, username, password, email, endereco, situacao, foto):
        self.nome = nome
        self.username = username
        self.password = password
        self.email = email
        self.endereco = endereco
        self.situacao = situacao
        self.foto = foto
       
    
    def __repr__(self):
        return '<Leitor %r>' % self.nome

       

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    nome_book = db.Column(db.String)
    descricao = db.Column(db.String(800))
    genero = db.Column(db.String)
    autor = db.Column(db.String)
    ano = db.Column(db.Integer)
    foto = db.Column(db.String(100))

    def __init__(self, nome_book, descricao, genero, autor, ano, foto):
        self.nome_book = nome_book
        self.descricao = descricao
        self.genero = genero
        self.autor =autor
        self.ano = ano
        self.foto = foto
    
    def __repr__(self):
        return '<Book %r>' % self.nome_book


class Alugar(db.Model):
    __tablename___ = 'alugar'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    nome_leitor = db.Column(db.String)
    book_id = db.Column(db.Integer)
    nome_livro = db.Column(db.String)
    inicio = db.Column(db.String)
    fim = db.Column(db.String)
    situacao = db.Column(db.Boolean)

    def __init__(self, user_id, nome_leitor, book_id, nome_livro, inicio, fim, situacao):
        self.user_id = user_id
        self.nome_leitor = nome_leitor
        self.book_id = book_id
        self.nome_livro = nome_livro
        self.inicio = inicio
        self.fim = fim
        self.situacao = situacao
        

class Palestra(db.Model):
    __tablename__ = 'palestra'

    id = db.Column(db.Integer, primary_key = True)
    palestrante = db.Column(db.String)
    titulo = db.Column(db.String)
    descricao = db.Column(db.String)
    banner = db.Column(db.String)
    duracao = db.Column(db.Integer) #minutos
    dateTime = db.Column(db.String)

    def __init__(self, titulo, palestrante, descricao, banner, duracao, dateTime):
        self.titulo = titulo
        self.palestrante = palestrante
        self.descricao = descricao
        self.banner = banner
        self.duracao = duracao
        self.dateTime = dateTime

class Publico(db.Model):
    __tablename__ = 'publico'

    id = db.Column(db.Integer, primary_key = True)
    id_palestra = db.Column(db.Integer)
    nome_palestra = db.Column(db.String)
    palestrante = db.Column(db.String)
    id_user = db.Column(db.Integer)
    nome_user = db.Column(db.String)

    def __init__(self, id_palestra, nome_palestra, palestrante, id_user, nome_user):
        self.id_palestra = id_palestra
        self.nome_palestra = nome_palestra
        self.palestrante = palestrante
        self.id_user = id_user
        self.nome_user = nome_user