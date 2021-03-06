
-- drop table MT_T_CERTIFICATE_PRINTM

create table MT_T_CERTIFICATE_PRINTM (

    constraint   PK_CERTIFICATE_PRINTM primary key ( id ) 
);


CREATE SEQUENCE MT_SEQ_CERTIFICATE_PRINTM
  INCREMENT 1  MINVALUE 1 
  MAXVALUE 9223372036854775807  START 1000000
  CACHE 1; 

-------MT_INS_CERTIFICATE_PRINTM--------------------
CREATE OR REPLACE FUNCTION MT_INS_CERTIFICATE_PRINTM() RETURNS TRIGGER AS $BODY$ 
DECLARE ID INTEGER; 
BEGIN 
SELECT NEXTVAL('MT_SEQ_CERTIFICATE_PRINTM') INTO ID;
 NEW.ID := ID;
RETURN NEW;
END; 
$BODY$ LANGUAGE PLPGSQL; 
--------------

CREATE TRIGGER TG_MT_INS_CERTIFICATE_PRINTM
BEFORE INSERT ON MT_T_CERTIFICATE_PRINTM
FOR EACH ROW EXECUTE PROCEDURE MT_INS_CERTIFICATE_PRINTM(); 
-------------------END------------------------