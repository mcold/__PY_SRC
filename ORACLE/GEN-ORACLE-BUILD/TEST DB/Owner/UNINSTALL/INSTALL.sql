spool .\LOG\INSTALL\OWNER.LOG

PROMPT ============================================================
prompt GRANT TO USER &USR_SXM
PROMPT ============================================================

revoke execute on DBMS_SCHEDULER from &USR_SXM;
revoke create job from &USR_SXM;

spool off
