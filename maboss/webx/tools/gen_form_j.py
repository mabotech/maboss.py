
from jinja2 import Environment, FileSystemLoader



 

loader  = FileSystemLoader("templates")

env = Environment(loader=loader)

template = env.get_template('form.html,tpl')

print template.render(the='variables', go='here')