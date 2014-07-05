#-*- coding: utf-8 -*-

"""A basic example of using the association object pattern.

The association object pattern is a richer form of a many-to-many
relationship.

The model will be an ecommerce example.  We will have an Order, which
represents a set of Items purchased by a user.  Each Item has a price.
However, the Order must store its own price for each Item, representing
the price paid by the user for that particular order, which is independent
of the price on each Item (since those can change).
"""

#import logging
from datetime import datetime

from itertools import count

from sqlalchemy import *

from sqlalchemy.orm import *
from sqlalchemy.exc import *

#from common.singleton import Singleton

#from db.model_dicts import *

# Uncomment these to watch database activity.
#logging.basicConfig(format='%(message)s')
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class Perfline:

    def __init__(self):
        pass

class PerfDB:

    #__metaclass__ = Singleton

    def __init__(self, echo = False):
        #print "create engine"
        uri = 'sqlite:///perf01.db'
        #uri = 'mysql://root:myjsy03bjwqt@127.0.0.1:3336/vpipe?charset=utf8&use_unicode=0'
        self.engine = create_engine(uri,encoding='utf-8')
        metadata = MetaData()
        metadata.bind = self.engine
        metadata.bind.echo  = echo
        self.connection = None

        self.perflines = Table('perflines', metadata,
            Column('level', Integer, nullable=False),
            Column('createdon', DateTime, nullable=False),
            Column('duration', Float, nullable=False),
            Column('logger', String(100), nullable=False),
            Column('type', String(20), nullable=False),
            Column('message', String(100), nullable=False),

            )



        self.perflines.create()
        """

        metadata.create_all()

        mapper(Perfline, self.perflines)
        """
        self.session = create_session()


    def execute(self, sql):
        #sql = sql.replace("'","''")
        self.connection = self.engine.connect()
        result = self.connection.execute(sql)
        return result

    def fetchone(self):
        return self.connection.fetchone()

    def fetchall(self):
        return self.connection.fetchall()


if __name__ =="__main__":

        pobj = PerfDB()

        f = file('FlexNet_PerformanceRolling1.log','r')
        i = 0
        for line in f:
            i = i + 1

            if i > 500:
                break
            ar =  line.split('\t')
            if len(ar) == 5:
                #print len(ar),
                msg = ar[4].split(':')
                if len(msg) >= 2:
                    #print msg[0],msg[-1].strip(),msg
                    sql = "insert into perflines values('%s','%s','%s','%s','%s','%s')" %(ar[0], ar[1], ar[2].strip(), ar[3], msg[0],msg[-1].strip())
                else:
                    sql = "insert into perflines values('%s','%s','%s','%s','%s','%s')" %(ar[0], ar[1], ar[2].strip(), ar[3], '',msg[0].strip())

                pobj.execute(sql)

            else:
                continue
        #sql = """insert into perflines values(10, '2009-07-08 09:02:08,764',1.2023,'logger','step','open')"""
        #

