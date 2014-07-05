
import threading

class Singleton(object):   

    objs  = {}
    objs_locker =  threading.Lock()

    def __new__(cls, *args, **kv):
        #print cls
        if cls in cls.objs:
            return cls.objs[cls]['obj']

        cls.objs_locker.acquire()
        try:

            if cls in cls.objs: ## double check locking
                return cls.objs[cls]['obj']
            obj = object.__new__(cls)
            cls.objs[cls] = {'obj': obj, 'init': False}
            
            #decorate_init
            setattr(cls, '__init__', cls.decorate_init(cls.__init__))

        finally:
            cls.objs_locker.release()   
            
            return cls.objs[cls]['obj']

    @classmethod
    def decorate_init(cls, fn):

        def init_wrap(*args):
            if not cls.objs[cls]['init']:
                fn(*args)
                cls.objs[cls]['init'] = True
            return

        return init_wrap
        

class Demo(Singleton):
    
    def __init__(self):
        print "init..."
        print id(self)
        
    def get_id(self):
        
        return id(self)
        
if __name__ == "__main__":
    
    
    #a = Demo()
    
    #print a
    
    a1 = Demo()
    
    #print a1
    
    print a1.get_id()
    
    a2 = Demo()
    #print a2
    print a2.get_id()
    a3 = Demo()
    
    #print a3
    print a3.get_id()
    
    

