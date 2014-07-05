
from flask import Blueprint

from maboss.runwebx import jsonrpc

mod = Blueprint('user', __name__)
jsonrpc.register_blueprint(mod)

@jsonrpc.method('User.index(a1=int, b2=str)')
def index(a1, b2):
    return {"data": [a1, b2, 'Welcome to User API', 'WebX']}