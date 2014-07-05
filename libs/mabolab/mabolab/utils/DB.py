


from sqlalchemy import create_engine

from singleton import Singleton

class DB:

  __metaclass__ = Singleton

  def __init__(self, url ):
    engine = create_engine(url)
    self.connection = engine.connect()
    pass

  def execute(self, sql):
    return self.connection.execute(sql)


def main():

  url = 'postgres://postgres:cormor03$@localhost:5432/kserver'
  sql = """select * from service_states"""
  db = DB(url)
  rt = db.execute(sql)
  for row in rt:
    print row


if __name__ == '__main__':
  main()
