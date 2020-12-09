"""Models for User"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    '''Connect to database '''
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User model'''
    __tablename__ = 'users'

    username = db.Column(db.String(20),primary_key=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False) # required
    email = db.Column(db.String(50), nullable=False) # required
    first_name = db.Column(db.String(30), nullable=False) # required
    last_name = db.Column(db.String(30), nullable=False) # required

    feedback = db.relationship('Feedback', backref="user", cascade="all,delete")
    
    #register
    @classmethod
    def register(cls, username, pwd,first_name,last_name,email):
        ''' Register user w/ hashed password. Returns a user'''
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')

        return cls(username=username, password=hashed_utf8,email=email,first_name=first_name,last_name=last_name)
    
    #authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        ''' Validate that user exists and password is correct.
        Return user if valid, else False:
        '''
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,pwd):
            #return instance
            return user
        else:
            return False

    #fullname
    @property
    def full_name(self):
        '''Return Full Name'''
        return f'{self.first_name} {self.last_name}'

class Feedback(db.Model):
    '''Feedback model'''
    __tablename__= 'feedback'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'),nullable=False)
