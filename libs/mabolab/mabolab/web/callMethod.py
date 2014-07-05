# -*- coding: utf-8 -*-

import xml.sax.saxutils as saxutils

# post xml soap message

import sys, httplib

from lxml import etree
from cStringIO import StringIO

import static

class CallMethod(object):
    
    def __init__(self):
        pass

    def getSessionToken(self):
        
        config = static.ERP_CONFIG # 'SL 8.0'
        
        SM_TEMPLATE = r"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <CreateSessionToken xmlns="http://frontstep.com/IDOWebService">
          <strUserId>%s</strUserId>
          <strPswd>%s</strPswd>
          <strConfig>%s</strConfig>
        </CreateSessionToken>
      </soap:Body>
    </soap:Envelope>"""  %(static.ERP_USER, static.ERP_PASSWD, config)

        SoapMessage = SM_TEMPLATE

        #print SoapMessage

        #construct and send the header

        host = static.ERP_HOST #"192.168.1.250" # "cnlyfs01"
        webservice = httplib.HTTP(host)
        webservice.putrequest("POST", "/idorequestservice/idowebservice.asmx")
        webservice.putheader("Host", host)
        webservice.putheader("User-Agent", "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.2;+SV1;+.NET+CLR+1.1.4322)")
        webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        webservice.putheader("Accept-Language", "en-us")
        webservice.putheader("Content-length", "%d" % len(SoapMessage))
        webservice.putheader("SOAPAction", "http://frontstep.com/IDOWebService/CreateSessionToken")
        webservice.endheaders()
        webservice.send(SoapMessage)

        # get the response

        statuscode, statusmessage, header = webservice.getreply()
        #print "Response: ", statuscode, statusmessage
        #print "headers: ", header
        
        res = webservice.getfile().read()
        
        print res
        
        print "--" *20

        return  self.parseSessionToken(res)
    
    def parseSessionToken(self, xmlstr):

        string_file = StringIO(xmlstr.replace('soap:',''))

        property = {}

        #root = etree.fromstring(xml)
        tree = etree.parse(string_file)

        SessionToken = None

        for element in tree.xpath('/Envelope/Body'):
            SessionToken = element[0][0].text
            
        return SessionToken    


    def buildParams(params_in):
        
        params_out = r"""<?xml version="1.0" encoding="utf-8"?>
        <Parameters>"""
       
        for item in params_in:
            v = """<Parameter ByRef="N">%s</Parameter>"""  % (item)
            params_out = params_out + v
            
        params_out = params_out + "</Parameters>"
        
        return params_out
            
            
        

    def callMethod(self, token, params):

        params_2 = r"""<?xml version="1.0" encoding="utf-8"?>
       <Parameters>
    <Parameter ByRef="N">1</Parameter>
    <Parameter ByRef="N">1</Parameter>
    <Parameter ByRef="N">      1</Parameter>
    <Parameter ByRef="N">1</Parameter>
    <Parameter ByRef="N">BJ00000002</Parameter>
    <Parameter ByRef="N">0</Parameter>
    <Parameter ByRef="N">10</Parameter>
    <Parameter ByRef="N">BOS-RM1</Parameter>
    <Parameter ByRef="N">EA</Parameter>
    <Parameter ByRef="N">MAIN</Parameter>
    <Parameter ByRef="N">2</Parameter>
    <Parameter ByRef="N">STOCK</Parameter>
    <Parameter ByRef="N">     2012090701</Parameter>
    <Parameter ByRef="N"></Parameter>
    <Parameter ByRef="Y"></Parameter>
       </Parameters>"""

        print params
        
        params = saxutils.escape(params)

        SM_TEMPLATE = r"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <CallMethod xmlns="http://frontstep.com/IDOWebService">
              <strSessionToken>%(token)s</strSessionToken>
              <strIDOName>SLDcjms</strIDOName>
              <strMethodName>DcJmcUpdateSp</strMethodName>
              <strMethodParameters>%(params)s</strMethodParameters>
            </CallMethod>
          </soap:Body>
        </soap:Envelope>"""  % {'token':token, 'params':params}

        SoapMessage = SM_TEMPLATE

        print SoapMessage

        #construct and send the header

        host = static.ERP_HOST #"192.168.1.250" # "cnlyfs01"
        webservice = httplib.HTTP(host)
        webservice.putrequest("POST", "/idorequestservice/idowebservice.asmx")
        webservice.putheader("Host", host)
        webservice.putheader("User-Agent", "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.2;+SV1;+.NET+CLR+1.1.4322)")
        webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        webservice.putheader("Accept-Language", "en-us")
        webservice.putheader("Content-length", "%d" % len(SoapMessage))
        webservice.putheader("SOAPAction", "http://frontstep.com/IDOWebService/CallMethod")
        webservice.endheaders()
        webservice.send(SoapMessage)

        # get the response

        statuscode, statusmessage, header = webservice.getreply()
        #print "Response: ", statuscode, statusmessage
        #print "headers: ", header
        res = webservice.getfile().read()

        #print '-'*20
        #print "done!"
        print res
        return res


    
    def getResponse(self, xmlstr):

        string_file = StringIO(xmlstr.replace('soap:',''))

        #root = etree.fromstring(xml)
        tree = etree.parse(string_file)

        resp = None

        for element in tree.xpath('/Envelope/Body'):
            resp = element[0][1].text
            
        return resp
        
    def getResult(self, xmlstr):
        
        resp = self.getResponse(xmlstr)
        
        string_file = StringIO(resp)

        #root = etree.fromstring(xml)
        tree = etree.parse(string_file)

        result = None
        
        v = tree.xpath('/Parameters')[0]
        
        l = len(v)
        
        result = v[l-1].text
        
        if result.count('successful') >0:
            return "S"
        else:
            return "F"    


def main():
    
    cm = CallMethod()
    
    xmlstr = cm.getSessionToken()
    
    
    print xmlstr
    
    token = cm.parseSessionToken(xmlstr)

    rtn = cm.callMethod(token, "")
    
    print cm.getResult(rtn)
    

    
 
    
if __name__ == '__main__':
    main()
