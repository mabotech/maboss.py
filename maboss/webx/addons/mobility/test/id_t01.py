

class T(object):
    self.id = 10
    
    print id(self.id)
    
t = T

print id(T.id)
print id(t.id)
