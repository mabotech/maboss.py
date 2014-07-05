
import re

class SQLParser:

    def __init__(self, sql):
        self.sql = sql

        self.paras = None

        self.num_para =  sql.count('@')  # @ only  be used as the parameter identify

        self.rawstr = ''
        s = '.*?@(\w+)'

        self.d = {}

        for i in range(0,self.num_para):
            self.rawstr = "%s%s" %(self.rawstr , s)

        compile_obj = re.compile(self.rawstr,re.DOTALL)
        match_obj = compile_obj.search(self.sql)


        self.all_groups = None

        if match_obj != None:
            self.all_groups = match_obj.groups()

    def getArgs(self):
        args = set()
        for item in self.all_groups:
            args.add(item)
        return args

    def getSQL(self):

        for item in self.all_groups:
            ori = '@%s' %(item)
            val = "%%(%s)s"%(item)
            self.sql = self.sql.replace(ori,val)

        return self.sql

    def setParas(self,paras):
        self.paras = paras

    def apply(self):

        for g in self.all_groups:
            #print g
            if self.d.has_key(g):
                pass
            else:
                if self.paras.has_key(g):
                    self.d[g] = self.paras[g]
                else:
                    raise Exception('no value assigned')

    def test(self,dd):
        self.setParas(dd)
        self.apply()
        sql = self.sql %self.paras
        return {'sql':sql, 'parameters':self.d}



if __name__ == "__main__":

        sql = """select sysdate from dual where user = '@username' and password='@password' or username='@username' """

        sp = SQLParser(sql)
        print sp.getArgs()
        print sp.getSQL()

        dd =  {'username':'aidear', 'password':'idea'}

        print sp.test(dd)



