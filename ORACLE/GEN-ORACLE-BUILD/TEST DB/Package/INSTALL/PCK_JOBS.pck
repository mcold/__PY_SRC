create or replace package PCK_JOBS is

/*
  ������ 3.4.1.0
  �������� �.�.
1. �������� ��������� job_register_revise. dbms_job.submit �������� �� dbms_scheduler.create_job
*/


--------------------------------------------------
--������� ���������� ������ ������
--------------------------------------------------
FUNCTION GetVersion RETURN VARCHAR2;
--------------------------------------------------

procedure job_register_revise(
  i_user   in varchar2 default 'job_register_revise'
);

procedure job_register_change_status(
  i_user   in varchar2 default 'job_register_change_status'
);

--------------------------------------------------
--�������� �������� ����������
--�������������� ��������� JOB ����� �������, ����� �� ���������� ���� ��� � ������,
--�.�. �������� �������� �������������� � �������
--------------------------------------------------
PROCEDURE JOB_Ch�ngeStatusTransaction
(
  IN_USER                    VARCHAR2 DEFAULT 'JOB_Ch�ngeStatusTransaction'                         --������������
);

end PCK_JOBS;
/
create or replace package body PCK_JOBS is

 --������ ������
  VERSION_PCK CONSTANT VARCHAR2(20):='3.4.1.0';
--�������� ������
  PACKAGE_NAME CONSTANT VARCHAR2(50):='PCK_JOBS';
--------------------------------------------------
--������� ���������� ������ ������
--------------------------------------------------
FUNCTION GetVersion RETURN VARCHAR2
IS
BEGIN
  RETURN VERSION_PCK;
END;

procedure job_register_revise(
  i_user   in varchar2 default 'job_register_revise'
)
is
  v_job         binary_integer;
  v_result      t_messages.code%type;
  v_err_message t_messages.description%type;
  v_count       number;
  v_num         number default 0;
begin
  v_count := pck_admin.GetParamStr('REC_COUNT_REGISTER', i_user);
  for rec in (select register_id from t_register where status=pck_register.lc_status_loaded and rownum<=v_count)
  loop
    pck_register.set_status_register(
      i_register_id => rec.register_id,
      i_status_new  => pck_register.lc_status_preparing,
      i_reason_code => 'OK',
      i_user        => i_user,
      o_result      => v_result,
      o_err_message => v_err_message
    );
    commit;
    if (v_result = 'OK') then
      v_num := v_num + 1;
      dbms_scheduler.create_job(job_name    => 'REGISTER_REVISE_' || v_num
                           ,job_type        => 'PLSQL_BLOCK'
                           ,job_action      => 'begin pck_register.revise(i_register_id => '||rec.register_id||', i_user => '''||i_user||'''); commit; end;'
                           ,start_date      => sysdate
                           ,enabled         => True
                           ,auto_drop       => True);
      commit;
    end if;
  end loop;
exception
  when others then
    pck_admin.SetLogErrorDB(to_char(SQLCODE),
                            'job'||' >> '||SQLERRM,
                            '������',
                            dbms_utility.format_call_stack,
                            dbms_utility.format_error_stack,
                            dbms_utility.format_error_backtrace,
                            i_user);
end;

procedure job_register_change_status(
  i_user   in varchar2 default 'job_register_change_status'
)
is
  v_count       number;
  v_result      t_messages.code%type;
  v_err_message t_messages.description%type;
begin
  v_count := pck_admin.GetParamStr('REC_COUNT_REGISTER', i_user);

  for rec_change_st in (select * from link_change_st_register where time_min_transition > 0)
  loop
    for rec in (select t.register_id
                  from t_register t
                 where t.status=rec_change_st.old_status_code
                   and t.status_date<=sysdate-rec_change_st.time_min_transition/1440
                   and rownum<=v_count)
    loop
      pck_register.set_status_register(
        i_register_id => rec.register_id,
        i_status_new  => rec_change_st.new_status_code,
        i_reason_code => 'OK',
        i_user        => i_user,
        o_result      => v_result,
        o_err_message => v_err_message
      );
      commit;
    end loop;
  end loop;
end;
--------------------------------------------------
--�������� �������� ����������
--�������������� ��������� JOB ����� �������, ����� �� ���������� ���� ��� � ������,
--�.�. �������� �������� �������������� � �������
--------------------------------------------------
PROCEDURE JOB_Ch�ngeStatusTransaction
(
  IN_USER                    VARCHAR2 DEFAULT 'JOB_Ch�ngeStatusTransaction'                         --������������
)
IS
  valRESULT                  T_MESSAGES.CODE%TYPE;
  valMESSAGE                 T_MESSAGES.DESCRIPTION%TYPE;
  valCOUNT_RED_STATUS_CHANGE NUMBER:=0;
  valSYSTIMESTAMP            TIMESTAMP:=SYSTIMESTAMP;
BEGIN
--�������� �� ������� ������� ������������
  valCOUNT_RED_STATUS_CHANGE:=NVL(PCK_ADMIN.GetParamInt('REC_COUNT_CHANGE_ST'), 0);
--�������� ��� ������� �� ������� ���������, ��� ����������� �����
  FOR REC_CHANGE_ST IN (SELECT * FROM LINK_CHANGE_ST_TRANS T WHERE T.TIME_MIN_TRANSITION > 0)
    LOOP
      --�������� ��� ����������, ������� ���������� � ���������� ������� ������ ������������ �������
      FOR REC_TRANS IN (SELECT TR.PAY_ID, TR.PAY_CTS, TR.STATUS_ID, TR.STATUS_DATE
                        FROM T_TRANSACTION TR
                        WHERE TR.STATUS_ID=REC_CHANGE_ST.OLD_STATUS_CODE
                        AND TR.STATUS_DATE <= valSYSTIMESTAMP-(REC_CHANGE_ST.TIME_MIN_TRANSITION/1440)
                        AND ROWNUM <= valCOUNT_RED_STATUS_CHANGE)
      LOOP
        --��������� ������ ����������
        PCK_TRANSACTION.SetStatusTransaction(REC_TRANS.PAY_ID,
                                             valSYSTIMESTAMP,
                                             REC_CHANGE_ST.NEW_STATUS_CODE,
                                             REC_CHANGE_ST.OLD_STATUS_CODE,
                                             NVL(IN_USER, USER),
                                             'OK_JOB_TIMING',
                                             valRESULT,
                                             valMESSAGE);
      END LOOP;
    END LOOP;
END;

end PCK_JOBS;
/
