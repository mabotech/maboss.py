#

CENTRAL_CONFIG = 'C:/MTP/mabotech/maboss1.3.0/maboss/configuration/central_config.py'

SERVICE_NAME = '_MaboTech_Scheduler'

SERVICE_DESC = 'MaboTech_Scheduler'

#JobExecutor Endpoint
ENDPOINT = "tcp://127.0.0.1:62001"

#DB url for testing
#DB_URL = 'oracle+cx_oracle://flxuser:flxuser@localhost:1521/mesdb?charset=utf8'

DB_URL = 'postgresql+psycopg2://postgres:py03thon@localhost:5432/maboss'

DB_ECHO = True