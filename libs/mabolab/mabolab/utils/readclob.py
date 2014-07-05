


from sqlalchemy import create_engine


class DB:
  def __init__(self):
    engine = create_engine('oracle://flxuser:flxuser@messpdb')
    self.connection = engine.connect()
    pass

  def execute(self, sql):
    return self.connection.execute(sql)


def main():
  
  sql = """select id, fuid, stepsflow from operation where operationcode = 'COB_SO_WS_OPERATION' order by id desc"""
  db = DB()
  rt = db.execute(sql)
  for row in rt:
    print row['stepsflow'].read()
    break


if __name__ == '__main__':
  main()
