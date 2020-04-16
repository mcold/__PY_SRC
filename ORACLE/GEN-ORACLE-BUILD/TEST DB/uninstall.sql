--Запускаем инициализацию параметров
@CONFIG.INI;

------------------------------------------------------------------
--Забираем права
------------------------------------------------------------------

--Подключение к БД
CONNECT &USR_SYS/&PWD_SYS@&SID AS SYSDBA;

--Запоминаем переменные окружения
STORE SET TO_INSTALL_PARAM.SQL REPLACE;

--Устанавливаем параметр
@TO_INSTALL_PARAM.SQL;

--Выдача прав пользователю
@.\Owner\UNINSTALL\INSTALL.SQL;

--Отключение
DISCONNECT;

------------------------------------------------------------------
--Откат системы 
------------------------------------------------------------------

--Подключение к БД
CONNECT &USR_SXM/&PWD_SXM@&SID;

--Запоминаем переменные окружения
STORE SET TO_INSTALL_PARAM.SQL REPLACE;

--Устанавливаем параметр
@TO_INSTALL_PARAM.SQL;

--Параметры сессии
@.\SQLsystem\SESSION_PARAMS.SQL;

--Java
@.\Java\INSTALL\INSTALL.SQL;

--JOB-ы
@.\Jobs\UNINSTALL\INSTALL.SQL;

--Метка
@.\Metka\UNINSTALL\INSTALL.SQL;

--Перекомпиляция объектов схемы
@.\SQLsystem\compile.sql;
@.\SQLsystem\compile_view.sql;

--Отключение
DISCONNECT;

--Завершение
EXIT;

------------------------------------------------------------------