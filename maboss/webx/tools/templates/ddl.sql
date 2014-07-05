#compiler-settings
cheetahVarStartToken = @
directiveStartToken = #
#end compiler-settings

-- drop table @table

create table @table (
#####################################################
#if @table.count('_T_') == 0:
#set @pk = 'PK_' + @table
#else:
#set @pk = 'PK_' + @table.split('_T_')[1]
#end if
#####################################################
#for @column in @columns:
#set @space = " " * (20 - len(@column[1]) )
#if @column[3] == 0:
#set @nullable = 'null'
#else:
#set @nullable = 'not null'
#end if
#if @column[1] == 'ID':    
    id @space  int8 not null,
#else:
    #if  @column[4] == None:
    @{column[1].lower()} @space  @{mapping[@column[2]]}  @{nullable},  --@{column[2]}
    #else:
    @{column[1].lower()} @space  @{mapping[@column[2]]}(@column[4])  @{nullable},  -- @{column[2]}
    #end if
#end if
#end for

    constraint   @{pk} primary key ( id ) 
);

#####################################################
#if @table.count('_T_') == 0:
#set @seq= 'SEQ_' + @table
#set @tg= 'INS_' + @table
#set @pk = 'PK_' + @table
#else:
#set @seq =  @table.replace('_T_','_SEQ_')
#set @tg =  @table.replace('_T_','_INS_')
#set @pk = 'PK_' + @table.split('_T_')[1]
#end if
#####################################################

CREATE SEQUENCE @seq
  INCREMENT 1  MINVALUE 1 
  MAXVALUE 9223372036854775807  START 1000000
  CACHE 1; 

-------@tg--------------------
CREATE OR REPLACE FUNCTION @{tg}() RETURNS TRIGGER AS $BODY$ 
DECLARE ID INTEGER; 
BEGIN 
SELECT NEXTVAL('@{seq}') INTO ID;
 NEW.ID := ID;
RETURN NEW;
END; 
$BODY$ LANGUAGE PLPGSQL; 
--------------

CREATE TRIGGER TG_@{tg}
BEFORE INSERT ON @{table}
FOR EACH ROW EXECUTE PROCEDURE @{tg}(); 
-------------------END------------------------