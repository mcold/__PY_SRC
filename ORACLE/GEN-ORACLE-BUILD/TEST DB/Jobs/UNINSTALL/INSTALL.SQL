spool .\LOG\INSTALL\JOBS.LOG

SET DEFINE OFF

prompt
prompt Drop previous JOBS created by DBMS_SCHEDULER
prompt ============================================
prompt
@@DROP_SCHEDULE_JOBS.SQL;


prompt
prompt Creating JOBS
prompt =============================
prompt
@@JOBS.SQL;


SET DEFINE ON

spool off