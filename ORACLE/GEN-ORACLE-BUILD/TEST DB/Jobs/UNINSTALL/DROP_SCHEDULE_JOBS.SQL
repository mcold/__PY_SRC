begin
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
end;
/