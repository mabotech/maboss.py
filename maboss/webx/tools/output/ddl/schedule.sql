
-- drop table SCHEDULE

create table SCHEDULE (

    constraint   PK_SCHEDULE primary key ( id ) 
);


CREATE SEQUENCE SEQ_SCHEDULE
  INCREMENT 1  MINVALUE 1 
  MAXVALUE 9223372036854775807  START 1000000
  CACHE 1; 

-------INS_SCHEDULE--------------------
CREATE OR REPLACE FUNCTION INS_SCHEDULE() RETURNS TRIGGER AS $BODY$ 
DECLARE ID INTEGER; 
BEGIN 
SELECT NEXTVAL('SEQ_SCHEDULE') INTO ID;
 NEW.ID := ID;
RETURN NEW;
END; 
$BODY$ LANGUAGE PLPGSQL; 
--------------

CREATE TRIGGER TG_INS_SCHEDULE
BEFORE INSERT ON SCHEDULE
FOR EACH ROW EXECUTE PROCEDURE INS_SCHEDULE(); 
-------------------END------------------------