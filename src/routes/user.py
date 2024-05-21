from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/register')
def register():
    return 'Register'

@user.route('/login')
def login():
    return 'Login2'