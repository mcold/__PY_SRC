-- Установка переменных окружения для сессии установки патча

set echo off verify off linesize 100
set serveroutput on size 1000000

-- Перевод сессии SQL*Plus в режим продолжения в случае ошибки
-- с указанием не выполнять ни фиксацию, ни откат транзакции

whenever sqlerror continue none
