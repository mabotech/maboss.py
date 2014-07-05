

from jinja2 import Environment, FileSystemLoader



 

loader  = FileSystemLoader("webx/templates")

env = Environment(loader=loader, trim_blocks=True, lstrip_blocks = True)

template = env.get_template('form.html')

v = template.render(name_space)



fn = "output/forms/%s.html" % (cls_name)

fh = open(fn, 'w')
 
fh.write(v)

fh.close() 