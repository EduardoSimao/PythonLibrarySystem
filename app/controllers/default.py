from app import app
from flask import render_template, Blueprint
from app.models.tables import Palestra

Index_blueprint = Blueprint('index', __name__)

@Index_blueprint.route('/')
def index():
    palestras = Palestra.query.all()
    return render_template('index.html', palestras = palestras)


    