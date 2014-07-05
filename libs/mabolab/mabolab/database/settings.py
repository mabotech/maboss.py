

from flask.config import Config


py = 'config.py'

root_path = ""

setting = Config(root_path)

setting.from_pyfile(py)

print setting['LOGGING']

print setting['PG_URL']

print setting['ORA_URL']