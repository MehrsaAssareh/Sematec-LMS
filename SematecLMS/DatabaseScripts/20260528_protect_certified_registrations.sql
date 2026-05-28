USE [SematecLearningManagementSystem];
GO

IF OBJECT_ID(N'dbo.FK_StudentCourseCertificate_Registration', N'F') IS NOT NULL
BEGIN
    ALTER TABLE dbo.StudentCourseCertificate
        DROP CONSTRAINT FK_StudentCourseCertificate_Registration;
END;
GO

ALTER TABLE dbo.StudentCourseCertificate WITH CHECK
    ADD CONSTRAINT FK_StudentCourseCertificate_Registration
    FOREIGN KEY (RegistrationID)
    REFERENCES dbo.Student_Course_Teacher (ID);
GO

ALTER TABLE dbo.StudentCourseCertificate
    CHECK CONSTRAINT FK_StudentCourseCertificate_Registration;
GO

IF OBJECT_ID(N'dbo.TR_Student_Course_Teacher_ProtectCertifiedRows', N'TR') IS NOT NULL
    DROP TRIGGER dbo.TR_Student_Course_Teacher_ProtectCertifiedRows;
GO

CREATE TRIGGER dbo.TR_Student_Course_Teacher_ProtectCertifiedRows
ON dbo.Student_Course_Teacher
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1
        FROM inserted AS i
        INNER JOIN deleted AS d
            ON d.ID = i.ID
        INNER JOIN dbo.StudentCourseCertificate AS certificate
            ON certificate.RegistrationID = i.ID
        WHERE i.StudentID <> d.StudentID
           OR i.CourseID <> d.CourseID
           OR i.TeacherID <> d.TeacherID
           OR i.TermNumber <> d.TermNumber
           OR ISNULL(CONVERT(int, i.Score), -1) <> ISNULL(CONVERT(int, d.Score), -1)
    )
    BEGIN
        THROW 51510, 'Certified course registrations cannot be changed.', 1;
    END;
END;
GO

IF OBJECT_ID(N'dbo.TR_Users_RequireActiveAdmin', N'TR') IS NOT NULL
    DROP TRIGGER dbo.TR_Users_RequireActiveAdmin;
GO

CREATE TRIGGER dbo.TR_Users_RequireActiveAdmin
ON dbo.Users
AFTER UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (
        SELECT 1
        FROM dbo.Users
        WHERE isAdmin = 1
          AND isActive = 1
    )
    BEGIN
        THROW 51511, 'At least one active admin account is required.', 1;
    END;
END;
GO
