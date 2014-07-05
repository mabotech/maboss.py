import re


def spec_parse(docstring):
    # common variables

    rawstr = r"""{(.*)}"""


    # method 1: using a compile object
    #compile_obj = re.compile(rawstr,  re.MULTILINE)
    #match_obj = compile_obj.search(docstring)

    # method 2: using search function (w/ external flags)
    #match_obj = re.search(rawstr, docstring,  re.MULTILINE)

    # method 3: using search function (w/ embedded flags)
    match_obj = re.findall(rawstr, docstring)

    for item in match_obj:
        
        d =  "{%s}" %(item)
        print d
        d1 = eval(d)
        
        print d1
        
        print type(d1)
    

if __name__ == "__main__":
    
    
    docstring = """
   bla
    input:
    {'workstation':'workstation'}
    output:
    {'data':'data'}
    bla
    """
    
    spec_parse(docstring)