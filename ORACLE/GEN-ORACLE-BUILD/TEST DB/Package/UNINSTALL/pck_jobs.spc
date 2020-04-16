create or replace package PCK_JOBS is

--------------------------------------------------
--Функция возвращает версию пакета
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
--Переходы статусов транзакций
--Рекомендуеться настроить JOB таким образом, чтобы он запускался один раз в минуту,
--т.к. переходы статусов настраиваються в минутах
--------------------------------------------------
PROCEDURE JOB_ChаngeStatusTransaction
(
  IN_USER                    VARCHAR2 DEFAULT 'JOB_ChаngeStatusTransaction'                         --Пользователь
);

end PCK_JOBS;
/

