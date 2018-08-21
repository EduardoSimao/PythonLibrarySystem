from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import db, lm
from app.models.tables import User
from app.models.forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates',
    url_prefix='/users'

)


@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

#****************** Adicionar User ***************************
@users_blueprint.route("/") 
def user():
    return render_template('add_user.html')

@users_blueprint.route('/post_user', methods=["POST"])
def post_user():
    password = request.form['password']
    if request.form.get('admin'):
        admin = True
    else:
        admin = False

    user = User(request.form['username'], generate_password_hash(password), request.form['name'], request.form['email'], admin = admin)
    db.session.add(user)
    db.session.commit()
    flash('Cadastrado com sucesso')
    
    return redirect(url_for('index.index'))

#******************* Listas Usuarios *****************

@users_blueprint.route('/list_users', methods=['GET'])
@login_required
def listarUser():
    if not current_user.admin == True:
        return render_template('404.html'), 404

    users = User.query.all()
    return render_template('listar_users.html', users = users)

#********Alterar permissão do usuarios atraves da list de pesquisa ********
@users_blueprint.route('/list_users/edit_user/<user_id>')
@login_required
def edit_user(user_id):
    if not current_user.admin == True:
        return render_template('404.html'), 404
        
    user = User.query.filter_by(id = user_id).first()

    if user.admin == True:
        user.admin = False
    else:
        user.admin = True
    
    db.session.commit()

    return redirect(url_for('users.listarUser'))

#***************** Autenticar login ***************************
@users_blueprint.route('/login', methods=["GET","Post"])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
               
        password = request.form['password']
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index.index'))
        
    return render_template('login.html', form=form)

#************ Fazer logout ****************************
@users_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.index'))


