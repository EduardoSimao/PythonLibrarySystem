from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import app, db, photos
from app.models.tables import Leitor
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_login import current_user

leitor_blueprint = Blueprint(
    'leitor',
    __name__,
    url_prefix='/leitor',
    template_folder = 'templates'
)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated and current_user.admin == True:
            return f(*args, **kwargs)
        else:
            return render_template('404.html'), 404
    return wrap

#****************** Adicionar Leitor *****************************
@leitor_blueprint.route('/')
@login_required
def leitor():
    return render_template('leitor.html')

@leitor_blueprint.route('/post_leitor', methods=["POST"])
@login_required
def post_leitor():
    filename = photos.save(request.files['imagem'])        
    password = request.form['password']
    leitor = Leitor(request.form['nome'], request.form['username'], generate_password_hash(password), request.form['email'], request.form['endereco'], situacao = True, foto = filename )
    
    db.session.add(leitor)
    db.session.commit()
    flash('Cadastrado com sucesso!')
    
    return redirect(url_for('index.index'))

#******************* Listas de Leitores *****************

@leitor_blueprint.route('/list_leitor', methods=['GET'])
@login_required
def listarLeitor():
    

    leitores = Leitor.query.all()
    
    return render_template('listar_leitor.html', leitores = leitores)

#************************ Alterar Leitor ****************************
@leitor_blueprint.route('/list_leitor/alt_situacao/<id_leitor>')
@login_required
def alt_situacao(id_leitor):
    
        
    leitor = Leitor.query.filter_by(id = id_leitor).first()
        
    if leitor.situacao == True:
        leitor.situacao = False
        db.session.commit() 
    else:
        leitor.situacao = True
        db.session.commit()
        
    return redirect(url_for('leitor.listarLeitor'))


@leitor_blueprint.route('/list_leitor/alt_leitor/<id_leitor>', methods=['GET', 'POST'])
@login_required
def alt_leitor(id_leitor):
    leitor = Leitor.query.filter_by(id = id_leitor).first()

    if request.method == 'POST':
        password = request.form.get('password')

        leitor.nome = request.form.get('nome')
        leitor.username = request.form.get('username')
        leitor.password =  generate_password_hash(password)
        leitor.email = request.form.get('email')
        leitor.endereco = request.form.get('endereco')
        
        db.session.commit()
        return redirect(url_for('leitor.listarLeitor'))
    

    return render_template('edit_leitor.html', leitor = leitor)