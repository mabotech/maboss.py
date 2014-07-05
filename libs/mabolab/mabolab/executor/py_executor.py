
import sys

from ..utils.importlib import import_module

def execute(fullname, args, module_path=None):
    
    if module_path != None:
        if module_path not in sys.path:    
            sys.path.append(module_path)
    
    i_module_name, function_name = fullname.rsplit('.', 1)
    
    #here the repository leading string is hard code.
    module_name = '.'.join(['repository', i_module_name])
    
    #TODO:
    # - if the module create time is changed, reload the module
    try:
        if  module_name in sys.modules:
            module = sys.modules[module_name]
        else:
            module = import_module(module_name)
    except Exception, e:
            raise Exception("import module error:%s [%s]" % (module_name, e.message) )
    if  hasattr(module, function_name):
        func = getattr(module, function_name)
        return  func(args)
    else:
        raise Exception('no this function:%s' %(function_name) )

if __name__ == '__main__':
    
    pass