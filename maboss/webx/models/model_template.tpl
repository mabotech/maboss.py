#compiler-settings
cheetahVarStartToken = %%
directiveStartToken = $$
#end compiler-settings
# -*- coding: utf-8 -*-
   
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence
from sqlalchemy import Column, DateTime, Integer, String, Unicode

from datetime import datetime

from mabolab.database.dbsession import Base

from mabolab.database.model import ColumnMixin

## table_name, column_name, data_type, nullable, data_length,  COLUMN_ID, data_scale 
##          0              1                2              3              4              5                6

class %%{class_name}(Base, ColumnMixin):
    
    __tablename__ = '%%{table}'
    
$$for %%column in %%columns:   
$$if %%column[1] == 'ID' or %%column[1].lower() == %%table.replace('_',''):    
    %%{column[1].lower()}  = Column(Integer,  primary_key=True)
$$else if %%column[2] == 'FLOAT':
    %%{column[1].lower()}  = Column(Float)     # %%{column[2]}
$$else if %%column[2] == 'NUMBER':
    %%{column[1].lower()}  = Column(Integer) 
$$else if %%column[2] == 'DATE':
    %%{column[1].lower()}  = Column(DateTime)    # %%{column[2]}    
$$else if %%column[2] == 'NVARCHAR2' or %%column[2] == 'CHAR'  or %%column[2] == 'VARCHAR2':
    %%{column[1].lower()}  = Column(Unicode(%%{column[4]}))     # %%{column[2]}       
$$else:
    %%{column[1].lower()}  =   Column(Unicode(2000))  # %%{column[2]}
$$end if
$$end for


    def __init__(self, %%{params}, createdby):
        """init"""
        
$$for %%column in %%columns: 
    $$if %%column[1] != 'ID':
        self.%%{column[1].lower()}  = %%{column[1].lower()}
    $$end if
$$end for    

        self.createdby = createdby
        self.createdon = datetime.now()
        
        self.lastupdateon = datetime.now()
        self.lastupdatedby = createdby
        
        self.active = 1
        self.rowversionstamp = 1

    def __repr__(self):
        return %%{rtn}
