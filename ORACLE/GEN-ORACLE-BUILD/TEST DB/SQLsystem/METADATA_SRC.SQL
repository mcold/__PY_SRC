
REM Имя файла куда записать
SPOOL &3/&1..&5
REM Не выводить на экран строки, которые записываются в файл (OFF - не выводить; ON - выводить)
SET TERMOUT OFF 
REM Управляет выдачей на экран каждой команды в командном файле, выполняемом с помощью 
SET ECHO OFF
REM Позволяет включать и отключать выдачу каждой строки команды до и после подстановки пользовательских переменных
SET VERIFY OFF
REM Усекает конечные пробелы
SET TRIMSPOOL ON
REM Управляет усечением слишком длинных строк результатов. По умолчанию, остатки строк переносятся на следующую строку. При задании значения OFF - усекаются.
SET WRAP ON
SET PAGESIZE 0
SET FEEDBACK OFF
SET PAUSE OFF
SET LINESIZE 200

SELECT 'SPOOL &4/&1&5..LOG' FROM DUAL
UNION ALL
SELECT ' ' FROM DUAL
UNION ALL
SELECT 'PROMPT ============================================================' FROM DUAL
UNION ALL
SELECT 'PROMPT &2 &1 '||TO_CHAR(SYSDATE, 'DD.MM.YYYY HH24:MI:SS') FROM DUAL
UNION ALL
SELECT 'PROMPT ============================================================' FROM DUAL
UNION ALL
SELECT ' ' FROM DUAL;

SELECT TEXT FROM
(
  SELECT
    DECODE(US.LINE, 1,'CREATE OR REPLACE '||US.TEXT,
           US.TEXT) AS TEXT 
  FROM USER_SOURCE US
  WHERE US.NAME='&1' AND US.TYPE='&2'
  ORDER BY US.LINE
)
UNION ALL
SELECT '/' FROM DUAL;

SELECT ' ' FROM DUAL
UNION ALL
SELECT 'SPOOL OFF' FROM DUAL;

SPOOL OFF;