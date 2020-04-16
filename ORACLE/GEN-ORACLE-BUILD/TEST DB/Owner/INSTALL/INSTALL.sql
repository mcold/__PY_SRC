spool .\LOG\INSTALL\OWNER.LOG

PROMPT ============================================================
prompt GRANT TO USER &USR_SXM
PROMPT ============================================================

grant execute on DBMS_SCHEDULER to &USR_SXM;
grant create job to &USR_SXM;


spool off
