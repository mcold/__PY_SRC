create or replace package PCK_JOBS is

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

