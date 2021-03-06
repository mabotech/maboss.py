#compiler-settings
cheetahVarStartToken = $
directiveStartToken = %
#end compiler-settings
# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence

from sqlalchemy import Column

from sqlalchemy import BigInteger, Integer, SmallInteger
from sqlalchemy import DateTime, Float, String, Unicode

from datetime import datetime

from mabolab.database.dbsession import Base

## table_name, column_name, data_type, nullable, data_length,  COLUMN_ID, data_scale ,  column_signature
##          0              1                2              3              4              5                6

class ${class_name}(Base):
    
    __tablename__ = '${table}'
    
%for $column in $columns:
%if $column[1] != 0: 
%set $space = " " * (20 - len($column[1]) )
%if $column[1] == 'ID' or $column[1].lower() == $table.lower() + "_id":    
    ${column[1].lower()}  $space =  Column( BigInteger, primary_key=True )
%else:
    %if  $column[4] == None:
    ${column[1].lower()}  ${space} =  Column( ${mapping[$column[3]]} )  # ${column[2]}
    %else:
    ${column[1].lower()}  ${space} =  Column( ${mapping[$column[3]]}($column[4]) )  # ${column[2]}
    %end if
%end if
%end if
%end for


    def __init__(self):
        """init"""
        pass

##%for $column in $columns: 
##    %if $column[1] != 'ID':
##        self.${column[1].lower()}  = ${column[1].lower()}
##    %end if
##%end for    


    def __repr__(self):
        return ${rtn}
