
import pyRXP

#import os, string, sys
#from types import StringType, ListType, TupleType
#import pprint




class LinksParser:

    def __init__(self):


        self.links = []
        self.p = 0
        self.count = 0

    def xml2doctree(self, xml):
        pyRXP_parse = pyRXP.Parser(
            ErrorOnValidityErrors=1,
            NoNoDTDWarning=1,
            ExpandCharacterEntities=0,
            ExpandGeneralEntities=0)
        return pyRXP_parse.parse(xml)


    def getParsed(self):
        return self.parsed

    def parse(self, xml):

        self.parsed = self.xml2doctree(xml)

        return self.parsed

    def getNode(self, node):

        for item in node:
            if isinstance(item, list) or isinstance(item, tuple):

                if item[0] == 'StepLinks':
                    self.p = 1
                if item[0] == 'StepPositions':
                    self.p = 2

                if item[0] == 'anyType' and  self.p == 1:
                    #print item
                    self.link(item)  # anytype node under StepLinks
                    self.count = self.count + 1
                else:
                    self.getNode(item)
            else:
                #print item
                pass

    def link(self, node):

        for item in node:

            FlowFunctionOutputValue =''

            if isinstance(item, list):

                for y in item:
                    if isinstance(y, tuple):
                        if y[0] == 'SourceStepID':
                            SourceStepID = y[2][0]
                        elif y[0] == 'DestinationStepID':
                            DestinationStepID = y[2][0]
                        elif y[0] == 'FlowFunctionOutputValue':
                            if  y[2] == None:
                                FlowFunctionOutputValue = ''
                            else:
                                FlowFunctionOutputValue = y[2][0]
                link = (SourceStepID,DestinationStepID, FlowFunctionOutputValue)
                self.links.append(link)


    def graph(self, xml):

        anyTypes = None
        self.parsed = self.xml2doctree(xml)

        for item in self.parsed:

            if isinstance(item, list):

                for v in item:

                    if v[0] == 'StepLinks':

                        for node in v:
                            if isinstance(node, list):
                                for nodel2 in node:
                                    if nodel2[0] == 'anyType':
                                    #if isinstance(nodel2, tuple):
                                        for x in nodel2:
                                            FlowFunctionOutputValue =''

                                            if isinstance(x, list):

                                                for y in x:
                                                    if isinstance(y, tuple):
                                                        if y[0] == 'SourceStepID':
                                                            SourceStepID = y[2][0]
                                                        elif y[0] == 'DestinationStepID':
                                                            DestinationStepID = y[2][0]
                                                        elif y[0] == 'FlowFunctionOutputValue':
                                                            if  y[2] == None:
                                                                FlowFunctionOutputValue = ''
                                                            else:
                                                                FlowFunctionOutputValue = y[2][0]
                                                link = (SourceStepID,DestinationStepID, FlowFunctionOutputValue)
                                                self.links.append(link)
                        #print v


        """
        for anyType in anyTypes:
            #print anyType
            if anyType != None:
                if isinstance(anyType, list):
                    for item in anyType:
                        if isinstance(item, tuple):
                            if len(item[2]) == 13:
                                if item[2][7][2] == None:
                                    val= ''
                                else:
                                    val =  item[2][7][2][0]
                            else:
                                val = ''
                            if isinstance(item[2], list):
                                print item[2]
                                SourceStepID = item[2][1][2][0]
                                print type(item[2][3][2])
                                DestinationStepID = item[2][3][2][0]
                                link = (SourceStepID,DestinationStepID, val)
                                self.links.append(link)
        """



        return self.links

if __name__=='__main__':

    fn = 'COB_SO_SubAssmMgmt27.xml'
    #fn = 'wp27.xml'
    xml = file(fn,'r').read()
    ld = LinksParser()
    #print ld.graph(xml)
    root = ld.parse(xml)
    ld.getNode(root)
    print ld.count
    print ld.links
    for item in ld.links:
        #print item
        pass
