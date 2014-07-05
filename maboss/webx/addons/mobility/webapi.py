
from mabolab.core.base import Base

base = Base()
db = base.get_db('postgresql') #'postgresql'  #default db is Oracle
log = base.get_logger()


from flask import Blueprint

jsonrpc = base.get_jsonrpc()

from mabolab.database.pagination_query import PaginationQuery

mod = Blueprint('weixin', __name__)
jsonrpc.register_blueprint(mod)

@jsonrpc.method('Weixin.list(page=int, limit=int, orderby=str, sort_order=str)')
def index(page, limit, orderby, sort_order):
    
    pq = PaginationQuery(db)
    
    if orderby == "":
        orderby = "id"
        sort_order = "desc"
    
    orderby = " order by %s %s "  % (orderby, sort_order)
    
    sql = """select wx.fromusername as fromusername , wx.tousername, wx.content , wx.active, wx.createdon, wx.createdby
    from mt_t_weixin wx %s""" % (orderby)
    
    #page = 1
    
    #limit = 2
    
    #orderby = 'order by id desc'
    
    log.debug(sql)
    
    try:
        (total_pages, rowcount, keys, data) = pq.query(sql, page, limit, orderby)
    except Exception, e:
        raise Exception(e.message)    
    
    return {'total_pages': total_pages, "data": data, "cols": keys }
