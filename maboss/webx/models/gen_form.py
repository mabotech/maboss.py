
from jinja2 import Environment, FileSystemLoader



 

loader  = FileSystemLoader("webx/templates")

env = Environment(loader=loader)

template = env.get_template('form.html')

print template.render(the='variables', go='here')