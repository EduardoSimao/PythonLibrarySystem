
#Importando uma instancia da classe flask, para poder utilizar o framework

#Init é um arquiv de quand a gente trabaha com modulos

from flask import Flask, render_template 
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES

#app é uma estancia da classe Flask, do framework
app = Flask(__name__)
#__name__ = é uma variavel especial que o interpretador 
# do python cria quando ele ta executando o arquivo, 
# dando um valor dizendo qual é o arquivo que estamos executando
#se é um aquivo princiapal da aplicação ou um secundario
#se for o principal ele da o nome de main
#a variavel app é muito importante, pois ela cira controlar toda a plicação

app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm = LoginManager(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


from app.models import tables, forms
from api import api_leitores, api_livros, api_users

from app.controllers.default import Index_blueprint
from app.controllers.user.routes import users_blueprint
from app.controllers.palestra.routes import palestras_blueprint
from app.controllers.livro.routes import livros_blueprint
from app.controllers.leitor.routes import leitor_blueprint


app.register_blueprint(Index_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(palestras_blueprint)
app.register_blueprint(livros_blueprint)
app.register_blueprint(leitor_blueprint)



