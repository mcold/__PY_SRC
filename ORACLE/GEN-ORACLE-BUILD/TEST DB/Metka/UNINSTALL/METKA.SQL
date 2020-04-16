PROMPT ============================================================
PROMPT DELETE METKA &PATH_VERSION
PROMPT ============================================================

DELETE FROM T_ABOUT T WHERE T.VERSION='&PATH_VERSION';

COMMIT;