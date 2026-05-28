USE [SematecLearningManagementSystem];
GO

SET XACT_ABORT ON;
GO

BEGIN TRANSACTION;

IF COL_LENGTH(N'dbo.Student', N'FirstName') IS NOT NULL
   AND COL_LENGTH(N'dbo.Student', N'LastName') IS NOT NULL
   AND EXISTS (
       SELECT 1
       FROM dbo.Student AS s
       INNER JOIN dbo.Person AS p ON p.ID = s.PersonID
       WHERE ISNULL(s.FirstName, N'') <> ISNULL(p.FirstName, N'')
          OR ISNULL(s.LastName, N'') <> ISNULL(p.LastName, N'')
   )
BEGIN
    THROW 51400, 'Cannot drop Student.FirstName/Student.LastName because some rows do not match Person names.', 1;
END;

IF COL_LENGTH(N'dbo.Student', N'FirstName') IS NOT NULL
BEGIN
    ALTER TABLE dbo.Student DROP COLUMN FirstName;
END;

IF COL_LENGTH(N'dbo.Student', N'LastName') IS NOT NULL
BEGIN
    ALTER TABLE dbo.Student DROP COLUMN LastName;
END;

COMMIT TRANSACTION;
GO
