from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import db, photos
from app.models.tables import Leitor, Book, Alugar
from datetime import date
from functools import wraps
from flask_login import current_user

livros_blueprint = Blueprint(
    'livros',
    __name__,
    url_prefix='/livros',
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


#*********************** adicionar Livro *****************************
@livros_blueprint.route('/')
@login_required
def livros(): 
    return render_template('livros.html') 

@livros_blueprint.route('/post_livro', methods=['POST'])
@login_required
def post_livro():
          
    filename = photos.save(request.files['imagem'])  

    livro = Book(request.form['nome_book'], request.form['genero'], request.form['autor'], request.form['ano'], foto = filename)
    db.session.add(livro)
    db.session.commit()
    flash('Cadastrado com sucesso!')
    
    return redirect(url_for('index.index'))
        
#******************* Listas de livros *****************
@livros_blueprint.route('/list_livros', methods=['GET'])
@login_required
def listarLivro():
    books = Book.query.all()   

    return render_template('listar_livros.html', books = books)

#************************ Alterar Livro ****************************
@livros_blueprint.route('/list_livros/alt_livro/<id_livro>', methods=['GET', 'POST'])
@login_required
def alt_livro(id_livro):
    livro = Book.query.filter_by(id = id_livro).first() 

    if request.method == 'POST':
        livro.nome_book = request.form.get('nome_book')
        livro.genero = request.form.get('genero')
        livro.ano = request.form.get('ano')
        livro.autor = request.form.get('autor')
     
        db.session.commit()

        return redirect(url_for('livros.listarLivro'))   

    return render_template("edit_book.html", livro = livro)

#************************** adiconar livro emprestado ******************
@livros_blueprint.route('/emprestar')
@login_required
def emprestar():
    return render_template('emprestar1.html')

@livros_blueprint.route('/emprestar/pesquisar', methods=['POST'])
@login_required
def pesquisarLivro():
    livro = Book.query.filter_by(id = request.form['cod_livro']).first()
    leitor = Leitor.query.filter_by(id = request.form['cod_leitor']).first()

    if not livro:
        flash('Livro não encontrado!')
        return render_template('emprestar1.html')
    elif not leitor:
        flash('Leitor não encontrado!')
        return render_template('emprestar1.html')
    
    if leitor.situacao == False:
        flash('Leitor se encontra com pendência!')
        return render_template('emprestar1.html')
    else:
        dt_atual = date.today()
        futuro = date.fromordinal(dt_atual.toordinal()+7)

        dt_atual = dt_atual.strftime('%d/%m/%Y')
        futuro = futuro.strftime('%d/%m/%Y')

        
    return render_template('emprestar2.html',livro = livro, leitor = leitor, dt_atual = dt_atual, futuro = futuro)

@livros_blueprint.route('/emprestar/post_emprestimo', methods =['POST'])
@login_required
def post_emprestimo():
    
    leitor = Leitor.query.filter_by(id = request.form['user_id']).first()
    emprestimo = Alugar(request.form['user_id'], request.form['nome_leitor'], request.form['book_id'], request.form['nome_livro'], request.form['inicio'], request.form['fim'], situacao = True)
    
    leitor.situacao = False
    db.session.add(emprestimo)
    db.session.commit()
    flash('Emprestimo realizado com sucesso!')
    return redirect(url_for('index.index'))

#******************* Listas de Emprestimos *****************
@livros_blueprint.route('/emprestar/list_emprestimo', methods=['GET'])

def listarEmprestimo(): 
    emprestimo = Alugar.query.all()

    return render_template('listar_Emprestimo.html', emprestimo = emprestimo)

#************************ Alterações atraves das pesqisas****************************
@livros_blueprint.route('/emprestar/list_emprestimo/del_emprestimo/<id_emprestimo>')
@login_required
def del_emprestimo(id_emprestimo):
    emprestimo = Alugar.query.filter_by(id = id_emprestimo).first()
    leitor = Leitor.query.filter_by(id = emprestimo.user_id).first()

    leitor.situacao = True            
    db.session.delete(emprestimo)
    db.session.commit()

    return redirect(url_for('livros.listarEmprestimo'))

