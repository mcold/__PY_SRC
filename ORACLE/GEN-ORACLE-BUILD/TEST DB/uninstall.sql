--��������� ������������� ����������
@CONFIG.INI;

------------------------------------------------------------------
--�������� �����
------------------------------------------------------------------

--����������� � ��
CONNECT &USR_SYS/&PWD_SYS@&SID AS SYSDBA;

--���������� ���������� ���������
STORE SET TO_INSTALL_PARAM.SQL REPLACE;

--������������� ��������
@TO_INSTALL_PARAM.SQL;

--������ ���� ������������
@.\Owner\UNINSTALL\INSTALL.SQL;

--����������
DISCONNECT;

------------------------------------------------------------------
--����� ������� 
------------------------------------------------------------------

--����������� � ��
CONNECT &USR_SXM/&PWD_SXM@&SID;

--���������� ���������� ���������
STORE SET TO_INSTALL_PARAM.SQL REPLACE;

--������������� ��������
@TO_INSTALL_PARAM.SQL;

--��������� ������
@.\SQLsystem\SESSION_PARAMS.SQL;

--Java
@.\Java\INSTALL\INSTALL.SQL;

--JOB-�
@.\Jobs\UNINSTALL\INSTALL.SQL;

--�����
@.\Metka\UNINSTALL\INSTALL.SQL;

--�������������� �������� �����
@.\SQLsystem\compile.sql;
@.\SQLsystem\compile_view.sql;

--����������
DISCONNECT;

--����������
EXIT;

------------------------------------------------------------------