from flask import Blueprint, render_template
from models import User

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    users = User.query.all()
    return render_template('index.html', users=users)

