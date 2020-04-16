spool .\LOG\INSTALL\JOBS.LOG

SET DEFINE OFF

prompt
prompt Creating TRANSLATE JOBS FROM DBMS_JOB TO DBMS_SCHEDULER
prompt =======================================================
prompt
@@TRANSLATE_JOBS.SQL;


SET DEFINE ON

spool off