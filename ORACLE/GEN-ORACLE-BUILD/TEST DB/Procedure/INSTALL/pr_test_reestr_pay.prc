create or replace procedure PR_TEST_REESTR_PAY
(
  IN_CONTRACT_CODE              IN T_TRANSACTION.CONTRACT_CODE%TYPE,
  IN_START_DATE                 IN T_TRANSACTION.PAY_DATE%TYPE,
  IN_END_DATE                   IN T_TRANSACTION.PAY_DATE%TYPE,
  IN_NUM_EXT_REESTR             IN NUMBER DEFAULT NULL,
  OUT_CLOB_REESTR               OUT CLOB,
  OUT_CLOB_BASE                 OUT CLOB,
  OUT_NUM_EXT_REESTR            OUT NUMBER
)
IS
  valAMOUNT_SUM_TRANSACTION     NUMBER:=0;
  valCOUNT_TRANSACTION          NUMBER:=0;
  valSUM_DEBT                   NUMBER:=0;
  valCURRENCY                   NUMBER:=810;
BEGIN
--Инициализация
  OUT_CLOB_REESTR:=NULL;
  OUT_CLOB_BASE:=NULL;
  OUT_NUM_EXT_REESTR:=IN_NUM_EXT_REESTR;
--Номер реестра, если не указан, тогда генерим
  IF OUT_NUM_EXT_REESTR IS NULL THEN
    BEGIN
      OUT_NUM_EXT_REESTR:=ROUND(DBMS_RANDOM.VALUE(1000000, 9999999), 0);
    END;
  END IF;
--Подсчитываем количество и сумму
  BEGIN


    SELECT
      COUNT(T_RES.PAY_ID) AS COUNT_TRANSACTION,
      SUM(T_RES.AMOUNT) AS AMOUNT_SUM_TRANSACTION,
      SUM(T_RES.DEBT) AS SUM_DEBT
    INTO valCOUNT_TRANSACTION, valAMOUNT_SUM_TRANSACTION, valSUM_DEBT
    FROM
    (
    SELECT
      T.PAY_ID,
      T.AMOUNT,
       (T.AMOUNT-ROUND(((T.AMOUNT*PCK_CONTRACT.GetRateContractTypeDateRate(
        T.CONTRACT_CODE,
        T.TYPE_PAY_TOOLS,
        T.PAY_DATE,
        'REESTR_SWERKA_TEST'                               --rec.amount-ROUND(  ((rec.amount*valRatePay)/100)   , 2);
      ))/100),2)) AS DEBT
    FROM
     T_TRANSACTION T
    WHERE
     T.STATUS_ID = 111
     AND T.CONTRACT_CODE = IN_CONTRACT_CODE
     AND T.PAY_DATE>=IN_START_DATE
     AND T.PAY_DATE<=IN_END_DATE
    ) T_RES;

    EXCEPTION WHEN OTHERS THEN
      BEGIN
        valAMOUNT_SUM_TRANSACTION:=0;
        valCOUNT_TRANSACTION:=0;
        valSUM_DEBT:=0;
      END;
   END;
--Выбираем данные для реестра
  BEGIN
    WITH T_REESTR AS
      (SELECT
         XMLELEMENT("p", XMLATTRIBUTES(T.ID_RECORD AS "id"),               T.PAY) AS XML_PAY
       FROM
       (  SELECT
            ROWNUM AS ID_RECORD,
            TEMP.PAY
          FROM
          (
          SELECT
            T.PARTNER_AC_CODE||';'||T.PAY_ID||';'||TO_CHAR(T.PAY_DATE, 'YYYYMMDDHH24MISS')||'000'||';'||T.PAY_ID_EXT||';'||T.NUMBER_TPP||';'||T.MSISDN||';'||T.OPERATOR_CODE||';'||T.ACCOUNT||';'||TO_CHAR(T.AMOUNT, 'FM999999990.009999')||';'||T.CURRENCY||';'||T.TYPE_PAY_TOOLS||';'||TO_CHAR(T.AMOUNT-ROUND(((T.AMOUNT*PCK_CONTRACT.GetRateContractTypeDateRate(
                                                                                                                                                                                                                                                                                                                                              T.CONTRACT_CODE,
                                                                                                                                                                                                                                                                                                                                              T.TYPE_PAY_TOOLS,
                                                                                                                                                                                                                                                                                                                                              T.PAY_DATE,
                                                                                                                                                                                                                                                                                                                                              'REESTR_SWERKA_TEST'
                                                                                                                                                                                                                                                                                                                                            ))/100),2), 'FM999999990.009999') AS PAY
          FROM
            T_TRANSACTION T
          WHERE
            T.STATUS_ID = 111
            AND T.CONTRACT_CODE = IN_CONTRACT_CODE
            AND T.PAY_DATE>=IN_START_DATE
            AND T.PAY_DATE<=IN_END_DATE
          ORDER BY T.PAY_DATE
          ) TEMP
       ) T
      )
    SELECT
      XMLROOT
      (
        XMLELEMENT("comparePacket",
                        XMLATTRIBUTES('http://www.w3.org/2001/XMLSchema-instance' AS "xmlns:xsi",
                                      'http://schema.mts.ru/ESPP/AgentPayments/Registries/Reconciliation/v5_02' AS "xmlns",
                                      'http://schema.mts.ru/ESPP/Core/Constraints/v5_02' AS "xmlns:ESPP-constraints",
                                      'http://schema.mts.ru/ESPP/AgentPayments/Registries/Reconciliation/v5_02 ESPP_AgentPayments_Registries_Reconciliation_v5_02.xsd
                                       http://schema.mts.ru/ESPP/Core/Constraints/v5_02 ESPP_Core_Constraints_v5_02.xsd' AS "xsi:schemaLocation",
                                       OUT_NUM_EXT_REESTR AS "id"
                                     ),
                        XMLELEMENT("summary",
                                      XMLELEMENT("contract",  IN_CONTRACT_CODE),
                                      XMLELEMENT("comparePeriod",
                                                   XMLELEMENT("from", TO_CHAR(IN_START_DATE, 'YYYY-MM-DD"T"HH24:MI:SS')),
                                                   XMLELEMENT("to", TO_CHAR(IN_END_DATE, 'YYYY-MM-DD"T"HH24:MI:SS'))
                                                ),
                                      XMLELEMENT("totalAmountOfPayments", valCOUNT_TRANSACTION),
                                      XMLELEMENT("currency", XMLATTRIBUTES('ESPP-constraints:CUR_fmt_01' AS "xsi:type"), valCURRENCY),
                                      XMLELEMENT("totalSum", TO_CHAR(valAMOUNT_SUM_TRANSACTION, 'FM999999990.009999')),
                                      XMLELEMENT("totalDebt", TO_CHAR(valSUM_DEBT, 'FM999999990.009999'))
                                  ),
                        XMLELEMENT("payments",
                                     XMLAGG(TR.XML_PAY)
                                   )
                   ),
        VERSION '1.0" encoding="UTF-8'
      ).GetClobVal()           AS RES
    INTO OUT_CLOB_REESTR
    FROM
      T_REESTR TR;
  END;
--Делаем BASE64
  BEGIN
    OUT_CLOB_BASE:=PCK_UTILS.encode_base64_clob(OUT_CLOB_REESTR);
  END;

END PR_TEST_REESTR_PAY2;
/