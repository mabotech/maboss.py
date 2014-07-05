
import time

class DataProvider:

    def __init__(self,**paras):
        #print paras
        self.name = paras['name']
        self.value = paras['value']

    def getKeys(self):
        pass

    def getResult(self):
        return (self.name, self.value)



    def execute(self):
        pass

    def getData(self, attr):

        return getattr(self, attr)



if __name__ == "__main__":

    start = time.time()

    paras = {'name': 'idea', 'value': 'test'}


    #import DataProvider
    cmd ="""DataProvider(name='idea', value='test')"""

    classname = cmd.split('(')[0]

    classfile = classname.lower().strip()

    print "from kserver.lib.%s import %s" %(classfile, classname)



    #DataProvider(name=@name, value=@value)
    cmd = """dp = DataProvider(name='%(name)s', value='%(value)s')"""%paras

    print cmd

    exec(cmd)


    v = dp.getData('value')

    print dp.getResult()

    print "v:[%s]"%(v)

    print time.time() - start



