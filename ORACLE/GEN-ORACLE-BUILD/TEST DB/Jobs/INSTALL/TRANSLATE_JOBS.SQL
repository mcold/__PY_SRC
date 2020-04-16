begin
  -- óäàëÿåì ïðåäûäóùèå âåðñèè job-îâ
  for v_rec in (select aj.* 
                  from all_jobs aj 
                 where trim(';' from lower(aj.what)) in ('pck_jobs.job_changestatustransaction'
                                                        ,'pck_jobs.job_register_revise'
                                                        ,'pck_jobs.job_register_change_status'
                                                        ,'pck_kladr.load_dbf'))
  loop
    dbms_job.remove(job => v_rec.job);
  end loop;
  
  for v_rec in (select * 
                  from all_scheduler_jobs aj
                 where aj.job_name in ('JOB_CHANGE_STATUS_TRANSACTION'
                                      ,'JOB_REGISTER_REVISE'
                                      ,'JOB_REGISTER_CHANGE_STATUS'
                                      ,'LOAD_DBF'))
  loop
    dbms_scheduler.drop_job(job_name => v_rec.job_name);
  end loop;
  commit;
  
  dbms_scheduler.create_job(job_name        => 'JOB_CHANGE_STATUS_TRANSACTION'
                           ,job_type        => 'STORED_PROCEDURE'
                           ,job_action      => 'pck_jobs.JOB_ChàngeStatusTransaction'
                           ,start_date      => sysdate
                           ,repeat_interval => 'FREQ=MINUTELY;INTERVAL=1;'
                           ,enabled         => True);

  dbms_scheduler.create_job(job_name        => 'JOB_REGISTER_REVISE'
                           ,job_type        => 'STORED_PROCEDURE'
                           ,job_action      => 'pck_jobs.job_register_revise'
                           ,start_date      => sysdate
                           ,repeat_interval => 'FREQ=MINUTELY;INTERVAL=1;'
                           ,enabled         => True);
                           
  dbms_scheduler.create_job(job_name        => 'JOB_REGISTER_CHANGE_STATUS'
                           ,job_type        => 'STORED_PROCEDURE'
                           ,job_action      => 'pck_jobs.job_register_change_status'
                           ,start_date      => sysdate
                           ,repeat_interval => 'FREQ=MINUTELY;INTERVAL=1;'
                           ,enabled         => True);
                           
  dbms_scheduler.create_job(job_name         => 'LOAD_DBF'
                           ,job_type         => 'STORED_PROCEDURE'
                           ,job_action       => 'pck_kladr.load_dbf'
                           ,start_date       => sysdate
                           ,repeat_interval  => 'FREQ=DAILY;BYHOUR=2;'
                           ,enabled          => True);
                           
  
end;
/