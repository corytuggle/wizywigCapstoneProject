from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Content(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(5000), nullable=False)
    text = db.Column(db.String(65000), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.date)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, title, text, date_added, user_token, id=''):
        self.id = self.set_id()
        self.title = title
        self.text = text
        self.date_added = date_added
        self.user_token = user_token

    def __repr__(self):
        return f'Added {self.title} to the Content Library on {self.date_added}.'

    def set_id(self):
        return (secrets.token_urlsafe())

class ContentSchema(ma.Schema):
    class Meta:
        fields = ['id','title', 'text', 'date_added']

content_schema = ContentSchema()
contents_schema = ContentSchema(many=True)