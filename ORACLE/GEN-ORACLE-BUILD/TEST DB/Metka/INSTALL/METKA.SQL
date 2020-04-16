PROMPT ============================================================
PROMPT ADD METKA
PROMPT ============================================================

DECLARE 
  valSYSDATE DATE;
BEGIN
--Инициализация
  valSYSDATE:=SYSDATE;
  
  WHILE valSYSDATE = SYSDATE
    LOOP
      BEGIN
        NULL;
      END;
    END LOOP;
  DBMS_OUTPUT.PUT_LINE(TO_DATE(valSYSDATE, 'DD.MM.YYYY HH24:MI:SS') ||' '||TO_DATE(SYSDATE, 'DD.MM.YYYY HH24:MI:SS'));  
    
END;
/

INSERT INTO T_ABOUT (VERSION, INSTALL_DATE, DESCRIPTION, USER_CREATE, DATE_CREATE)
VALUES ('&PATH_VERSION', SYSDATE, '&PATH_DESCR', USER, SYSDATE);

COMMIT;