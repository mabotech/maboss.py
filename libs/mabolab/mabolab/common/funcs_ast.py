
import logilab

from logilab.astng import builder

def alert(filename, line, msg):
    print """  File "%s", line %s, %s!!""" % (filename, line, msg)

def main(filename = None):

    filename = "__init__.py"
    

    tbuilder = builder.ASTNGBuilder()
    
    tree = tbuilder.file_build(filename)
    
    for item in tree:
        #if  type(tree[ item]) == logilab.astng.scoped_nodes.Function : 
        if isinstance(tree[ item],  logilab.astng.scoped_nodes.Function):
            t = tree[ item]
            
            print "<<"*20
            print type(t)
            
            if t.decorators != None:
                alert(filename, t.lineno, 'decorator alert')
            
            if t.args.as_string() != 'args':
                alert(filename, t.lineno, 'args alert')
               
            if  t.doc != None:
                docstring = t.doc
            else:
                docstring = None# t.name
                #alert(filename, t.lineno, 'docstring empty alert')
            
            print  "%s,%s,%s" %(filename, t.name, docstring)
            print ">>"*20
        else:
            print item
            print type(tree[item])

if __name__ == "__main__":
    
    main()