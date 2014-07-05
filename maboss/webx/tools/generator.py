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

from schedule import Schedule

settings = Config("" )

settings.from_pyfile( 'C:/MTP/mabotech/maboss1.3.0/maboss/conf/tools_config.py')

settings['APP_NAME'] = "mabozen"

base = Base( settings)

db_type = 'postgresql'

db = base.get_db(db_type) 


def render(template_file, name_space):
    """
    template file render
    """
    tpt = Template(file=template_file, searchList=[name_space])
    return str(tpt)
    

def get_meta_ora(table_name):

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
    
    return columns   

def get_meta_pg(table_name):
    
    project = 'avl'
    project_revision = 1000004
    

    sql = """
SELECT  table_name, column_name, 
            data_type, not_null, width, scale, default_value, ispk, pkposition, 
            isfk, fkposition, project, fk_project_revision, ordering, iscommon, 
            tab, defination
            FROM mt_t_column where table_name = '%s'  and active =1 and (fkposition is null or fkposition < 2)
            and iscommon = 0
            and project = '%s'  and fk_project_revision = %s  order by ordering   
    """ % (table_name, project, project_revision)
    #and iscommon =0
    rtn = db.session.execute(sql)

    columns = rtn.fetchall()
    
    print "=="*20
    print sql
    print columns
    
    return columns  

def get_schema_pg(table_name):
    

    

    sql = """
select table_name, column_name, data_type, udt_name from information_schema.columns
where table_schema = 'public' and table_name = '%s'
order by ordinal_position
    """ % (table_name)
    #and iscommon =0
    rtn = db.session.execute(sql)

    columns = rtn.fetchall()
    
    print "=="*20
    print sql
    print columns
    
    return columns  

def get_mapping(platform):
    
    dt = {}
    
    dt[platform] ={}
    
    sql = "select alias from mt_t_db_platform where name = '%s'" %(platform)
    
    rtn = db.session.execute(sql)
    
    
    row = rtn.fetchone()
    
    db_platform_id =  row[0]
    
    
    sql = """select d.datatypename, dt.datatypename from mt_t_datatype d 
left join mt_t_db_datatype dt on d.id = dt.fk_datatype and dt.fk_db_platform = %s """ % (db_platform_id)

    rtn = db.session.execute(sql)
    
    
    rows = rtn.fetchall()
    
    for row in rows:
        dt[platform][row[0]] = row[1]
        
    
    #print dt
    
    return dt[platform]

    
    
def get_class_name(table_name):
    
    if table_name.count('_T_') == 1:
        cls_name = table_name.split('_T_')[1].lower()
        
        cls_name_s = cls_name.split('_')
        
        class_name = ''.join( map(lambda x: x.capitalize() ,cls_name_s) )   
    else:
        cls_name = table_name.lower()
        class_name = table_name.capitalize() 
    
    return cls_name, class_name
    
def gen_model(table_name, columns, mapping):

    cls_name, class_name = get_class_name(table_name)

    params = []
    self_params = []
    self_p = []
    
    #print columns
    
    for col in columns:
        if col[1] != 'ID':
            params.append(col[1].lower())
            self_params.append('self.'+col[1].lower())
            self_p.append("'%s'")
            
    params_str = ', '.join(params)
    attrs = ', '.join(self_params)
    att_ct = ', '.join(self_p)
    
    rtn = '"<%s(%%s, %s)>" \\\n            %% (self.id, %s)' % (class_name, att_ct, attrs)


    name_space = {'class_name': class_name, 'table': table_name.lower(), 'columns':columns, 'mapping':mapping,
                            'params':params_str, 'rtn':rtn }

    template_file = 'templates/model.py'
    model = render(template_file, name_space)
    
    write_output('models', cls_name, model)

def gen_ddl(table_name, columns, mapping):

    cls_name, class_name = get_class_name(table_name)

    params = []
    self_params = []
    self_p = []
    
    #print columns
    
    for col in columns:
        if col[1] != 'ID':
            params.append(col[1].lower())
            self_params.append('self.'+col[1].lower())
            self_p.append("'%s'")
            
    params_str = ', '.join(params)
    attrs = ', '.join(self_params)
    att_ct = ', '.join(self_p)
    
    rtn = '"<%s(%%s, %s)>" \\\n            %% (self.id, %s)' % (class_name, att_ct, attrs)


    name_space = {'class_name': class_name, 'table': table_name.upper(), 'columns':columns, 'mapping':mapping,
                            'params':params_str, 'rtn':rtn }

    template_file = 'templates/ddl.sql'
    model = render(template_file, name_space)
    
    write_output('ddl', cls_name, model)
    
    
    
def write_output(otype, cls_name, output):
    
    
    if otype == 'models':
        t = 'py'
    elif otype == 'forms':
        t = 'html'
        
    elif otype == 'controllers':
        t = 'js'

    elif otype == 'ddl':
        t = 'sql'        
        
    fn = "output/%s/%s.%s" % (otype, cls_name, t)

    fh = open(fn, 'w')
     
    fh.write(output)

    fh.close()  
    
def gen_form(table_name, columns):
    
    cls_name, class_name = get_class_name(table_name)
    
    name_space = {'class_name': class_name, 'table': table_name.lower(), 'columns':columns}

    template_file = 'templates/form.html'

    form = render(template_file, name_space)    
    
    write_output('forms', cls_name, form)
    
def gen_js(table_name, columns):
    
    cls_name, class_name = get_class_name(table_name)
    
    name_space = {'class_name': class_name, 'table': table_name.lower(), 'columns':columns}

    template_file = 'templates/controller.js'

    form = render(template_file, name_space)    
    
    write_output('controllers', cls_name, form)
    
    
def gen_doc(table_name, columns):
    pass
    
def gen(table_name):
    
    #db_type = 'oracle'  

    platform = 'SQLAlchemy'
    
    mapping = get_mapping(platform)

    platform = 'PostgreSQL 8.0'
    
    ddl_mapping = get_mapping(platform)
    
    
    if db_type == 'oracle':
        columns = get_meta_ora(table_name)
    else:
        columns = get_meta_pg(table_name)       
    
    gen_model(table_name, columns, mapping)
    
    gen_ddl(table_name, columns, ddl_mapping)
    
    gen_form(table_name, columns)
    
    gen_js(table_name, columns)
    

def main():
    
    table_names  = ['GCIC_T_AVL_DATA','avl_oee_period']#, 'MT_T_WORKSTATION_PRINTER','MT_T_CERTIFICATE','MT_T_CERTIFICATE_PRINTM']
                            #'MT_T_CERTIFICATE_MP' #'MT_T_CERTIFICATE'


    
    
    for table_name in table_names:
        gen(table_name)
        pass
        
    
    
if __name__ == '__main__':
    main()