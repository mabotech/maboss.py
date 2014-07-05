from flask import Blueprint


from maboss.runwebx import jsonrpc

mod = Blueprint('article', __name__)
jsonrpc.register_blueprint(mod)

@jsonrpc.method('Article.index')
def index():
    return 'Welcome to Article API'