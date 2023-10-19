----------------------------------------------------------------
--- create date range column: with var declaration

DECLARE @StartDate datetime = '2016-01-01'
       ,@EndDate   datetime = GETDATE()
;

WITH theDates AS
     (SELECT @StartDate as theDate
      UNION ALL
      SELECT DATEADD(day, 1, theDate)
        FROM theDates
       WHERE DATEADD(day, 1, theDate) <= @EndDate
     )
SELECT CONVERT(DATE, theDate) AS [date]
  FROM theDates
OPTION (MAXRECURSION 0)
;

----------------------------------------------------------------
--- create date range column: without var declaration

WITH theDates AS
     (SELECT CONVERT(DATE, '2016-01-01') as theDate
      UNION ALL
      SELECT DATEADD(day, 1, theDate)
        FROM theDates
       WHERE DATEADD(day, 1, theDate) <= GETDATE()
     )
SELECT CONVERT(DATE, theDate) AS [date]
  FROM theDates
OPTION (MAXRECURSION 0)
;
