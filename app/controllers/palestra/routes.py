from flask import render_template, flash, redirect, url_for, request, Blueprint, make_response
from app import db, photos
from flask_login import login_required, current_user
from app.models.tables import User, Palestra, Publico
import pdfkit
import os

palestras_blueprint = Blueprint(
    'palestras',
    __name__,
    url_prefix='/palestras'
)


#***************** Adicionar Palestra *********************
@palestras_blueprint.route('/', methods = ['GET', 'POST'])
@login_required
def palestra():
    if not current_user.admin == True:
        return render_template('404.html'), 404
        
    if request.method =='POST':
        filename = photos.save(request.files['imagem'])
        palestra = Palestra(request.form['titulo'], request.form['palestrante'], request.form['descricao'], filename, request.form['duracao'], request.form['dateTime'])
        
        db.session.add(palestra)
        db.session.commit()  
        flash('Emprestimo realizado com sucesso!')
        
        return redirect(url_for('index.index'))

    return render_template('palestra.html') 


#***************** Cadastrar Publico na palestra *******************************
@palestras_blueprint.route('/viewPalestra/cadPublico/<palestra_id>/<user_id>', methods=['POST'])
@login_required
def cadPublico(palestra_id, user_id):
    user = User.query.filter_by(id = user_id).first()
    palestra = Palestra.query.filter_by(id = palestra_id).first()

    usuario = Publico.query.filter_by(id_user = user_id, id_palestra = palestra_id).first()
    if usuario:
        flash('Você já esta cadastrado nessa Palestra!') 
    else:
        publico = Publico(id_palestra = palestra.id, nome_palestra = palestra.titulo, palestrante = palestra.palestrante, id_user = user_id, nome_user = user.name)
        
        db.session.add(publico)
        db.session.commit()
        flash('Cadastrado com sucesso!')
        return redirect(url_for('index.index'))
    
    return viewPalestra(palestra.id)

#******************* Listas de Palestras *****************
@palestras_blueprint.route('/list_palestra', methods=['GET'])
@login_required
def listarPalestra():
    if not current_user.admin == True:
        return render_template('404.html'), 404

    palestras = Palestra.query.all()

    return render_template('listar_palestra.html', palestras = palestras)

'''@palestras_blueprint.route('/list_palestra/list_uses/<palestra_id>', methods=['GET'])
@login_required
def listaInscritos(palestra_id):
    if not current_user.admin == True:
        return render_template('404.html'), 404
    
    palestras = Palestra.query.filter_by(id = palestra_id).all()
    if not palestras:
        flash('Nenhum inscrito na palestra!')
        return redirect(url_for('palestras.listarPalestra'))
    
    return render_template('listar_palestra.html', palestras = palestras)'''
    

#************************ Ver informações da palestra ****************************
@palestras_blueprint.route('/viewPalestra/<id_palestra>')
def viewPalestra(id_palestra):
    palestra = Palestra.query.filter_by(id = id_palestra).first()

    return render_template('info_palestra.html', palestra = palestra)

#******************* Listas Usuarios cadastrados nas Palestras *****************
@palestras_blueprint.route('/list_publico')
@login_required
def list_publico():
    usuario = Publico.query.all()

    return render_template('listar_publico.html', usuario = usuario)

#************************ Excluir Palestra ****************************
@palestras_blueprint.route('/delPalestra/<palestra_id>')
@login_required
def delPalestra(palestra_id):
    if not current_user.admin == True:
        return render_template('404.html'), 404

    palestra = Palestra.query.filter_by(id = palestra_id).first()

    path ="app/static/img/leitor_livro"
    dir = os.listdir(path)
    for file in dir:
        if file == palestra.banner:
            os.remove('app/static/img/leitor_livro/'+ file)

    db.session.delete(palestra)
    db.session.commit()
    flash('Palestra excluida com sucesso!')

    return redirect(url_for('index.index'))

#******************* Listas Usuarios *****************
@palestras_blueprint.route('/list_usuario/<user_id>')
@login_required
def list_usuario(user_id):
    usuario = Publico.query.filter_by(id_user = user_id).all()

    return render_template('listar_publico.html', usuario = usuario)



#************************ Alterações Usuario da Palestra ****************************
@palestras_blueprint.route('/list_usuario/delPublico/<usuario_id>/<palestra_id>')
@login_required
def delPublico(usuario_id, palestra_id):
    usuario = Publico.query.filter_by(id_user = usuario_id, id_palestra = palestra_id).first()

    db.session.delete(usuario)
    db.session.commit()

    return redirect('palestras/list_usuario/{}'.format(usuario.id_user))


#***************** Gerar Relatorio ***********************************************

@palestras_blueprint.route('/viewPalestra/lista/<id_palestra>')
@login_required
def pdf_template(id_palestra):
    if not current_user.admin == True:
        return render_template('404.html'), 404
        
    publico = Publico.query.filter_by(id_palestra = id_palestra).all()
    palestra = Palestra.query.filter_by(id = id_palestra).first()

    rendered = render_template('listaInscritos.html', publico = publico, palestra = palestra)
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers['Content-ype'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename = {}.pdf'.format(palestra.titulo)

    return response

