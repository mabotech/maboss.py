
-- drop table MT_T_WEIXIN

create table MT_T_WEIXIN (
    id                     int8 not null,
    msgclass               varchar(20)  null,  -- NVARCHAR
    msgid                  varchar(40)  null,  -- NVARCHAR
    msgtype                varchar(40)  null,  -- NVARCHAR
    fromusername           varchar(60)  null,  -- NVARCHAR
    tousername             varchar(60)  null,  -- NVARCHAR
    createtime             int8  null,  --BIGINT
    content                varchar(2000)  null,  -- NVARCHAR

    constraint   PK_WEIXIN primary key ( id ) 
);


CREATE SEQUENCE MT_SEQ_WEIXIN
  INCREMENT 1  MINVALUE 1 
  MAXVALUE 9223372036854775807  START 1000000
  CACHE 1; 

-------MT_INS_WEIXIN--------------------
CREATE OR REPLACE FUNCTION MT_INS_WEIXIN() RETURNS TRIGGER AS $BODY$ 
DECLARE ID INTEGER; 
BEGIN 
SELECT NEXTVAL('MT_SEQ_WEIXIN') INTO ID;
 NEW.ID := ID;
RETURN NEW;
END; 
$BODY$ LANGUAGE PLPGSQL; 
--------------

CREATE TRIGGER TG_MT_INS_WEIXIN
BEFORE INSERT ON MT_T_WEIXIN
FOR EACH ROW EXECUTE PROCEDURE MT_INS_WEIXIN(); 
-------------------END------------------------