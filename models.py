from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False, default='')
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, nullable=False, default=False)
    token = db.Column(db.String, nullable=False, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.g_auth_verify = g_auth_verify
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(100), nullable = False, default='')
    model = db.Column(db.String(100), nullable = False, default='')
    year = db.Column(db.Integer, nullable = False, default='')
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False, default='')

    def __init__(self, make, model, year, user_token):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.user_token = user_token

    def __repr__(self):
        return f'The car has been added to the inventory: {self.year} {self.make} {self.model} ({self.id})'

    def set_id(self):
        return (secrets.token_urlsafe())

class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make', 'model', 'year', 'user_token']

class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'email']

car_schema = CarSchema()
car_multi_schema = CarSchema(many=True)
user_schema = UserSchema()