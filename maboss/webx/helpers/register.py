import logging
import logging.handlers
import logging.config

#from maboss import config

log = logging.getLogger(__name__)


from .lazy_view import LazyView

#function view
def url(app, url_rule, import_name, **options):
    view = LazyView('maboss.' + import_name)
    app.add_url_rule(url_rule, view_func=view, **options)
    
    
#restful function view     
def register_rest(app, url_base, import_name, pk='id', pk_type='int'):
    
    log.debug("=="*20)
    log.debug(import_name)
   
    #get
    url_rule = url_base
    view = LazyView('maboss.' + import_name+'.get')
    log.debug(view)
    app.add_url_rule(url_rule, view_func=view, methods = ['OPTIONS', 'GET',])    
    
    #post
    url_rule = url_base
    view = LazyView('maboss.' + import_name+'.post')
    app.add_url_rule(url_rule, view_func=view, methods = ['OPTIONS', 'POST'])
    
    #get
    url_rule ='%s<%s:%s>' % (url_base, pk_type, pk)
    view = LazyView('maboss.' + import_name+'.get')
    app.add_url_rule(url_rule, view_func=view, methods = ['OPTIONS', 'GET',])

    #put
    url_rule = '%s<%s:%s>' % (url_base, pk_type, pk)
    view = LazyView('maboss.' + import_name+'.put')
    app.add_url_rule(url_rule, view_func=view, methods = ['OPTIONS', 'PUT'])

    #delete
    url_rule ='%s<%s:%s>' % (url_base, pk_type, pk)
    view = LazyView('maboss.' + import_name+'.delete')
    app.add_url_rule(url_rule, view_func=view, methods = ['OPTIONS', 'DELETE'])   
    


#class view
def register_api(app, view, endpoint, url, pk='id', pk_type='int'):
    
    view_func = view.as_view(endpoint)
    
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])
    