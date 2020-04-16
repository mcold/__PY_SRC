declare
  job number;
begin
  sys.dbms_job.submit(job,
                      what => 'PCK_JOBS.JOB_ChàngeStatusTransaction;',
                      next_date => SYSDATE,
                      interval => 'SYSDATE+60/86400');
  commit;
end;
/

declare
  job number;
begin
  sys.dbms_job.submit(job,
                      what => 'PCK_JOBS.job_register_revise;',
                      next_date => SYSDATE,
                      interval => 'SYSDATE+60/86400');
  commit;
end;
/

declare
  job number;
begin
  sys.dbms_job.submit(job,
                      what => 'pck_jobs.job_register_change_status;',
                      next_date => SYSDATE,
                      interval => 'SYSDATE+60/86400');
  commit;
end;
/

declare
  job number;
begin
  sys.dbms_job.submit(job,
                      what => 'pck_kladr.load_dbf;',
                      next_date => SYSDATE,
                      interval => 'trunc(sysdate) + 1 + 2/24');
  commit;
end;
/
