
-- drop table GCIC_T_AVL_DATA

create table GCIC_T_AVL_DATA (
    id                     int8 not null,
    type                   int2  not null,  --SMALLINT
    status                 int2  not null,  --SMALLINT
    comments               varchar(1000)  null,  -- NVARCHAR
    testcell               varchar(40)  null,  -- NVARCHAR
    pallet                 varchar(40)  null,  -- NVARCHAR
    esn                    varchar(40)  null,  -- NVARCHAR
    testdate               timestamp  null,  --DATETIME
    speed                  numeric(18)  null,  -- NUMERIC
    pwr_kw                 numeric(18)  null,  -- NUMERIC
    torque                 numeric(18)  null,  -- NUMERIC
    bsfc                   numeric(18)  null,  -- NUMERIC
    fuel_rate              numeric(18)  null,  -- NUMERIC
    oil_filter_p           numeric(18)  null,  -- NUMERIC
    blowby_l_p             numeric(18)  null,  -- NUMERIC
    in_manifold_l_p        numeric(18)  null,  -- NUMERIC
    coolant_in_t           numeric(18)  null,  -- NUMERIC
    cell_air_t             numeric(18)  null,  -- NUMERIC
    fuel_in_p              numeric(18)  null,  -- NUMERIC
    fuel_in_t              numeric(18)  null,  -- NUMERIC
    fuel_out_p             numeric(18)  null,  -- NUMERIC
    coolant_out_t          numeric(18)  null,  -- NUMERIC
    coolant_out_p          numeric(18)  null,  -- NUMERIC
    coolant_in_p           numeric(18)  null,  -- NUMERIC
    smoke                  numeric(10)  null,  -- NUMERIC
    turbo_tur_out_l_t      numeric(10)  null,  -- NUMERIC
    turbo_tur_out_l_p      numeric(10)  null,  -- NUMERIC
    opacity                numeric(10)  null,  -- NUMERIC

    constraint   PK_AVL_DATA primary key ( id ) 
);


CREATE SEQUENCE GCIC_SEQ_AVL_DATA
  INCREMENT 1  MINVALUE 1 
  MAXVALUE 9223372036854775807  START 1000000
  CACHE 1; 

-------GCIC_INS_AVL_DATA--------------------
CREATE OR REPLACE FUNCTION GCIC_INS_AVL_DATA() RETURNS TRIGGER AS $BODY$ 
DECLARE ID INTEGER; 
BEGIN 
SELECT NEXTVAL('GCIC_SEQ_AVL_DATA') INTO ID;
 NEW.ID := ID;
RETURN NEW;
END; 
$BODY$ LANGUAGE PLPGSQL; 
--------------

CREATE TRIGGER TG_GCIC_INS_AVL_DATA
BEFORE INSERT ON GCIC_T_AVL_DATA
FOR EACH ROW EXECUTE PROCEDURE GCIC_INS_AVL_DATA(); 
-------------------END------------------------