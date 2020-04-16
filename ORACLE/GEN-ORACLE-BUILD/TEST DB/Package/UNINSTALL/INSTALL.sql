spool .\LOG\UNINSTALL\PACKAGE.LOG

SET DEFINE OFF

prompt
prompt Creating package PCK_JOBS
prompt =============================
prompt
@@pck_jobs.spc
@@pck_jobs.bdy
              
SET DEFINE ON

SPOOL OFF