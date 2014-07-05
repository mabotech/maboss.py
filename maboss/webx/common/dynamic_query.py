

import re

import logging
import logging.handlers
import logging.config

log = logging.getLogger(__name__)


def get_conditions(request, query_col, table_alias,  db_type):
    
    
    log.debug(request.form )
    
    query_str = request.form.get('search','')
    
    page =  request.form.get('page', 1, type=int) 
    limit = request.form.get('limit', 15, type=int)
    
    date_from = request.form.get('date_from', '')
    date_to = request.form.get('date_to','')
    
    sort_by =   request.form.get('sort_by','')
    sort_order =  request.form.get('sort_order','ASC')
    
    where = []
    
    if query_str != '':        
        where.append("%s like '%%%s%%'"  % (query_col, query_str) )       
    
    
    if db_type == 'oracle':
        if date_from != '':
             where.append( "%s.lastupdateon >= to_date('%s:00:00:00','YYYY-MM-DD HH24:MI:SS')" %(table_alias, date_from) )
        if date_to != '':
            where.append( "%s.lastupdateon <= to_date('%s 23:59:59', 'YYYY-MM-DD HH24:MI:SS')" %(table_alias, date_to))
    else:
        if date_from != '':
             where.append( "%s.lastupdateon >= '%s 00:00:00'" %(table_alias, date_from) )
        if date_to != '':
            where.append( "%s.lastupdateon <= '%s 23:59:59'" %(table_alias, date_to) )       

    if len(where)>0:
        where_clause = ' and '.join(where)
    else:
        where_clause = None
    
    orderby = " order by certv.lastupdateon desc"
    
    log.debug(sort_by)
    
    if sort_by != '':
        #split and get the column name
        colname = sort_by.replace("_",".",1) # re.split('_', sort_by) 
        orderby = " order by %s %s" % (colname, sort_order)
        
    return (page, limit, where_clause, orderby)
