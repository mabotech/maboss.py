# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers
import logging.config
#import profile
import time
from time import strftime, localtime

from Cheetah.Template import Template

from mabolab.core.base import Base

from flask.config import Config

settings = Config("" )

settings.from_pyfile( 'C:/MTP/mabotech/maboss1.2/maboss/configuration/central_config.py')

settings['APP_NAME'] = "mabozen"

base = Base( settings)
db = base.get_db("oracle") 


def render(template_file, name_space):
    """
    template file render
    """
    tpt = Template(file=template_file, searchList=[name_space])
    return str(tpt)
    

def gen(table_name):

    sql = """select atc.table_name, atc.column_name,
     atc.data_type,atc.nullable,  atc.data_length/2 AS data_length,  atc.COLUMN_ID as COLUMN_ID ,
                atc.data_scale , atc.data_default as default_value, 
               
                acc.comments as column_desc
                from all_tab_columns  atc 
                inner join all_col_comments acc
                on (acc.owner = atc.owner and acc.table_name = atc.table_name and acc.column_name = atc.column_name)
                where atc.owner = 'FLXUSER' and 
                atc.table_name = '%s' 
                  and atc.column_name not in ('ACTIVE', 'REFERENCEID','LASTUPDATEON','LASTUPDATEDBY','CREATEDON','CREATEDBY',
    'LASTDELETEON','LASTDELETEDBY','LASTREACTIVATEON','LASTREACTIVATEDBY','ARCHIVEID','LASTARCHIVEON',
    'LASTARCHIVEDBY', 'LASTRESTOREON','LASTRESTOREDBY','ROWVERSIONSTAMP')   
                ORDER BY atc.COLUMN_ID""" % (table_name.upper())
                

    rtn = db.session.execute(sql)

    columns = rtn.fetchall()

    cls_name = table_name.split('_T_')[1].lower()
    
    cls_name_s = cls_name.split('_')
    
    class_name = ''.join( map(lambda x: x.capitalize() ,cls_name_s) )
    
    
    

    params = []
    self_params = []
    self_p = []
    for col in columns:
        if col[1] != 'ID':
            params.append(col[1].lower())
            self_params.append('self.'+col[1].lower())
            self_p.append("'%s'")
            
    params_str = ', '.join(params)
    attrs = ', '.join(self_params)
    att_ct = ', '.join(self_p)
    
    rtn = '"<%s(%%s, %s)>" \\\n            %% (self.id, %s)' % (class_name, att_ct, attrs)


    name_space = {'class_name': class_name, 'table': table_name.lower(), 'columns':columns, 
                            'params':params_str, 'rtn':rtn }

    template_file = 'model_template.tpl'

    model = render(template_file, name_space)



    fn = "output/%s.py" % (cls_name)

    fh = open(fn, 'w')
     
    fh.write(model)

    fh.close()  
    
    ###
    

    from jinja2 import Environment, FileSystemLoader



     

    loader  = FileSystemLoader("webx/templates")

    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks = True)

    template = env.get_template('form.html')

    v = template.render(name_space)



    fn = "output/forms/%s.html" % (cls_name)

    fh = open(fn, 'w')
     
    fh.write(v)

    fh.close()      
    


def main():
    
    table_names  = ['MT_T_WORKSTATION_PRINTER','MT_T_CERTIFICATE','MT_T_CERTIFICATE_PRINTM',
                            'MT_T_SERIAL_MODEL','MT_T_PRODUCTION_LICENSE','MT_T_PRODUCTION_LIC_HIS']
                            #'MT_T_CERTIFICATE_MP' #'MT_T_CERTIFICATE'

    for table_name in table_names:
        gen(table_name)
    
    
if __name__ == '__main__':
    main()