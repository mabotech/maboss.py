

import logging
import logging.handlers
import logging.config

log = logging.getLogger(__name__)


from werkzeug import import_string, cached_property

class LazyView(object):

    def __init__(self, import_name):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        
        log.debug( "~~"*20 )
        log.debug( import_name )
        
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)

    def __call1__(self, *args, **kwargs):
        
        log.debug ( "__call__" * 5 )
        
        log.debug( args )
        log.debug( kwargs )
        
        return self.view(*args, **kwargs)
        
class LazyBlueprintView(object):

    def __init__(self, import_name, endpoint):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        
        self.endpoint = endpoint
        
        log.debug( "~~"*20 )
        log.debug( import_name )
        
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)
        
    def __call__(self, *args, **kwargs):
            view = self.view.as_view(self.endpoint)
            for decorator in view.decorators:
                view = decorator(view)
            return view(*args, **kwargs)