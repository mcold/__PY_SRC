set serveroutput on size 1000000
set feedback on
set termout on
set linesize 255 pagesize 100

SPOOL .\LOG\SQLSystem\COMPILE_VIEW.LOG

PROMPT ============================================================
PROMPT COMPILLING ALL VIEW
PROMPT ============================================================

declare
  cursor c
  is
    select   t.object_name, t.object_type
           , to_char( t.created, 'DD.MM.YYYY HH24:MI:SS' ) as created
           , to_char( t.last_ddl_time
             , 'DD.MM.YYYY HH24:MI:SS' ) as last_ddl_time
        from sys.user_objects t
       where t.status != 'VALID'
         and t.object_type = 'VIEW'
    order by t.object_type, t.object_name;
  r  c%rowtype;
begin
  open c;
  fetch c
   into r;
  if c%found then
    dbms_output.put_line
      (
      'OBJECT TYPE        OBJECT NAME                   CREATED              LAST DDL TIME        IS COMPILED '
    );
    dbms_output.put_line
      (
      '================== ============================= ==================== ==================== ============'
    );
    loop
      dbms_output.put_line( chr( 10 ) );
      dbms_output.put(
           rpad( r.object_type, 19 )
        || rpad( r.object_name, 30 )
        || rpad( r.created, 21 )
        || rpad( r.last_ddl_time, 21 )
      );
      begin
        execute immediate 'alter view ' || r.object_name || ' compile';
        dbms_output.put_line( 'compiled' );
      exception
        when others then
          dbms_output.put_line( 'not compiled' );
          dbms_output.put_line( 'errors:' );
          dbms_output.put_line( 'ln/pos  text' );
          for r1 in ( select  ue.line, ue.position, ue.text
                         from user_errors ue
                        where ue.name = r.object_name
                     order by ue.sequence ) loop
            dbms_output.put_line(
              substr( rpad( r1.line || '/' || r1.position, 8 ) || r1.text, 1, 255 )
            );
          end loop;
      end;
      fetch c
       into r;
      exit when c%notfound;
    end loop;
  end if;
  close c;
end;
/

SPOOL OFF
