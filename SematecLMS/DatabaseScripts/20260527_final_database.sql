-- Sematec LMS final database script
-- Generated from the live SematecLearningManagementSystem database on 2026-05-27.
-- This is the clean baseline script; use it instead of old historical migration scripts.
-- Warning: when run against an existing database, it drops and recreates the app objects below.

IF DB_ID(N'SematecLearningManagementSystem') IS NULL
BEGIN
    EXEC(N'CREATE DATABASE [SematecLearningManagementSystem]');
END
GO

USE [SematecLearningManagementSystem];
GO

SET NOCOUNT ON;
GO

-- Drop existing app objects
IF OBJECT_ID(N'dbo.TR_Certification_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Certification_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Course_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Course_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_CourseCategory_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_CourseCategory_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_CourseSchedule_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_CourseSchedule_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Department_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Department_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Education_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Education_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Employee_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Employee_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Job_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Job_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Person_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Person_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_PersonPhoto_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_PersonPhoto_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Student_Course_Teacher_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Student_Course_Teacher_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Student_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Student_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_StudentCourseCertificate_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_StudentCourseCertificate_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Teacher_Certification_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Teacher_Certification_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Teacher_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Teacher_SetUpdatedAt];
IF OBJECT_ID(N'dbo.TR_Users_SetUpdatedAt', N'TR') IS NOT NULL DROP TRIGGER [dbo].[TR_Users_SetUpdatedAt];
IF OBJECT_ID(N'dbo.Course', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Course_Course', N'F') IS NOT NULL ALTER TABLE [dbo].[Course] DROP CONSTRAINT [FK_Course_Course];
IF OBJECT_ID(N'dbo.Course', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Course_CourseCategory', N'F') IS NOT NULL ALTER TABLE [dbo].[Course] DROP CONSTRAINT [FK_Course_CourseCategory];
IF OBJECT_ID(N'dbo.CourseSchedule', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_CourseSchedule_Course', N'F') IS NOT NULL ALTER TABLE [dbo].[CourseSchedule] DROP CONSTRAINT [FK_CourseSchedule_Course];
IF OBJECT_ID(N'dbo.CourseSchedule', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_CourseSchedule_Teacher', N'F') IS NOT NULL ALTER TABLE [dbo].[CourseSchedule] DROP CONSTRAINT [FK_CourseSchedule_Teacher];
IF OBJECT_ID(N'dbo.Employee', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Employee_Department', N'F') IS NOT NULL ALTER TABLE [dbo].[Employee] DROP CONSTRAINT [FK_Employee_Department];
IF OBJECT_ID(N'dbo.Employee', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Employee_Job', N'F') IS NOT NULL ALTER TABLE [dbo].[Employee] DROP CONSTRAINT [FK_Employee_Job];
IF OBJECT_ID(N'dbo.Employee', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Employee_Person', N'F') IS NOT NULL ALTER TABLE [dbo].[Employee] DROP CONSTRAINT [FK_Employee_Person];
IF OBJECT_ID(N'dbo.Person', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Person_Education', N'F') IS NOT NULL ALTER TABLE [dbo].[Person] DROP CONSTRAINT [FK_Person_Education];
IF OBJECT_ID(N'dbo.PersonPhoto', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_PersonPhoto_Person', N'F') IS NOT NULL ALTER TABLE [dbo].[PersonPhoto] DROP CONSTRAINT [FK_PersonPhoto_Person];
IF OBJECT_ID(N'dbo.Student', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Student_Person', N'F') IS NOT NULL ALTER TABLE [dbo].[Student] DROP CONSTRAINT [FK_Student_Person];
IF OBJECT_ID(N'dbo.Student_Course_Teacher', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Student_Course_Teacher_Course', N'F') IS NOT NULL ALTER TABLE [dbo].[Student_Course_Teacher] DROP CONSTRAINT [FK_Student_Course_Teacher_Course];
IF OBJECT_ID(N'dbo.Student_Course_Teacher', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Student_Course_Teacher_Student', N'F') IS NOT NULL ALTER TABLE [dbo].[Student_Course_Teacher] DROP CONSTRAINT [FK_Student_Course_Teacher_Student];
IF OBJECT_ID(N'dbo.Student_Course_Teacher', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Student_Course_Teacher_Teacher', N'F') IS NOT NULL ALTER TABLE [dbo].[Student_Course_Teacher] DROP CONSTRAINT [FK_Student_Course_Teacher_Teacher];
IF OBJECT_ID(N'dbo.StudentCourseCertificate', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_StudentCourseCertificate_Registration', N'F') IS NOT NULL ALTER TABLE [dbo].[StudentCourseCertificate] DROP CONSTRAINT [FK_StudentCourseCertificate_Registration];
IF OBJECT_ID(N'dbo.Teacher', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Teacher_Person', N'F') IS NOT NULL ALTER TABLE [dbo].[Teacher] DROP CONSTRAINT [FK_Teacher_Person];
IF OBJECT_ID(N'dbo.Teacher_Certification', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Teacher_Certification_Certification', N'F') IS NOT NULL ALTER TABLE [dbo].[Teacher_Certification] DROP CONSTRAINT [FK_Teacher_Certification_Certification];
IF OBJECT_ID(N'dbo.Teacher_Certification', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Teacher_Certification_Teacher', N'F') IS NOT NULL ALTER TABLE [dbo].[Teacher_Certification] DROP CONSTRAINT [FK_Teacher_Certification_Teacher];
IF OBJECT_ID(N'dbo.Users', N'U') IS NOT NULL AND OBJECT_ID(N'dbo.FK_Users_Person_PersonID', N'F') IS NOT NULL ALTER TABLE [dbo].[Users] DROP CONSTRAINT [FK_Users_Person_PersonID];
IF OBJECT_ID(N'dbo.Users', N'U') IS NOT NULL DROP TABLE [dbo].[Users];
IF OBJECT_ID(N'dbo.Teacher_Certification', N'U') IS NOT NULL DROP TABLE [dbo].[Teacher_Certification];
IF OBJECT_ID(N'dbo.Teacher', N'U') IS NOT NULL DROP TABLE [dbo].[Teacher];
IF OBJECT_ID(N'dbo.StudentCourseCertificate', N'U') IS NOT NULL DROP TABLE [dbo].[StudentCourseCertificate];
IF OBJECT_ID(N'dbo.Student_Course_Teacher', N'U') IS NOT NULL DROP TABLE [dbo].[Student_Course_Teacher];
IF OBJECT_ID(N'dbo.Student', N'U') IS NOT NULL DROP TABLE [dbo].[Student];
IF OBJECT_ID(N'dbo.PersonPhoto', N'U') IS NOT NULL DROP TABLE [dbo].[PersonPhoto];
IF OBJECT_ID(N'dbo.Person', N'U') IS NOT NULL DROP TABLE [dbo].[Person];
IF OBJECT_ID(N'dbo.Job', N'U') IS NOT NULL DROP TABLE [dbo].[Job];
IF OBJECT_ID(N'dbo.Employee', N'U') IS NOT NULL DROP TABLE [dbo].[Employee];
IF OBJECT_ID(N'dbo.Education', N'U') IS NOT NULL DROP TABLE [dbo].[Education];
IF OBJECT_ID(N'dbo.Department', N'U') IS NOT NULL DROP TABLE [dbo].[Department];
IF OBJECT_ID(N'dbo.CourseSchedule', N'U') IS NOT NULL DROP TABLE [dbo].[CourseSchedule];
IF OBJECT_ID(N'dbo.CourseCategory', N'U') IS NOT NULL DROP TABLE [dbo].[CourseCategory];
IF OBJECT_ID(N'dbo.Course', N'U') IS NOT NULL DROP TABLE [dbo].[Course];
IF OBJECT_ID(N'dbo.Certification', N'U') IS NOT NULL DROP TABLE [dbo].[Certification];
GO

-- Create tables
CREATE TABLE [dbo].[Certification] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [CertificationTitle] nvarchar(50) NOT NULL,
    [Vendor] nvarchar(50) NOT NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Certification_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Certification_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Course] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [CourseCode] int NOT NULL,
    [CourseName] nvarchar(50) NOT NULL,
    [Duration] int NOT NULL,
    [Syllabus] nvarchar(MAX) NOT NULL,
    [Cost] int NOT NULL,
    [Status] nvarchar(20) NOT NULL CONSTRAINT [DF_Course_Status] DEFAULT (N'Active'),
    [CourseCategoryID] int NOT NULL,
    [PrerequisiteCourseID] int NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Course_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Course_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[CourseCategory] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [CourseCategoryName] nvarchar(50) NOT NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_CourseCategory_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_CourseCategory_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[CourseSchedule] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [CourseID] int NOT NULL,
    [PlannedBeginningDate] date NOT NULL,
    [DurationWeek] smallint NOT NULL,
    [DurationSessionHour] tinyint NOT NULL,
    [PlannedFinishingDate] date NOT NULL,
    [ActualBeginningDate] date NULL,
    [ActualDurationWeek] smallint NULL,
    [ActualFinishingDate] date NULL,
    [Comments] nvarchar(500) NULL,
    [TeacherID] int NOT NULL,
    [TermNumber] int NOT NULL,
    [Capacity] smallint NULL,
    [RoomName] nvarchar(50) NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_CourseSchedule_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_CourseSchedule_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Department] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [DepartmentName] nvarchar(50) NOT NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Department_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Department_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Education] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [EducationTitle] nvarchar(50) NOT NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Education_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Education_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Employee] (
    [PersonID] int NOT NULL,
    [TotalChildren] tinyint NOT NULL,
    [StartDate] date NOT NULL,
    [InsuranceNumber] varchar(7) NOT NULL,
    [AccountNumber] varchar(16) NOT NULL,
    [HireDate] date NOT NULL,
    [DepartmentID] int NOT NULL,
    [JobID] int NOT NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Employee_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Employee_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Job] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [JobTitle] nvarchar(50) NOT NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Job_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Job_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Person] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [FirstName] nvarchar(20) NOT NULL,
    [LastName] nvarchar(50) NOT NULL,
    [Birthdate] date NOT NULL,
    [MaritalStatus] nvarchar(20) NOT NULL,
    [NationalCode] varchar(10) NOT NULL,
    [Mobile] varchar(11) NOT NULL,
    [Address] nvarchar(500) NULL,
    [Gender] nvarchar(20) NOT NULL,
    [EmailAddress] varchar(100) NULL,
    [EducationID] int NOT NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Person_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Person_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[PersonPhoto] (
    [PersonID] int NOT NULL,
    [PhotoContent] varbinary(MAX) NOT NULL,
    [FileName] nvarchar(260) NULL,
    [ContentType] nvarchar(100) NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_PersonPhoto_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_PersonPhoto_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Student] (
    [PersonID] int NOT NULL,
    [FirstRegisterDate] date NOT NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Student_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Student_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Student_Course_Teacher] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [StudentID] int NOT NULL,
    [CourseID] int NOT NULL,
    [TeacherID] int NOT NULL,
    [TermNumber] int NOT NULL,
    [Score] tinyint NULL,
    [CreatedAt] datetime2(7) NOT NULL CONSTRAINT [DF_Student_Course_Teacher_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(7) NOT NULL CONSTRAINT [DF_Student_Course_Teacher_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[StudentCourseCertificate] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [RegistrationID] int NOT NULL,
    [CertificateNumber] nvarchar(30) NOT NULL,
    [IssueDate] date NOT NULL CONSTRAINT [DF_StudentCourseCertificate_IssueDate] DEFAULT (CONVERT([date],getdate())),
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_StudentCourseCertificate_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_StudentCourseCertificate_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Teacher] (
    [PersonID] int NOT NULL,
    [InsuranceNumber] varchar(7) NOT NULL,
    [AccountNumber] varchar(16) NOT NULL,
    [StartDate] date NOT NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Teacher_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Teacher_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Teacher_Certification] (
    [TeacherID] int NOT NULL,
    [CertificationID] int NOT NULL,
    [ReceiptID] nvarchar(50) NOT NULL,
    [CreatedAt] datetime2(7) NOT NULL CONSTRAINT [DF_Teacher_Certification_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(7) NOT NULL CONSTRAINT [DF_Teacher_Certification_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

CREATE TABLE [dbo].[Users] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [UserName] varchar(50) NOT NULL,
    [FirstName] nvarchar(50) NOT NULL,
    [LastName] nvarchar(50) NOT NULL,
    [isAdmin] bit NOT NULL,
    [isActive] bit NOT NULL CONSTRAINT [DF_Users_isActive] DEFAULT ((1)),
    [PersonID] int NOT NULL,
    [PasswordHash] varbinary(32) NOT NULL,
    [PasswordSalt] varbinary(16) NOT NULL,
    [PasswordIterations] int NOT NULL,
    [CreatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Users_CreatedAt] DEFAULT (sysutcdatetime()),
    [UpdatedAt] datetime2(0) NOT NULL CONSTRAINT [DF_Users_UpdatedAt] DEFAULT (sysutcdatetime())
);
GO

-- Primary keys and unique indexes
ALTER TABLE [dbo].[Certification] ADD CONSTRAINT [PK_Certification] PRIMARY KEY CLUSTERED ([ID] ASC);
ALTER TABLE [dbo].[Course] ADD CONSTRAINT [PK_Course] PRIMARY KEY CLUSTERED ([ID] ASC);
ALTER TABLE [dbo].[CourseCategory] ADD CONSTRAINT [PK_CourseCategory] PRIMARY KEY CLUSTERED ([ID] ASC);
ALTER TABLE [dbo].[CourseSchedule] ADD CONSTRAINT [PK_CourseSchedule] PRIMARY KEY CLUSTERED ([ID] ASC);
ALTER TABLE [dbo].[Department] ADD CONSTRAINT [PK_Department] PRIMARY KEY CLUSTERED ([ID] ASC);
ALTER TABLE [dbo].[Education] ADD CONSTRAINT [PK_Education] PRIMARY KEY CLUSTERED ([ID] ASC);
ALTER TABLE [dbo].[Employee] ADD CONSTRAINT [PK_Employee] PRIMARY KEY CLUSTERED ([PersonID] ASC);
ALTER TABLE [dbo].[Job] ADD CONSTRAINT [PK_Job] PRIMARY KEY CLUSTERED ([ID] ASC);
ALTER TABLE [dbo].[Person] ADD CONSTRAINT [PK_Person] PRIMARY KEY CLUSTERED ([ID] ASC);
ALTER TABLE [dbo].[PersonPhoto] ADD CONSTRAINT [PK_PersonPhoto] PRIMARY KEY CLUSTERED ([PersonID] ASC);
ALTER TABLE [dbo].[Student] ADD CONSTRAINT [PK_Student] PRIMARY KEY CLUSTERED ([PersonID] ASC);
ALTER TABLE [dbo].[Student_Course_Teacher] ADD CONSTRAINT [PK_Student_Course_Teacher] PRIMARY KEY CLUSTERED ([ID] ASC);
ALTER TABLE [dbo].[StudentCourseCertificate] ADD CONSTRAINT [PK_StudentCourseCertificate] PRIMARY KEY CLUSTERED ([ID] ASC);
ALTER TABLE [dbo].[Teacher] ADD CONSTRAINT [PK_Teacher] PRIMARY KEY CLUSTERED ([PersonID] ASC);
ALTER TABLE [dbo].[Teacher_Certification] ADD CONSTRAINT [PK_Teacher_Certification] PRIMARY KEY CLUSTERED ([TeacherID] ASC, [CertificationID] ASC);
ALTER TABLE [dbo].[Users] ADD CONSTRAINT [PK_Users] PRIMARY KEY CLUSTERED ([ID] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Certification_TitleVendor] ON [dbo].[Certification] ([CertificationTitle] ASC, [Vendor] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Course_CourseCode] ON [dbo].[Course] ([CourseCode] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_CourseCategory_CourseCategoryName] ON [dbo].[CourseCategory] ([CourseCategoryName] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_CourseSchedule_Offering] ON [dbo].[CourseSchedule] ([CourseID] ASC, [TeacherID] ASC, [TermNumber] ASC, [PlannedBeginningDate] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Department_DepartmentName] ON [dbo].[Department] ([DepartmentName] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Education_EducationTitle] ON [dbo].[Education] ([EducationTitle] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Employee_AccountNumber] ON [dbo].[Employee] ([AccountNumber] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Employee_InsuranceNumber] ON [dbo].[Employee] ([InsuranceNumber] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Job_JobTitle] ON [dbo].[Job] ([JobTitle] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [NCI_U_NationalCode] ON [dbo].[Person] ([NationalCode] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_StudentCourseTerm] ON [dbo].[Student_Course_Teacher] ([StudentID] ASC, [CourseID] ASC, [TermNumber] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_StudentCourseCertificate_Number] ON [dbo].[StudentCourseCertificate] ([CertificateNumber] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_StudentCourseCertificate_RegistrationID] ON [dbo].[StudentCourseCertificate] ([RegistrationID] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Teacher_AccountNumber] ON [dbo].[Teacher] ([AccountNumber] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Teacher_InsuranceNumber] ON [dbo].[Teacher] ([InsuranceNumber] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Users_PersonID] ON [dbo].[Users] ([PersonID] ASC);
CREATE UNIQUE NONCLUSTERED INDEX [UX_Users_UserName] ON [dbo].[Users] ([UserName] ASC);
GO

-- Check constraints
ALTER TABLE [dbo].[Course] WITH CHECK ADD CONSTRAINT [CK_Course_Cost] CHECK ([Cost]>=(0));
ALTER TABLE [dbo].[Course] CHECK CONSTRAINT [CK_Course_Cost];
ALTER TABLE [dbo].[Course] WITH CHECK ADD CONSTRAINT [CK_Course_Duration] CHECK ([Duration]>(0));
ALTER TABLE [dbo].[Course] CHECK CONSTRAINT [CK_Course_Duration];
ALTER TABLE [dbo].[Course] WITH CHECK ADD CONSTRAINT [CK_Course_Prerequisite_NotSelf] CHECK ([PrerequisiteCourseID] IS NULL OR [PrerequisiteCourseID]<>[ID]);
ALTER TABLE [dbo].[Course] CHECK CONSTRAINT [CK_Course_Prerequisite_NotSelf];
ALTER TABLE [dbo].[Course] WITH CHECK ADD CONSTRAINT [CK_Course_Status] CHECK ([Status]=N'Inactive' OR [Status]=N'Active');
ALTER TABLE [dbo].[Course] CHECK CONSTRAINT [CK_Course_Status];
ALTER TABLE [dbo].[CourseSchedule] WITH CHECK ADD CONSTRAINT [CK_CourseSchedule_ActualDates] CHECK ([ActualBeginningDate] IS NULL OR [ActualFinishingDate] IS NULL OR [ActualFinishingDate]>=[ActualBeginningDate]);
ALTER TABLE [dbo].[CourseSchedule] CHECK CONSTRAINT [CK_CourseSchedule_ActualDates];
ALTER TABLE [dbo].[CourseSchedule] WITH CHECK ADD CONSTRAINT [CK_CourseSchedule_ActualDurationWeek] CHECK ([ActualDurationWeek] IS NULL OR [ActualDurationWeek]>=(0));
ALTER TABLE [dbo].[CourseSchedule] CHECK CONSTRAINT [CK_CourseSchedule_ActualDurationWeek];
ALTER TABLE [dbo].[CourseSchedule] WITH CHECK ADD CONSTRAINT [CK_CourseSchedule_Capacity] CHECK ([Capacity] IS NULL OR [Capacity]>(0));
ALTER TABLE [dbo].[CourseSchedule] CHECK CONSTRAINT [CK_CourseSchedule_Capacity];
ALTER TABLE [dbo].[CourseSchedule] WITH CHECK ADD CONSTRAINT [CK_CourseSchedule_DurationSessionHour] CHECK ([DurationSessionHour]>(0));
ALTER TABLE [dbo].[CourseSchedule] CHECK CONSTRAINT [CK_CourseSchedule_DurationSessionHour];
ALTER TABLE [dbo].[CourseSchedule] WITH CHECK ADD CONSTRAINT [CK_CourseSchedule_DurationWeek] CHECK ([DurationWeek]>(0));
ALTER TABLE [dbo].[CourseSchedule] CHECK CONSTRAINT [CK_CourseSchedule_DurationWeek];
ALTER TABLE [dbo].[CourseSchedule] WITH CHECK ADD CONSTRAINT [CK_CourseSchedule_PlannedDates] CHECK ([PlannedFinishingDate]>=[PlannedBeginningDate]);
ALTER TABLE [dbo].[CourseSchedule] CHECK CONSTRAINT [CK_CourseSchedule_PlannedDates];
ALTER TABLE [dbo].[CourseSchedule] WITH CHECK ADD CONSTRAINT [CK_CourseSchedule_TermNumber] CHECK ([TermNumber] IS NULL OR [TermNumber]>(0));
ALTER TABLE [dbo].[CourseSchedule] CHECK CONSTRAINT [CK_CourseSchedule_TermNumber];
ALTER TABLE [dbo].[Employee] WITH CHECK ADD CONSTRAINT [CK_Employee_AccountNumber] CHECK (len([AccountNumber])=(16) AND NOT [AccountNumber] like '%[^0-9]%');
ALTER TABLE [dbo].[Employee] CHECK CONSTRAINT [CK_Employee_AccountNumber];
ALTER TABLE [dbo].[Employee] WITH CHECK ADD CONSTRAINT [CK_Employee_InsuranceNumber] CHECK (len([InsuranceNumber])=(7) AND NOT [InsuranceNumber] like '%[^0-9]%');
ALTER TABLE [dbo].[Employee] CHECK CONSTRAINT [CK_Employee_InsuranceNumber];
ALTER TABLE [dbo].[Employee] WITH CHECK ADD CONSTRAINT [CK_Employee_TotalChildren] CHECK ([TotalChildren]>=(0) AND [TotalChildren]<=(30));
ALTER TABLE [dbo].[Employee] CHECK CONSTRAINT [CK_Employee_TotalChildren];
ALTER TABLE [dbo].[Person] WITH CHECK ADD CONSTRAINT [CK_Person_Birthdate] CHECK ([Birthdate]<=CONVERT([date],getdate()));
ALTER TABLE [dbo].[Person] CHECK CONSTRAINT [CK_Person_Birthdate];
ALTER TABLE [dbo].[Person] WITH CHECK ADD CONSTRAINT [CK_Person_EmailAddress] CHECK ([EmailAddress] IS NULL OR [EmailAddress] like '%_@_%._%');
ALTER TABLE [dbo].[Person] CHECK CONSTRAINT [CK_Person_EmailAddress];
ALTER TABLE [dbo].[Person] WITH CHECK ADD CONSTRAINT [CK_Person_Gender] CHECK ([Gender]=N'Female' OR [Gender]=N'Male');
ALTER TABLE [dbo].[Person] CHECK CONSTRAINT [CK_Person_Gender];
ALTER TABLE [dbo].[Person] WITH CHECK ADD CONSTRAINT [CK_Person_MaritalStatus] CHECK ([MaritalStatus]=N'Married' OR [MaritalStatus]=N'Single');
ALTER TABLE [dbo].[Person] CHECK CONSTRAINT [CK_Person_MaritalStatus];
ALTER TABLE [dbo].[Person] WITH CHECK ADD CONSTRAINT [CK_Person_Mobile] CHECK (len([Mobile])=(11) AND NOT [Mobile] like '%[^0-9]%');
ALTER TABLE [dbo].[Person] CHECK CONSTRAINT [CK_Person_Mobile];
ALTER TABLE [dbo].[Person] WITH CHECK ADD CONSTRAINT [CK_Person_NationalCode] CHECK (len([NationalCode])=(10) AND NOT [NationalCode] like '%[^0-9]%');
ALTER TABLE [dbo].[Person] CHECK CONSTRAINT [CK_Person_NationalCode];
ALTER TABLE [dbo].[Student_Course_Teacher] WITH CHECK ADD CONSTRAINT [CK_Student_Course_Teacher_Score] CHECK ([Score] IS NULL OR [Score]>=(0) AND [Score]<=(100));
ALTER TABLE [dbo].[Student_Course_Teacher] CHECK CONSTRAINT [CK_Student_Course_Teacher_Score];
ALTER TABLE [dbo].[Student_Course_Teacher] WITH CHECK ADD CONSTRAINT [CK_Student_Course_Teacher_TermNumber] CHECK ([TermNumber]>(0));
ALTER TABLE [dbo].[Student_Course_Teacher] CHECK CONSTRAINT [CK_Student_Course_Teacher_TermNumber];
ALTER TABLE [dbo].[Teacher] WITH CHECK ADD CONSTRAINT [CK_Teacher_AccountNumber] CHECK (len([AccountNumber])=(16) AND NOT [AccountNumber] like '%[^0-9]%');
ALTER TABLE [dbo].[Teacher] CHECK CONSTRAINT [CK_Teacher_AccountNumber];
ALTER TABLE [dbo].[Teacher] WITH CHECK ADD CONSTRAINT [CK_Teacher_InsuranceNumber] CHECK (len([InsuranceNumber])=(7) AND NOT [InsuranceNumber] like '%[^0-9]%');
ALTER TABLE [dbo].[Teacher] CHECK CONSTRAINT [CK_Teacher_InsuranceNumber];
ALTER TABLE [dbo].[Users] WITH CHECK ADD CONSTRAINT [CK_Users_PasswordHash] CHECK ([PasswordHash] IS NULL OR datalength([PasswordHash])=(32) AND datalength([PasswordSalt])=(16) AND [PasswordIterations]>=(100000));
ALTER TABLE [dbo].[Users] CHECK CONSTRAINT [CK_Users_PasswordHash];
GO

-- Data
-- [dbo].[Certification] (8 rows)
SET IDENTITY_INSERT [dbo].[Certification] ON;
INSERT INTO [dbo].[Certification] ([ID], [CertificationTitle], [Vendor], [CreatedAt], [UpdatedAt]) VALUES (1, N'Development Associate', N'SAP', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Certification] ([ID], [CertificationTitle], [Vendor], [CreatedAt], [UpdatedAt]) VALUES (2, N'Azure Developer Associate', N'Microsoft', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Certification] ([ID], [CertificationTitle], [Vendor], [CreatedAt], [UpdatedAt]) VALUES (3, N'Associate Cloud Engineer', N'Google', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Certification] ([ID], [CertificationTitle], [Vendor], [CreatedAt], [UpdatedAt]) VALUES (4, N'Developer Associate', N'SAP', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Certification] ([ID], [CertificationTitle], [Vendor], [CreatedAt], [UpdatedAt]) VALUES (5, N'Java SE 11 Developer', N'Oracle', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Certification] ([ID], [CertificationTitle], [Vendor], [CreatedAt], [UpdatedAt]) VALUES (7, N'PL_300', N'Microsoft', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Certification] ([ID], [CertificationTitle], [Vendor], [CreatedAt], [UpdatedAt]) VALUES (8, N'AWS Certified Developer', N'Amazon Web Services', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Certification] ([ID], [CertificationTitle], [Vendor], [CreatedAt], [UpdatedAt]) VALUES (9, N'Platform App Builder', N'Salesforce', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
SET IDENTITY_INSERT [dbo].[Certification] OFF;
GO

-- [dbo].[Course] (3 rows)
SET IDENTITY_INSERT [dbo].[Course] ON;
INSERT INTO [dbo].[Course] ([ID], [CourseCode], [CourseName], [Duration], [Syllabus], [Cost], [Status], [CourseCategoryID], [PrerequisiteCourseID], [CreatedAt], [UpdatedAt]) VALUES (3, 1, N'Data Science', 140, CAST(N'Introduction of Data Science =>
• SQL Server
• Introduction to Microsoft SQL Server 2019
• Install SQL Server 2019
• Relational Database Design Concepts
• Normalization Form
• Creating Tables and Declarative Constraints
• Working with SQL Server 2016 Data Types
• Constraints and Rules
• Introduction to T-SQL Querying
• Writing Basic SELECT Statements
• Using Built-In Functions
• Querying Multiple Tables
• Sorting and Filtering Data
• Grouping and Aggregating Data
• Correlated Query
• Using Subqueries
• Using Common Table Expressions
• Recursive CTE
• Using Set Operators
• Using Windows Ranking, Offset, and Aggregate Functions
• Pivoting and Grouping Sets
• Using DML to Modify Data
• Merge Statement
• Executing Stored Procedures
• Views
• Table-Value and Scalar Function
• Trigger
• Programming with T-SQL
• Implementing Error Handling
• Implementing Transaction
• Row Store and Column Store Index
• Final Project
Power BI =>
• Introduction Business Intelligence
• Microsoft BI Architecture
• Introduction Self-Service BI
• Install Power BI Desktop
• Data Extraction from CSV, Excel, SQL Server Database, Web Content
• Star and Snowflake Schema
• Import and Direct Query Modes
• Introduction Power Query Editor
• Data Types
• Append Queries and Merge Queries
• Hierarchy
• Introduction to Reports and Visualization Types
• Custom Visuals
• Filters in Power BI
• Slicers in Power BI
• Table and Matrix
• Column and Bar Chart
• Pie chart and Doughnut charts
• Conditional Formatting on Visuals
• Card and Multi-Row Card
• Phone layout
• Treemap
• Combo Chart
• Line chart, Area chart, and Stacked area chart
• Gauge chart
• KPI
• Drill through
• Map and Filled map
• Offline Map ( Synoptic Panel )
• Waterfall Chart
• Funnel chart
• Buttons and Bookmark
• Scatter Chart
• Introduction to Data Analysis Expression (DAX)
• Creating Calculated Columns, Creating Measures
• Introduction DAX Studio
• DAX Date and Time Functions
• DAX Text Functions
• DAX Logical Functions
• DAX Related Function
• DAX Implicit Versus Explicit Measures
• DAX Statistical Functions
• DAX Filter Functions
• DAX X-factor Functions
• DAX Time Intelligence Functions
• DAX Rank Functions
• Persian DimDate
• Tables and Parameters
• Install Power BI Report Server
• Publish Report
• Auto Refresh
• Authorization in Power BI Report Server
• Row-Level Security
• Branding
• Final Project 
Python =>
• Introducing Python
• Python’s applications
• Install and run Python
• Install IDE (PyCharm, Visual Studio Code )
• I/O
• Types
• Variables
• Operators
• Functions
• Conditional
• Loops
• Built-in Functions
• List, Tuple and Dictionary
• Define Function
• Object Oriented Concepts
• Classes
• Fields and methods
• Inheritance
• Override
• Design Patterns
• Using libraries
• Read and write text files
• CSV and Excel File Library (csv, openpyxl)
• Testing with unit test
• GUI with tkinter
• Database Programming with sqlite3 and pyodbc
• Recursive functions
• Exception
• Lambda expressions
• Reflection
• Closure
• Regular expression
• Generators
• Threading & Multiprocessing
• Queue, Stack, Linked list and Tree
• Final Project
Data Science with Python =>
• Install Anaconda
• Introduction of Python Data Science Libraries
• Data Mining Process
• CRISP
• Data Preparation
• Introduction Pandas
• DataFrames
• Data type conversions using pandas
• Working with String and Dates using pandas
• Dealing with missing data using pandas
• Groupby and aggregations
• Merging (Merge, Join) and concatenating (Concat) dataframes
• Mapping variables into groups
• Plotting with pandas
• Correlations and statistical functions
• Introduction Numpy
• Array and Features
• Array’s Operators
• Numpy Functions
• Indexing and Slicing
• Using Numpy in Linear Algebra
• Introduction to Matplolip
• Graphs
• Bar Graph
• Scatter Graph
• Using Text
• Annotation in Graph
• Scatter plot and Categorical plot
• Histograms
• Pyplot
• Pyplot Tex
• Barh and Fill
• Pcolormesh and Pathpatch
• Streamplot
• Pie Chart
• Table
• Log and Polar
• Customizing Plot
• Customizing Styles
• GridSpec
• 3D Line and Bar
• Transformation
• Introduction of Scikit-Learn
• KNN
• Linear Regression
• Logistic Regression
• Clustering
• Linear SVM
• Nave Bayes
• Decision Trees
• Neural Networks
• TensorFlow
• Final Project' AS nvarchar(MAX)), 14900000, N'Active', 1, NULL, N'2026-05-20 02:49:16', N'2026-05-28 06:46:45');
INSERT INTO [dbo].[Course] ([ID], [CourseCode], [CourseName], [Duration], [Syllabus], [Cost], [Status], [CourseCategoryID], [PrerequisiteCourseID], [CreatedAt], [UpdatedAt]) VALUES (10, 3, N'Programming with Python Language', 40, CAST(N'Principles of Programming in Python =>
• Variable definitions and data types (Mutable & Immutable)
• Operators and Input/Output (I/O)
• Conditional structures: if – elif – else
• while and for loops
• Function definitions and recursive functions
• How to install and use libraries
• Familiarity with commonly used libraries such as math and statistics
• Pack and Unpack concepts
Object-Oriented Programming (OOP) in Python =>
• Object-Oriented Programming (OOP) in Python
• Classes and the concept of Inheritance
• Exception and Error Handling
• Connecting to SQLite3 databases in Python
• Reading from and writing to CSV files' AS nvarchar(MAX)), 5000000, N'Active', 9, NULL, N'2026-05-26 08:12:40', N'2026-05-28 06:47:59');
INSERT INTO [dbo].[Course] ([ID], [CourseCode], [CourseName], [Duration], [Syllabus], [Cost], [Status], [CourseCategoryID], [PrerequisiteCourseID], [CreatedAt], [UpdatedAt]) VALUES (11, 4, N'Advanced Python', 40, CAST(N'Advanced Topics =>
• Iterators and Generators
• Package Management
• Working with JSON
• Advanced Object-Oriented Programming (OOP) concepts
• Design Patterns
• Regular Expressions
• Coding Standards and PEP-8
• Debugging and Profiling
Advanced Libraries =>
• functools and urllib
• itertools and combinatorics
• collections
• Multithreading and Multiprocessing
• Asynchronous Programming (asyncio)
• Virtual Environment Management (venv)
• Working with Scrapy for Web Scraping
• Operating System Management with os
• Working with data: array, decimal, fraction
• Testing: doctest and unittest' AS nvarchar(MAX)), 8000000, N'Active', 9, 10, N'2026-05-26 08:14:48', N'2026-05-28 06:49:01');
SET IDENTITY_INSERT [dbo].[Course] OFF;
GO

-- [dbo].[CourseCategory] (8 rows)
SET IDENTITY_INSERT [dbo].[CourseCategory] ON;
INSERT INTO [dbo].[CourseCategory] ([ID], [CourseCategoryName], [CreatedAt], [UpdatedAt]) VALUES (1, N'Data', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[CourseCategory] ([ID], [CourseCategoryName], [CreatedAt], [UpdatedAt]) VALUES (2, N'Network & Security', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[CourseCategory] ([ID], [CourseCategoryName], [CreatedAt], [UpdatedAt]) VALUES (3, N'Database', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[CourseCategory] ([ID], [CourseCategoryName], [CreatedAt], [UpdatedAt]) VALUES (4, N'Graphic Design', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[CourseCategory] ([ID], [CourseCategoryName], [CreatedAt], [UpdatedAt]) VALUES (5, N'Cloud & DevOps', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[CourseCategory] ([ID], [CourseCategoryName], [CreatedAt], [UpdatedAt]) VALUES (6, N'Cyber Security', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[CourseCategory] ([ID], [CourseCategoryName], [CreatedAt], [UpdatedAt]) VALUES (8, N'Business Intelligence', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[CourseCategory] ([ID], [CourseCategoryName], [CreatedAt], [UpdatedAt]) VALUES (9, N'Programming', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
SET IDENTITY_INSERT [dbo].[CourseCategory] OFF;
GO

-- [dbo].[CourseSchedule] (3 rows)
SET IDENTITY_INSERT [dbo].[CourseSchedule] ON;
INSERT INTO [dbo].[CourseSchedule] ([ID], [CourseID], [PlannedBeginningDate], [DurationWeek], [DurationSessionHour], [PlannedFinishingDate], [ActualBeginningDate], [ActualDurationWeek], [ActualFinishingDate], [Comments], [TeacherID], [TermNumber], [Capacity], [RoomName], [CreatedAt], [UpdatedAt]) VALUES (3, 3, N'2025-04-19', 40, 4, N'2026-01-17', N'2025-04-19', 35, N'2026-02-21', NULL, 33, 1, 50, N'2', N'2026-05-26 08:20:50', N'2026-05-26 08:21:26');
INSERT INTO [dbo].[CourseSchedule] ([ID], [CourseID], [PlannedBeginningDate], [DurationWeek], [DurationSessionHour], [PlannedFinishingDate], [ActualBeginningDate], [ActualDurationWeek], [ActualFinishingDate], [Comments], [TeacherID], [TermNumber], [Capacity], [RoomName], [CreatedAt], [UpdatedAt]) VALUES (4, 10, N'2023-11-12', 10, 4, N'2024-01-21', N'2023-11-12', 10, N'2024-01-21', NULL, 61, 3, 50, N'1', N'2026-05-26 08:32:20', N'2026-05-26 08:32:20');
INSERT INTO [dbo].[CourseSchedule] ([ID], [CourseID], [PlannedBeginningDate], [DurationWeek], [DurationSessionHour], [PlannedFinishingDate], [ActualBeginningDate], [ActualDurationWeek], [ActualFinishingDate], [Comments], [TeacherID], [TermNumber], [Capacity], [RoomName], [CreatedAt], [UpdatedAt]) VALUES (5, 11, N'2024-04-19', 10, 4, N'2024-06-21', N'2024-04-19', 10, N'2024-06-21', NULL, 61, 1, 50, N'1', N'2026-05-26 08:35:51', N'2026-05-26 08:35:51');
SET IDENTITY_INSERT [dbo].[CourseSchedule] OFF;
GO

-- [dbo].[Department] (4 rows)
SET IDENTITY_INSERT [dbo].[Department] ON;
INSERT INTO [dbo].[Department] ([ID], [DepartmentName], [CreatedAt], [UpdatedAt]) VALUES (1, N'Management', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Department] ([ID], [DepartmentName], [CreatedAt], [UpdatedAt]) VALUES (2, N'HR', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Department] ([ID], [DepartmentName], [CreatedAt], [UpdatedAt]) VALUES (3, N'IT', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Department] ([ID], [DepartmentName], [CreatedAt], [UpdatedAt]) VALUES (4, N'Production', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
SET IDENTITY_INSERT [dbo].[Department] OFF;
GO

-- [dbo].[Education] (5 rows)
SET IDENTITY_INSERT [dbo].[Education] ON;
INSERT INTO [dbo].[Education] ([ID], [EducationTitle], [CreatedAt], [UpdatedAt]) VALUES (1, N'phd', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Education] ([ID], [EducationTitle], [CreatedAt], [UpdatedAt]) VALUES (2, N'Master', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Education] ([ID], [EducationTitle], [CreatedAt], [UpdatedAt]) VALUES (3, N'Bachelors', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Education] ([ID], [EducationTitle], [CreatedAt], [UpdatedAt]) VALUES (5, N'Associate', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
INSERT INTO [dbo].[Education] ([ID], [EducationTitle], [CreatedAt], [UpdatedAt]) VALUES (6, N'Diploma', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
SET IDENTITY_INSERT [dbo].[Education] OFF;
GO

-- [dbo].[Employee] (2 rows)
GO

-- [dbo].[Job] (3 rows)
SET IDENTITY_INSERT [dbo].[Job] ON;
INSERT INTO [dbo].[Job] ([ID], [JobTitle], [CreatedAt], [UpdatedAt]) VALUES (1, N'Training Specialist', N'2026-05-20 02:49:16', N'2026-05-26 06:17:50');
INSERT INTO [dbo].[Job] ([ID], [JobTitle], [CreatedAt], [UpdatedAt]) VALUES (2, N'Training Manager', N'2026-05-20 02:49:16', N'2026-05-26 06:17:50');
INSERT INTO [dbo].[Job] ([ID], [JobTitle], [CreatedAt], [UpdatedAt]) VALUES (3, N'Training Staff', N'2026-05-20 02:49:16', N'2026-05-20 02:49:16');
SET IDENTITY_INSERT [dbo].[Job] OFF;
GO

-- [dbo].[Person] (9 rows)
INSERT INTO [dbo].[Employee] ([PersonID], [TotalChildren], [StartDate], [InsuranceNumber], [AccountNumber], [HireDate], [DepartmentID], [JobID], [CreatedAt], [UpdatedAt]) VALUES (35, 0, N'2018-01-05', '1000035', '1000000000000035', N'2018-01-05', 2, 2, N'2026-05-20 02:49:16', N'2026-05-26 08:41:00');
INSERT INTO [dbo].[Employee] ([PersonID], [TotalChildren], [StartDate], [InsuranceNumber], [AccountNumber], [HireDate], [DepartmentID], [JobID], [CreatedAt], [UpdatedAt]) VALUES (38, 0, N'2021-09-07', '1000038', '1000000000000038', N'2021-09-07', 3, 1, N'2026-05-20 02:49:16', N'2026-05-26 07:56:22');
SET IDENTITY_INSERT [dbo].[Person] ON;
INSERT INTO [dbo].[Person] ([ID], [FirstName], [LastName], [Birthdate], [MaritalStatus], [NationalCode], [Mobile], [Address], [Gender], [EmailAddress], [EducationID], [CreatedAt], [UpdatedAt]) VALUES (33, N'Alex', N'Morgan', N'1981-09-16', N'Single', N'0000000033', N'09120000033', N'Demo Address 33', N'Male', N'alex.morgan@example.com', 1, N'2026-05-20 02:49:16', N'2026-05-26 07:56:59');
INSERT INTO [dbo].[Person] ([ID], [FirstName], [LastName], [Birthdate], [MaritalStatus], [NationalCode], [Mobile], [Address], [Gender], [EmailAddress], [EducationID], [CreatedAt], [UpdatedAt]) VALUES (35, N'Sara', N'Bennett', N'1988-01-05', N'Single', N'0000000035', N'09120000035', N'Demo Address 35', N'Female', N'sara.bennett@example.com', 2, N'2026-05-20 02:49:16', N'2026-05-26 08:41:00');
INSERT INTO [dbo].[Person] ([ID], [FirstName], [LastName], [Birthdate], [MaritalStatus], [NationalCode], [Mobile], [Address], [Gender], [EmailAddress], [EducationID], [CreatedAt], [UpdatedAt]) VALUES (38, N'Omar', N'Carter', N'2006-05-29', N'Single', N'0000000038', N'09120000038', N'Demo Address 38', N'Male', N'omar.carter@example.com', 5, N'2026-05-20 02:49:16', N'2026-05-26 07:56:22');
INSERT INTO [dbo].[Person] ([ID], [FirstName], [LastName], [Birthdate], [MaritalStatus], [NationalCode], [Mobile], [Address], [Gender], [EmailAddress], [EducationID], [CreatedAt], [UpdatedAt]) VALUES (39, N'Lily', N'Adams', N'1995-04-05', N'Single', N'0000000039', N'09120000039', N'Demo Address 39', N'Female', N'lily.adams@example.com', 2, N'2026-05-20 02:49:16', N'2026-05-26 07:48:35');
INSERT INTO [dbo].[Person] ([ID], [FirstName], [LastName], [Birthdate], [MaritalStatus], [NationalCode], [Mobile], [Address], [Gender], [EmailAddress], [EducationID], [CreatedAt], [UpdatedAt]) VALUES (40, N'Emma', N'Johnson', N'2005-04-18', N'Single', N'0000000040', N'09120000040', N'Demo Address 40', N'Female', N'emma.johnson@example.com', 3, N'2026-05-20 02:49:16', N'2026-05-26 07:47:10');
INSERT INTO [dbo].[Person] ([ID], [FirstName], [LastName], [Birthdate], [MaritalStatus], [NationalCode], [Mobile], [Address], [Gender], [EmailAddress], [EducationID], [CreatedAt], [UpdatedAt]) VALUES (41, N'Daniel', N'Wilson', N'1976-11-04', N'Married', N'0000000041', N'09120000041', N'Demo Address 41', N'Male', N'daniel.wilson@example.com', 3, N'2026-05-20 02:49:16', N'2026-05-26 08:00:32');
INSERT INTO [dbo].[Person] ([ID], [FirstName], [LastName], [Birthdate], [MaritalStatus], [NationalCode], [Mobile], [Address], [Gender], [EmailAddress], [EducationID], [CreatedAt], [UpdatedAt]) VALUES (49, N'Noah', N'Brooks', N'1995-04-05', N'Single', N'0000000049', N'09120000049', N'Demo Address 49', N'Male', N'noah.brooks@example.com', 2, N'2026-05-20 02:49:16', N'2026-05-26 07:48:01');
INSERT INTO [dbo].[Person] ([ID], [FirstName], [LastName], [Birthdate], [MaritalStatus], [NationalCode], [Mobile], [Address], [Gender], [EmailAddress], [EducationID], [CreatedAt], [UpdatedAt]) VALUES (50, N'Mia', N'Clark', N'1998-07-10', N'Single', N'0000000050', N'09120000050', N'Demo Address 50', N'Female', N'mia.clark@example.com', 2, N'2026-05-20 02:49:16', N'2026-05-26 07:46:07');
INSERT INTO [dbo].[Person] ([ID], [FirstName], [LastName], [Birthdate], [MaritalStatus], [NationalCode], [Mobile], [Address], [Gender], [EmailAddress], [EducationID], [CreatedAt], [UpdatedAt]) VALUES (61, N'Ryan', N'Miller', N'1996-05-26', N'Single', N'0000000061', N'09120000061', N'Demo Address 61', N'Male', N'ryan.miller@example.com', 3, N'2026-05-26 08:29:33', N'2026-05-26 08:29:33');
SET IDENTITY_INSERT [dbo].[Person] OFF;
GO

-- [dbo].[PersonPhoto] (9 rows)
GO

-- [dbo].[Student] (4 rows)
INSERT INTO [dbo].[Student] ([PersonID], [FirstRegisterDate], [CreatedAt], [UpdatedAt]) VALUES (39, N'2025-06-06', N'2026-05-20 02:49:16', N'2026-05-26 07:48:35');
INSERT INTO [dbo].[Student] ([PersonID], [FirstRegisterDate], [CreatedAt], [UpdatedAt]) VALUES (40, N'2023-11-12', N'2026-05-20 02:49:16', N'2026-05-26 07:47:10');
INSERT INTO [dbo].[Student] ([PersonID], [FirstRegisterDate], [CreatedAt], [UpdatedAt]) VALUES (49, N'2026-05-26', N'2026-05-26 05:35:34', N'2026-05-26 07:48:01');
INSERT INTO [dbo].[Student] ([PersonID], [FirstRegisterDate], [CreatedAt], [UpdatedAt]) VALUES (50, N'2026-05-26', N'2026-05-26 05:35:48', N'2026-05-26 07:46:07');
GO

-- [dbo].[Student_Course_Teacher] (6 rows)
INSERT INTO [dbo].[PersonPhoto] ([PersonID], [PhotoContent], [FileName], [ContentType], [CreatedAt], [UpdatedAt]) VALUES (33, 0x89504E470D0A1A0A0000000D4948445200000100000001000802000000D3103F31000004F349444154789CEDDC318E5D451040D131625F84AC83803D10BCF005EC81807510B21B474E9D1220C148969131CCFF5D75CFC92D7D57F5EDFE1A8DE6DDFB0F1F5FA0EA9B677F00782601902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048FBF6D91FA0E2FEE5F77FFB4FAE1FBF7B9BCFC2DFDEF9F3E8279CF52FA78AFF9700061CFACF11C37F27806187FE73C4F0750430FBDC7F4A09FF8A00969CFB4F29E14B0860E1D17F4D06FF4C006B8FFE6B32F81C012C3FFAAFC9E05302481CFDD764F09A004247FF3519FC4900B9A3FFDA95CFC02FC3754FFF4BFBFFFEA7F40B60FD7FC93E05DD17C0E97F2D3B8DE20B905DF697B8624F41EE0570FAFFD91D9B4F2B80DA76BFCE5D9A52E52B506AA9FF972BF07528F10238FD5FE70ECC6D7F00852DBE9D7BFBF49607B07E7F0F70AF9EE1E600766FEE91EEBD935C1BC0E29D3DC5BD749E3B03D8BAADE7BA374E7561002BF774887BDD6CB705B06F43A7B9774D785500CB7673AC7BD19CF704B0692BE7BBB74C7B49006BF631C8BD62E64B02806E003BAEA289EEF9931F1FC0821D8C760F9FFFEC00A64F7F877BF216660700DD00465F3CCBDC6377313580B913DFEA9EB991A901403780A197CD7AF7C0BDCC0B60E2943BEE69DB99170074031877C104DDA376342C00E80630EB6A29BBE76C6A5200D00D60D0A5C2CB9C7D8D0900BA014CB94E18B7B519014037801117094377372000E80670FE15C2E80D9E1E00BC29019076740087BF9E2CD8E3D101C05B130069E70670F2BBC99A6D9E1B003C800048130069870670EC574696EDF4D000E03104409A00483B318033BF2CB272B32706000F2300D204409A00481300690220EDB8000EFC49198BF77B5C00F04802204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A00483B2E80EBC7EF9EFD1108EDF7B800E09104409A004813006902204D00A49D18C0693F2963F1664F0C001E4600A40980B4430338F0CB222B777A6800F01802204D00A49D1BC0995F1959B6CD73038007100069470770ECBBC99A3D1E1D00BC350190767A0027BF9E2CD8E0E901403D80C3AF1046EF6E4000500FE0FC8B84A15B9B1100D40318719D306E5F6302807A00532E15AE399B9A1400D4031874B5645DA376342C00A80730EB82A9B9A66D675E0013A71C710DDCCBC800A01EC0C4CB66B76BE646A6063077E22B5D6377313800A80730F7E2D9E49ABC85D9014C9FFE02D7F0F98F0F60C10EE6BAE64F7E4300500F60C15534CEB562E64B0258B38F29AE2DD3DE13C0A6AD1CEE5A34E755012CDBCD99AE5D13DE16C0BE0D1DE55A37DB8501ACDCD309AE8D537DF7FEC3C797337CFFC3CFCFFE083CCE6FBFFEF472809D2F007C2101902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048130069EFDE7FF8F8ECCF004FE305204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813002F657F0028AD135E187470B10000000049454E44AE426082, N'demo-person-33.png', N'image/png', N'2026-05-20 02:49:16', N'2026-05-26 07:56:59');
INSERT INTO [dbo].[PersonPhoto] ([PersonID], [PhotoContent], [FileName], [ContentType], [CreatedAt], [UpdatedAt]) VALUES (35, 0x89504E470D0A1A0A0000000D4948445200000100000001000802000000D3103F31000004F349444154789CEDDC318E5D451040D131625F84AC83803D10BCF005EC81807510B21B474E9D1220C148969131CCFF5D75CFC92D7D57F5EDFE1A8DE6DDFB0F1F5FA0EA9B677F00782601902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048FBF6D91FA0E2FEE5F77FFB4FAE1FBF7B9BCFC2DFDEF9F3E8279CF52FA78AFF9700061CFACF11C37F27806187FE73C4F0750430FBDC7F4A09FF8A00969CFB4F29E14B0860E1D17F4D06FF4C006B8FFE6B32F81C012C3FFAAFC9E05302481CFDD764F09A004247FF3519FC4900B9A3FFDA95CFC02FC3754FFF4BFBFFFEA7F40B60FD7FC93E05DD17C0E97F2D3B8DE20B905DF697B8624F41EE0570FAFFD91D9B4F2B80DA76BFCE5D9A52E52B506AA9FF972BF07528F10238FD5FE70ECC6D7F00852DBE9D7BFBF49607B07E7F0F70AF9EE1E600766FEE91EEBD935C1BC0E29D3DC5BD749E3B03D8BAADE7BA374E7561002BF774887BDD6CB705B06F43A7B9774D785500CB7673AC7BD19CF704B0692BE7BBB74C7B49006BF631C8BD62E64B02806E003BAEA289EEF9931F1FC0821D8C760F9FFFEC00A64F7F877BF216660700DD00465F3CCBDC6377313580B913DFEA9EB991A901403780A197CD7AF7C0BDCC0B60E2943BEE69DB99170074031877C104DDA376342C00E80630EB6A29BBE76C6A5200D00D60D0A5C2CB9C7D8D0900BA014CB94E18B7B519014037801117094377372000E80670FE15C2E80D9E1E00BC29019076740087BF9E2CD8E3D101C05B130069E70670F2BBC99A6D9E1B003C800048130069870670EC574696EDF4D000E03104409A00483B318033BF2CB272B32706000F2300D204409A00481300690220EDB8000EFC49198BF77B5C00F04802204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A00483B2E80EBC7EF9EFD1108EDF7B800E09104409A004813006902204D00A49D18C0693F2963F1664F0C001E4600A40980B4430338F0CB222B777A6800F01802204D00A49D1BC0995F1959B6CD73038007100069470770ECBBC99A3D1E1D00BC350190767A0027BF9E2CD8E0E901403D80C3AF1046EF6E4000500FE0FC8B84A15B9B1100D40318719D306E5F6302807A00532E15AE399B9A1400D4031874B5645DA376342C00A80730EB82A9B9A66D675E0013A71C710DDCCBC800A01EC0C4CB66B76BE646A6063077E22B5D6377313800A80730F7E2D9E49ABC85D9014C9FFE02D7F0F98F0F60C10EE6BAE64F7E4300500F60C15534CEB562E64B0258B38F29AE2DD3DE13C0A6AD1CEE5A34E755012CDBCD99AE5D13DE16C0BE0D1DE55A37DB8501ACDCD309AE8D537DF7FEC3C797337CFFC3CFCFFE083CCE6FBFFEF472809D2F007C2101902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048130069EFDE7FF8F8ECCF004FE305204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813002F657F0028AD135E187470B10000000049454E44AE426082, N'demo-person-35.png', N'image/png', N'2026-05-20 02:49:16', N'2026-05-26 08:41:00');
INSERT INTO [dbo].[PersonPhoto] ([PersonID], [PhotoContent], [FileName], [ContentType], [CreatedAt], [UpdatedAt]) VALUES (38, 0x89504E470D0A1A0A0000000D4948445200000100000001000802000000D3103F31000004F349444154789CEDDC318E5D451040D131625F84AC83803D10BCF005EC81807510B21B474E9D1220C148969131CCFF5D75CFC92D7D57F5EDFE1A8DE6DDFB0F1F5FA0EA9B677F00782601902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048FBF6D91FA0E2FEE5F77FFB4FAE1FBF7B9BCFC2DFDEF9F3E8279CF52FA78AFF9700061CFACF11C37F27806187FE73C4F0750430FBDC7F4A09FF8A00969CFB4F29E14B0860E1D17F4D06FF4C006B8FFE6B32F81C012C3FFAAFC9E05302481CFDD764F09A004247FF3519FC4900B9A3FFDA95CFC02FC3754FFF4BFBFFFEA7F40B60FD7FC93E05DD17C0E97F2D3B8DE20B905DF697B8624F41EE0570FAFFD91D9B4F2B80DA76BFCE5D9A52E52B506AA9FF972BF07528F10238FD5FE70ECC6D7F00852DBE9D7BFBF49607B07E7F0F70AF9EE1E600766FEE91EEBD935C1BC0E29D3DC5BD749E3B03D8BAADE7BA374E7561002BF774887BDD6CB705B06F43A7B9774D785500CB7673AC7BD19CF704B0692BE7BBB74C7B49006BF631C8BD62E64B02806E003BAEA289EEF9931F1FC0821D8C760F9FFFEC00A64F7F877BF216660700DD00465F3CCBDC6377313580B913DFEA9EB991A901403780A197CD7AF7C0BDCC0B60E2943BEE69DB99170074031877C104DDA376342C00E80630EB6A29BBE76C6A5200D00D60D0A5C2CB9C7D8D0900BA014CB94E18B7B519014037801117094377372000E80670FE15C2E80D9E1E00BC29019076740087BF9E2CD8E3D101C05B130069E70670F2BBC99A6D9E1B003C800048130069870670EC574696EDF4D000E03104409A00483B318033BF2CB272B32706000F2300D204409A00481300690220EDB8000EFC49198BF77B5C00F04802204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A00483B2E80EBC7EF9EFD1108EDF7B800E09104409A004813006902204D00A49D18C0693F2963F1664F0C001E4600A40980B4430338F0CB222B777A6800F01802204D00A49D1BC0995F1959B6CD73038007100069470770ECBBC99A3D1E1D00BC350190767A0027BF9E2CD8E0E901403D80C3AF1046EF6E4000500FE0FC8B84A15B9B1100D40318719D306E5F6302807A00532E15AE399B9A1400D4031874B5645DA376342C00A80730EB82A9B9A66D675E0013A71C710DDCCBC800A01EC0C4CB66B76BE646A6063077E22B5D6377313800A80730F7E2D9E49ABC85D9014C9FFE02D7F0F98F0F60C10EE6BAE64F7E4300500F60C15534CEB562E64B0258B38F29AE2DD3DE13C0A6AD1CEE5A34E755012CDBCD99AE5D13DE16C0BE0D1DE55A37DB8501ACDCD309AE8D537DF7FEC3C797337CFFC3CFCFFE083CCE6FBFFEF472809D2F007C2101902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048130069EFDE7FF8F8ECCF004FE305204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813002F657F0028AD135E187470B10000000049454E44AE426082, N'demo-person-38.png', N'image/png', N'2026-05-20 02:49:16', N'2026-05-26 07:56:22');
INSERT INTO [dbo].[PersonPhoto] ([PersonID], [PhotoContent], [FileName], [ContentType], [CreatedAt], [UpdatedAt]) VALUES (39, 0x89504E470D0A1A0A0000000D4948445200000100000001000802000000D3103F31000004F349444154789CEDDC318E5D451040D131625F84AC83803D10BCF005EC81807510B21B474E9D1220C148969131CCFF5D75CFC92D7D57F5EDFE1A8DE6DDFB0F1F5FA0EA9B677F00782601902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048FBF6D91FA0E2FEE5F77FFB4FAE1FBF7B9BCFC2DFDEF9F3E8279CF52FA78AFF9700061CFACF11C37F27806187FE73C4F0750430FBDC7F4A09FF8A00969CFB4F29E14B0860E1D17F4D06FF4C006B8FFE6B32F81C012C3FFAAFC9E05302481CFDD764F09A004247FF3519FC4900B9A3FFDA95CFC02FC3754FFF4BFBFFFEA7F40B60FD7FC93E05DD17C0E97F2D3B8DE20B905DF697B8624F41EE0570FAFFD91D9B4F2B80DA76BFCE5D9A52E52B506AA9FF972BF07528F10238FD5FE70ECC6D7F00852DBE9D7BFBF49607B07E7F0F70AF9EE1E600766FEE91EEBD935C1BC0E29D3DC5BD749E3B03D8BAADE7BA374E7561002BF774887BDD6CB705B06F43A7B9774D785500CB7673AC7BD19CF704B0692BE7BBB74C7B49006BF631C8BD62E64B02806E003BAEA289EEF9931F1FC0821D8C760F9FFFEC00A64F7F877BF216660700DD00465F3CCBDC6377313580B913DFEA9EB991A901403780A197CD7AF7C0BDCC0B60E2943BEE69DB99170074031877C104DDA376342C00E80630EB6A29BBE76C6A5200D00D60D0A5C2CB9C7D8D0900BA014CB94E18B7B519014037801117094377372000E80670FE15C2E80D9E1E00BC29019076740087BF9E2CD8E3D101C05B130069E70670F2BBC99A6D9E1B003C800048130069870670EC574696EDF4D000E03104409A00483B318033BF2CB272B32706000F2300D204409A00481300690220EDB8000EFC49198BF77B5C00F04802204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A00483B2E80EBC7EF9EFD1108EDF7B800E09104409A004813006902204D00A49D18C0693F2963F1664F0C001E4600A40980B4430338F0CB222B777A6800F01802204D00A49D1BC0995F1959B6CD73038007100069470770ECBBC99A3D1E1D00BC350190767A0027BF9E2CD8E0E901403D80C3AF1046EF6E4000500FE0FC8B84A15B9B1100D40318719D306E5F6302807A00532E15AE399B9A1400D4031874B5645DA376342C00A80730EB82A9B9A66D675E0013A71C710DDCCBC800A01EC0C4CB66B76BE646A6063077E22B5D6377313800A80730F7E2D9E49ABC85D9014C9FFE02D7F0F98F0F60C10EE6BAE64F7E4300500F60C15534CEB562E64B0258B38F29AE2DD3DE13C0A6AD1CEE5A34E755012CDBCD99AE5D13DE16C0BE0D1DE55A37DB8501ACDCD309AE8D537DF7FEC3C797337CFFC3CFCFFE083CCE6FBFFEF472809D2F007C2101902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048130069EFDE7FF8F8ECCF004FE305204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813002F657F0028AD135E187470B10000000049454E44AE426082, N'demo-person-39.png', N'image/png', N'2026-05-20 02:49:16', N'2026-05-26 07:48:35');
INSERT INTO [dbo].[PersonPhoto] ([PersonID], [PhotoContent], [FileName], [ContentType], [CreatedAt], [UpdatedAt]) VALUES (40, 0x89504E470D0A1A0A0000000D4948445200000100000001000802000000D3103F31000004F349444154789CEDDC318E5D451040D131625F84AC83803D10BCF005EC81807510B21B474E9D1220C148969131CCFF5D75CFC92D7D57F5EDFE1A8DE6DDFB0F1F5FA0EA9B677F00782601902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048FBF6D91FA0E2FEE5F77FFB4FAE1FBF7B9BCFC2DFDEF9F3E8279CF52FA78AFF9700061CFACF11C37F27806187FE73C4F0750430FBDC7F4A09FF8A00969CFB4F29E14B0860E1D17F4D06FF4C006B8FFE6B32F81C012C3FFAAFC9E05302481CFDD764F09A004247FF3519FC4900B9A3FFDA95CFC02FC3754FFF4BFBFFFEA7F40B60FD7FC93E05DD17C0E97F2D3B8DE20B905DF697B8624F41EE0570FAFFD91D9B4F2B80DA76BFCE5D9A52E52B506AA9FF972BF07528F10238FD5FE70ECC6D7F00852DBE9D7BFBF49607B07E7F0F70AF9EE1E600766FEE91EEBD935C1BC0E29D3DC5BD749E3B03D8BAADE7BA374E7561002BF774887BDD6CB705B06F43A7B9774D785500CB7673AC7BD19CF704B0692BE7BBB74C7B49006BF631C8BD62E64B02806E003BAEA289EEF9931F1FC0821D8C760F9FFFEC00A64F7F877BF216660700DD00465F3CCBDC6377313580B913DFEA9EB991A901403780A197CD7AF7C0BDCC0B60E2943BEE69DB99170074031877C104DDA376342C00E80630EB6A29BBE76C6A5200D00D60D0A5C2CB9C7D8D0900BA014CB94E18B7B519014037801117094377372000E80670FE15C2E80D9E1E00BC29019076740087BF9E2CD8E3D101C05B130069E70670F2BBC99A6D9E1B003C800048130069870670EC574696EDF4D000E03104409A00483B318033BF2CB272B32706000F2300D204409A00481300690220EDB8000EFC49198BF77B5C00F04802204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A00483B2E80EBC7EF9EFD1108EDF7B800E09104409A004813006902204D00A49D18C0693F2963F1664F0C001E4600A40980B4430338F0CB222B777A6800F01802204D00A49D1BC0995F1959B6CD73038007100069470770ECBBC99A3D1E1D00BC350190767A0027BF9E2CD8E0E901403D80C3AF1046EF6E4000500FE0FC8B84A15B9B1100D40318719D306E5F6302807A00532E15AE399B9A1400D4031874B5645DA376342C00A80730EB82A9B9A66D675E0013A71C710DDCCBC800A01EC0C4CB66B76BE646A6063077E22B5D6377313800A80730F7E2D9E49ABC85D9014C9FFE02D7F0F98F0F60C10EE6BAE64F7E4300500F60C15534CEB562E64B0258B38F29AE2DD3DE13C0A6AD1CEE5A34E755012CDBCD99AE5D13DE16C0BE0D1DE55A37DB8501ACDCD309AE8D537DF7FEC3C797337CFFC3CFCFFE083CCE6FBFFEF472809D2F007C2101902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048130069EFDE7FF8F8ECCF004FE305204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813002F657F0028AD135E187470B10000000049454E44AE426082, N'demo-person-40.png', N'image/png', N'2026-05-20 02:49:16', N'2026-05-26 07:47:10');
INSERT INTO [dbo].[PersonPhoto] ([PersonID], [PhotoContent], [FileName], [ContentType], [CreatedAt], [UpdatedAt]) VALUES (41, 0x89504E470D0A1A0A0000000D4948445200000100000001000802000000D3103F31000004F349444154789CEDDC318E5D451040D131625F84AC83803D10BCF005EC81807510B21B474E9D1220C148969131CCFF5D75CFC92D7D57F5EDFE1A8DE6DDFB0F1F5FA0EA9B677F00782601902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048FBF6D91FA0E2FEE5F77FFB4FAE1FBF7B9BCFC2DFDEF9F3E8279CF52FA78AFF9700061CFACF11C37F27806187FE73C4F0750430FBDC7F4A09FF8A00969CFB4F29E14B0860E1D17F4D06FF4C006B8FFE6B32F81C012C3FFAAFC9E05302481CFDD764F09A004247FF3519FC4900B9A3FFDA95CFC02FC3754FFF4BFBFFFEA7F40B60FD7FC93E05DD17C0E97F2D3B8DE20B905DF697B8624F41EE0570FAFFD91D9B4F2B80DA76BFCE5D9A52E52B506AA9FF972BF07528F10238FD5FE70ECC6D7F00852DBE9D7BFBF49607B07E7F0F70AF9EE1E600766FEE91EEBD935C1BC0E29D3DC5BD749E3B03D8BAADE7BA374E7561002BF774887BDD6CB705B06F43A7B9774D785500CB7673AC7BD19CF704B0692BE7BBB74C7B49006BF631C8BD62E64B02806E003BAEA289EEF9931F1FC0821D8C760F9FFFEC00A64F7F877BF216660700DD00465F3CCBDC6377313580B913DFEA9EB991A901403780A197CD7AF7C0BDCC0B60E2943BEE69DB99170074031877C104DDA376342C00E80630EB6A29BBE76C6A5200D00D60D0A5C2CB9C7D8D0900BA014CB94E18B7B519014037801117094377372000E80670FE15C2E80D9E1E00BC29019076740087BF9E2CD8E3D101C05B130069E70670F2BBC99A6D9E1B003C800048130069870670EC574696EDF4D000E03104409A00483B318033BF2CB272B32706000F2300D204409A00481300690220EDB8000EFC49198BF77B5C00F04802204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A00483B2E80EBC7EF9EFD1108EDF7B800E09104409A004813006902204D00A49D18C0693F2963F1664F0C001E4600A40980B4430338F0CB222B777A6800F01802204D00A49D1BC0995F1959B6CD73038007100069470770ECBBC99A3D1E1D00BC350190767A0027BF9E2CD8E0E901403D80C3AF1046EF6E4000500FE0FC8B84A15B9B1100D40318719D306E5F6302807A00532E15AE399B9A1400D4031874B5645DA376342C00A80730EB82A9B9A66D675E0013A71C710DDCCBC800A01EC0C4CB66B76BE646A6063077E22B5D6377313800A80730F7E2D9E49ABC85D9014C9FFE02D7F0F98F0F60C10EE6BAE64F7E4300500F60C15534CEB562E64B0258B38F29AE2DD3DE13C0A6AD1CEE5A34E755012CDBCD99AE5D13DE16C0BE0D1DE55A37DB8501ACDCD309AE8D537DF7FEC3C797337CFFC3CFCFFE083CCE6FBFFEF472809D2F007C2101902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048130069EFDE7FF8F8ECCF004FE305204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813002F657F0028AD135E187470B10000000049454E44AE426082, N'demo-person-41.png', N'image/png', N'2026-05-20 02:49:16', N'2026-05-26 08:00:32');
INSERT INTO [dbo].[PersonPhoto] ([PersonID], [PhotoContent], [FileName], [ContentType], [CreatedAt], [UpdatedAt]) VALUES (49, 0x89504E470D0A1A0A0000000D4948445200000100000001000802000000D3103F31000004F349444154789CEDDC318E5D451040D131625F84AC83803D10BCF005EC81807510B21B474E9D1220C148969131CCFF5D75CFC92D7D57F5EDFE1A8DE6DDFB0F1F5FA0EA9B677F00782601902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048FBF6D91FA0E2FEE5F77FFB4FAE1FBF7B9BCFC2DFDEF9F3E8279CF52FA78AFF9700061CFACF11C37F27806187FE73C4F0750430FBDC7F4A09FF8A00969CFB4F29E14B0860E1D17F4D06FF4C006B8FFE6B32F81C012C3FFAAFC9E05302481CFDD764F09A004247FF3519FC4900B9A3FFDA95CFC02FC3754FFF4BFBFFFEA7F40B60FD7FC93E05DD17C0E97F2D3B8DE20B905DF697B8624F41EE0570FAFFD91D9B4F2B80DA76BFCE5D9A52E52B506AA9FF972BF07528F10238FD5FE70ECC6D7F00852DBE9D7BFBF49607B07E7F0F70AF9EE1E600766FEE91EEBD935C1BC0E29D3DC5BD749E3B03D8BAADE7BA374E7561002BF774887BDD6CB705B06F43A7B9774D785500CB7673AC7BD19CF704B0692BE7BBB74C7B49006BF631C8BD62E64B02806E003BAEA289EEF9931F1FC0821D8C760F9FFFEC00A64F7F877BF216660700DD00465F3CCBDC6377313580B913DFEA9EB991A901403780A197CD7AF7C0BDCC0B60E2943BEE69DB99170074031877C104DDA376342C00E80630EB6A29BBE76C6A5200D00D60D0A5C2CB9C7D8D0900BA014CB94E18B7B519014037801117094377372000E80670FE15C2E80D9E1E00BC29019076740087BF9E2CD8E3D101C05B130069E70670F2BBC99A6D9E1B003C800048130069870670EC574696EDF4D000E03104409A00483B318033BF2CB272B32706000F2300D204409A00481300690220EDB8000EFC49198BF77B5C00F04802204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A00483B2E80EBC7EF9EFD1108EDF7B800E09104409A004813006902204D00A49D18C0693F2963F1664F0C001E4600A40980B4430338F0CB222B777A6800F01802204D00A49D1BC0995F1959B6CD73038007100069470770ECBBC99A3D1E1D00BC350190767A0027BF9E2CD8E0E901403D80C3AF1046EF6E4000500FE0FC8B84A15B9B1100D40318719D306E5F6302807A00532E15AE399B9A1400D4031874B5645DA376342C00A80730EB82A9B9A66D675E0013A71C710DDCCBC800A01EC0C4CB66B76BE646A6063077E22B5D6377313800A80730F7E2D9E49ABC85D9014C9FFE02D7F0F98F0F60C10EE6BAE64F7E4300500F60C15534CEB562E64B0258B38F29AE2DD3DE13C0A6AD1CEE5A34E755012CDBCD99AE5D13DE16C0BE0D1DE55A37DB8501ACDCD309AE8D537DF7FEC3C797337CFFC3CFCFFE083CCE6FBFFEF472809D2F007C2101902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048130069EFDE7FF8F8ECCF004FE305204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813002F657F0028AD135E187470B10000000049454E44AE426082, N'demo-person-49.png', N'image/png', N'2026-05-20 02:49:16', N'2026-05-26 07:48:01');
INSERT INTO [dbo].[PersonPhoto] ([PersonID], [PhotoContent], [FileName], [ContentType], [CreatedAt], [UpdatedAt]) VALUES (50, 0x89504E470D0A1A0A0000000D4948445200000100000001000802000000D3103F31000004F349444154789CEDDC318E5D451040D131625F84AC83803D10BCF005EC81807510B21B474E9D1220C148969131CCFF5D75CFC92D7D57F5EDFE1A8DE6DDFB0F1F5FA0EA9B677F00782601902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048FBF6D91FA0E2FEE5F77FFB4FAE1FBF7B9BCFC2DFDEF9F3E8279CF52FA78AFF9700061CFACF11C37F27806187FE73C4F0750430FBDC7F4A09FF8A00969CFB4F29E14B0860E1D17F4D06FF4C006B8FFE6B32F81C012C3FFAAFC9E05302481CFDD764F09A004247FF3519FC4900B9A3FFDA95CFC02FC3754FFF4BFBFFFEA7F40B60FD7FC93E05DD17C0E97F2D3B8DE20B905DF697B8624F41EE0570FAFFD91D9B4F2B80DA76BFCE5D9A52E52B506AA9FF972BF07528F10238FD5FE70ECC6D7F00852DBE9D7BFBF49607B07E7F0F70AF9EE1E600766FEE91EEBD935C1BC0E29D3DC5BD749E3B03D8BAADE7BA374E7561002BF774887BDD6CB705B06F43A7B9774D785500CB7673AC7BD19CF704B0692BE7BBB74C7B49006BF631C8BD62E64B02806E003BAEA289EEF9931F1FC0821D8C760F9FFFEC00A64F7F877BF216660700DD00465F3CCBDC6377313580B913DFEA9EB991A901403780A197CD7AF7C0BDCC0B60E2943BEE69DB99170074031877C104DDA376342C00E80630EB6A29BBE76C6A5200D00D60D0A5C2CB9C7D8D0900BA014CB94E18B7B519014037801117094377372000E80670FE15C2E80D9E1E00BC29019076740087BF9E2CD8E3D101C05B130069E70670F2BBC99A6D9E1B003C800048130069870670EC574696EDF4D000E03104409A00483B318033BF2CB272B32706000F2300D204409A00481300690220EDB8000EFC49198BF77B5C00F04802204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A00483B2E80EBC7EF9EFD1108EDF7B800E09104409A004813006902204D00A49D18C0693F2963F1664F0C001E4600A40980B4430338F0CB222B777A6800F01802204D00A49D1BC0995F1959B6CD73038007100069470770ECBBC99A3D1E1D00BC350190767A0027BF9E2CD8E0E901403D80C3AF1046EF6E4000500FE0FC8B84A15B9B1100D40318719D306E5F6302807A00532E15AE399B9A1400D4031874B5645DA376342C00A80730EB82A9B9A66D675E0013A71C710DDCCBC800A01EC0C4CB66B76BE646A6063077E22B5D6377313800A80730F7E2D9E49ABC85D9014C9FFE02D7F0F98F0F60C10EE6BAE64F7E4300500F60C15534CEB562E64B0258B38F29AE2DD3DE13C0A6AD1CEE5A34E755012CDBCD99AE5D13DE16C0BE0D1DE55A37DB8501ACDCD309AE8D537DF7FEC3C797337CFFC3CFCFFE083CCE6FBFFEF472809D2F007C2101902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048130069EFDE7FF8F8ECCF004FE305204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813002F657F0028AD135E187470B10000000049454E44AE426082, N'demo-person-50.png', N'image/png', N'2026-05-20 02:49:16', N'2026-05-26 07:46:07');
INSERT INTO [dbo].[PersonPhoto] ([PersonID], [PhotoContent], [FileName], [ContentType], [CreatedAt], [UpdatedAt]) VALUES (61, 0x89504E470D0A1A0A0000000D4948445200000100000001000802000000D3103F31000004F349444154789CEDDC318E5D451040D131625F84AC83803D10BCF005EC81807510B21B474E9D1220C148969131CCFF5D75CFC92D7D57F5EDFE1A8DE6DDFB0F1F5FA0EA9B677F00782601902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048FBF6D91FA0E2FEE5F77FFB4FAE1FBF7B9BCFC2DFDEF9F3E8279CF52FA78AFF9700061CFACF11C37F27806187FE73C4F0750430FBDC7F4A09FF8A00969CFB4F29E14B0860E1D17F4D06FF4C006B8FFE6B32F81C012C3FFAAFC9E05302481CFDD764F09A004247FF3519FC4900B9A3FFDA95CFC02FC3754FFF4BFBFFFEA7F40B60FD7FC93E05DD17C0E97F2D3B8DE20B905DF697B8624F41EE0570FAFFD91D9B4F2B80DA76BFCE5D9A52E52B506AA9FF972BF07528F10238FD5FE70ECC6D7F00852DBE9D7BFBF49607B07E7F0F70AF9EE1E600766FEE91EEBD935C1BC0E29D3DC5BD749E3B03D8BAADE7BA374E7561002BF774887BDD6CB705B06F43A7B9774D785500CB7673AC7BD19CF704B0692BE7BBB74C7B49006BF631C8BD62E64B02806E003BAEA289EEF9931F1FC0821D8C760F9FFFEC00A64F7F877BF216660700DD00465F3CCBDC6377313580B913DFEA9EB991A901403780A197CD7AF7C0BDCC0B60E2943BEE69DB99170074031877C104DDA376342C00E80630EB6A29BBE76C6A5200D00D60D0A5C2CB9C7D8D0900BA014CB94E18B7B519014037801117094377372000E80670FE15C2E80D9E1E00BC29019076740087BF9E2CD8E3D101C05B130069E70670F2BBC99A6D9E1B003C800048130069870670EC574696EDF4D000E03104409A00483B318033BF2CB272B32706000F2300D204409A00481300690220EDB8000EFC49198BF77B5C00F04802204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A00483B2E80EBC7EF9EFD1108EDF7B800E09104409A004813006902204D00A49D18C0693F2963F1664F0C001E4600A40980B4430338F0CB222B777A6800F01802204D00A49D1BC0995F1959B6CD73038007100069470770ECBBC99A3D1E1D00BC350190767A0027BF9E2CD8E0E901403D80C3AF1046EF6E4000500FE0FC8B84A15B9B1100D40318719D306E5F6302807A00532E15AE399B9A1400D4031874B5645DA376342C00A80730EB82A9B9A66D675E0013A71C710DDCCBC800A01EC0C4CB66B76BE646A6063077E22B5D6377313800A80730F7E2D9E49ABC85D9014C9FFE02D7F0F98F0F60C10EE6BAE64F7E4300500F60C15534CEB562E64B0258B38F29AE2DD3DE13C0A6AD1CEE5A34E755012CDBCD99AE5D13DE16C0BE0D1DE55A37DB8501ACDCD309AE8D537DF7FEC3C797337CFFC3CFCFFE083CCE6FBFFEF472809D2F007C2101902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A0048130069EFDE7FF8F8ECCF004FE305204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813006902204D00A409803401902600D204409A004813002F657F0028AD135E187470B10000000049454E44AE426082, N'demo-person-61.png', N'image/png', N'2026-05-26 08:29:33', N'2026-05-26 08:29:33');
SET IDENTITY_INSERT [dbo].[Student_Course_Teacher] ON;
INSERT INTO [dbo].[Student_Course_Teacher] ([ID], [StudentID], [CourseID], [TeacherID], [TermNumber], [Score], [CreatedAt], [UpdatedAt]) VALUES (3, 40, 3, 33, 1, 100, N'2026-05-26 08:08:50.6979952', N'2026-05-26 08:08:50.6979952');
INSERT INTO [dbo].[Student_Course_Teacher] ([ID], [StudentID], [CourseID], [TeacherID], [TermNumber], [Score], [CreatedAt], [UpdatedAt]) VALUES (4, 39, 3, 33, 1, 100, N'2026-05-26 08:09:08.8776676', N'2026-05-26 08:09:08.8776676');
INSERT INTO [dbo].[Student_Course_Teacher] ([ID], [StudentID], [CourseID], [TeacherID], [TermNumber], [Score], [CreatedAt], [UpdatedAt]) VALUES (5, 49, 3, 33, 1, 100, N'2026-05-26 08:09:20.8794289', N'2026-05-26 08:09:20.8794289');
INSERT INTO [dbo].[Student_Course_Teacher] ([ID], [StudentID], [CourseID], [TeacherID], [TermNumber], [Score], [CreatedAt], [UpdatedAt]) VALUES (6, 50, 3, 33, 1, 100, N'2026-05-26 08:09:37.6391391', N'2026-05-26 08:09:44.7514847');
INSERT INTO [dbo].[Student_Course_Teacher] ([ID], [StudentID], [CourseID], [TeacherID], [TermNumber], [Score], [CreatedAt], [UpdatedAt]) VALUES (7, 40, 10, 61, 3, 100, N'2026-05-26 08:40:14.1702126', N'2026-05-26 08:40:14.1702126');
INSERT INTO [dbo].[Student_Course_Teacher] ([ID], [StudentID], [CourseID], [TeacherID], [TermNumber], [Score], [CreatedAt], [UpdatedAt]) VALUES (8, 40, 11, 61, 1, 100, N'2026-05-26 08:40:27.9660074', N'2026-05-26 08:40:27.9660074');
SET IDENTITY_INSERT [dbo].[Student_Course_Teacher] OFF;
GO

-- [dbo].[StudentCourseCertificate] (6 rows)
SET IDENTITY_INSERT [dbo].[StudentCourseCertificate] ON;
INSERT INTO [dbo].[StudentCourseCertificate] ([ID], [RegistrationID], [CertificateNumber], [IssueDate], [CreatedAt], [UpdatedAt]) VALUES (1, 7, N'CERT-2026-000001', N'2026-05-26', N'2026-05-27 04:22:34', N'2026-05-27 04:22:34');
INSERT INTO [dbo].[StudentCourseCertificate] ([ID], [RegistrationID], [CertificateNumber], [IssueDate], [CreatedAt], [UpdatedAt]) VALUES (2, 8, N'CERT-2026-000002', N'2026-05-26', N'2026-05-27 04:47:12', N'2026-05-27 04:47:12');
INSERT INTO [dbo].[StudentCourseCertificate] ([ID], [RegistrationID], [CertificateNumber], [IssueDate], [CreatedAt], [UpdatedAt]) VALUES (3, 3, N'CERT-2026-000003', N'2026-05-26', N'2026-05-27 04:47:30', N'2026-05-27 04:47:30');
INSERT INTO [dbo].[StudentCourseCertificate] ([ID], [RegistrationID], [CertificateNumber], [IssueDate], [CreatedAt], [UpdatedAt]) VALUES (4, 5, N'CERT-2026-000004', N'2026-05-26', N'2026-05-27 04:47:43', N'2026-05-27 04:47:43');
INSERT INTO [dbo].[StudentCourseCertificate] ([ID], [RegistrationID], [CertificateNumber], [IssueDate], [CreatedAt], [UpdatedAt]) VALUES (5, 4, N'CERT-2026-000005', N'2026-05-26', N'2026-05-27 04:59:08', N'2026-05-27 04:59:08');
INSERT INTO [dbo].[StudentCourseCertificate] ([ID], [RegistrationID], [CertificateNumber], [IssueDate], [CreatedAt], [UpdatedAt]) VALUES (6, 6, N'CERT-2026-000006', N'2026-05-26', N'2026-05-27 04:59:23', N'2026-05-27 04:59:23');
SET IDENTITY_INSERT [dbo].[StudentCourseCertificate] OFF;
GO

-- [dbo].[Teacher] (3 rows)
GO

-- [dbo].[Teacher_Certification] (0 rows)

-- [dbo].[Users] (6 rows)
INSERT INTO [dbo].[Teacher] ([PersonID], [InsuranceNumber], [AccountNumber], [StartDate], [CreatedAt], [UpdatedAt]) VALUES (33, '1000033', '2000000000000033', N'2000-01-25', N'2026-05-20 02:49:16', N'2026-05-26 07:56:59');
INSERT INTO [dbo].[Teacher] ([PersonID], [InsuranceNumber], [AccountNumber], [StartDate], [CreatedAt], [UpdatedAt]) VALUES (41, '1000041', '2000000000000041', N'2020-01-27', N'2026-05-20 02:49:16', N'2026-05-26 08:00:32');
INSERT INTO [dbo].[Teacher] ([PersonID], [InsuranceNumber], [AccountNumber], [StartDate], [CreatedAt], [UpdatedAt]) VALUES (61, '1000061', '2000000000000061', N'2026-05-26', N'2026-05-26 08:29:33', N'2026-05-26 08:29:33');
SET IDENTITY_INSERT [dbo].[Users] ON;
INSERT INTO [dbo].[Users] ([ID], [UserName], [FirstName], [LastName], [isAdmin], [isActive], [PersonID], [PasswordHash], [PasswordSalt], [PasswordIterations], [CreatedAt], [UpdatedAt]) VALUES (1, N'admin.demo', N'Emma', N'Johnson', 1, 1, 40, 0xF2A103F17A3FE6F20B4531E8B2DB81CAA19DDD8A8C878ABAA56C7A7096A4B001, 0xFFB47A9E514D7C9076DE716763935D0D, 210000, N'2026-05-20 02:49:16', N'2026-05-26 05:49:15');
INSERT INTO [dbo].[Users] ([ID], [UserName], [FirstName], [LastName], [isAdmin], [isActive], [PersonID], [PasswordHash], [PasswordSalt], [PasswordIterations], [CreatedAt], [UpdatedAt]) VALUES (3, N'student.lily', N'Lily', N'Adams', 0, 1, 39, 0xF283BB3F784DE80A4ACDF0FD6BD02D33EC3A279C8EA49E3FCE17EED5D1EB7AEC, 0xFE9D6CAF80950B71BDDFE1152814E081, 210000, N'2026-05-20 02:49:16', N'2026-05-26 05:49:49');
INSERT INTO [dbo].[Users] ([ID], [UserName], [FirstName], [LastName], [isAdmin], [isActive], [PersonID], [PasswordHash], [PasswordSalt], [PasswordIterations], [CreatedAt], [UpdatedAt]) VALUES (4, N'student.noah', N'Noah', N'Brooks', 0, 1, 49, 0x2EA890CBEB38EE146CF61924ABCAC7505F8336D607D2DFC485B64E56F0BD23B9, 0xB2E85E9DA72A829288DE1FDB3C951386, 210000, N'2026-05-20 02:49:16', N'2026-05-26 05:50:13');
INSERT INTO [dbo].[Users] ([ID], [UserName], [FirstName], [LastName], [isAdmin], [isActive], [PersonID], [PasswordHash], [PasswordSalt], [PasswordIterations], [CreatedAt], [UpdatedAt]) VALUES (7, N'student.mia', N'Mia', N'Clark', 0, 1, 50, 0xD4B204B848431B1ED46F43A0E9E0E0896917129E2959FAC6A79F66BEEEE3DC86, 0xAE1D88D7E67D5A8CF5284CB68A983A3F, 210000, N'2026-05-20 02:49:16', N'2026-05-26 05:50:34');
INSERT INTO [dbo].[Users] ([ID], [UserName], [FirstName], [LastName], [isAdmin], [isActive], [PersonID], [PasswordHash], [PasswordSalt], [PasswordIterations], [CreatedAt], [UpdatedAt]) VALUES (14, N'teacher.daniel', N'Daniel', N'Wilson', 0, 1, 41, 0x2EAB8483E23C54402F38A8EA2DC7B5888B8C68FD9143ED59CFF7DC214220095E, 0x614DC4325B392DA5F4A4C320B4933871, 210000, N'2026-05-26 05:48:38', N'2026-05-26 05:48:38');
INSERT INTO [dbo].[Users] ([ID], [UserName], [FirstName], [LastName], [isAdmin], [isActive], [PersonID], [PasswordHash], [PasswordSalt], [PasswordIterations], [CreatedAt], [UpdatedAt]) VALUES (15, N'admin.omar', N'Omar', N'Carter', 1, 1, 38, 0x1C356BB87F01F3C071AABC21B371CAA76DDE306FD6A84E3A50612BBD8966A3B3, 0xDDF6FE6A4CEB0597A22AF65D3B7D8F60, 210000, N'2026-05-26 07:43:54', N'2026-05-26 07:43:54');
SET IDENTITY_INSERT [dbo].[Users] OFF;
GO

-- Foreign keys
ALTER TABLE [dbo].[Course] WITH CHECK ADD CONSTRAINT [FK_Course_Course] FOREIGN KEY ([PrerequisiteCourseID]) REFERENCES [dbo].[Course] ([ID]);
ALTER TABLE [dbo].[Course] CHECK CONSTRAINT [FK_Course_Course];
ALTER TABLE [dbo].[Course] WITH CHECK ADD CONSTRAINT [FK_Course_CourseCategory] FOREIGN KEY ([CourseCategoryID]) REFERENCES [dbo].[CourseCategory] ([ID]);
ALTER TABLE [dbo].[Course] CHECK CONSTRAINT [FK_Course_CourseCategory];
ALTER TABLE [dbo].[CourseSchedule] WITH CHECK ADD CONSTRAINT [FK_CourseSchedule_Course] FOREIGN KEY ([CourseID]) REFERENCES [dbo].[Course] ([ID]);
ALTER TABLE [dbo].[CourseSchedule] CHECK CONSTRAINT [FK_CourseSchedule_Course];
ALTER TABLE [dbo].[CourseSchedule] WITH CHECK ADD CONSTRAINT [FK_CourseSchedule_Teacher] FOREIGN KEY ([TeacherID]) REFERENCES [dbo].[Teacher] ([PersonID]);
ALTER TABLE [dbo].[CourseSchedule] CHECK CONSTRAINT [FK_CourseSchedule_Teacher];
ALTER TABLE [dbo].[Employee] WITH CHECK ADD CONSTRAINT [FK_Employee_Department] FOREIGN KEY ([DepartmentID]) REFERENCES [dbo].[Department] ([ID]);
ALTER TABLE [dbo].[Employee] CHECK CONSTRAINT [FK_Employee_Department];
ALTER TABLE [dbo].[Employee] WITH CHECK ADD CONSTRAINT [FK_Employee_Job] FOREIGN KEY ([JobID]) REFERENCES [dbo].[Job] ([ID]);
ALTER TABLE [dbo].[Employee] CHECK CONSTRAINT [FK_Employee_Job];
ALTER TABLE [dbo].[Employee] WITH CHECK ADD CONSTRAINT [FK_Employee_Person] FOREIGN KEY ([PersonID]) REFERENCES [dbo].[Person] ([ID]);
ALTER TABLE [dbo].[Employee] CHECK CONSTRAINT [FK_Employee_Person];
ALTER TABLE [dbo].[Person] WITH CHECK ADD CONSTRAINT [FK_Person_Education] FOREIGN KEY ([EducationID]) REFERENCES [dbo].[Education] ([ID]);
ALTER TABLE [dbo].[Person] CHECK CONSTRAINT [FK_Person_Education];
ALTER TABLE [dbo].[PersonPhoto] WITH CHECK ADD CONSTRAINT [FK_PersonPhoto_Person] FOREIGN KEY ([PersonID]) REFERENCES [dbo].[Person] ([ID]);
ALTER TABLE [dbo].[PersonPhoto] CHECK CONSTRAINT [FK_PersonPhoto_Person];
ALTER TABLE [dbo].[Student] WITH CHECK ADD CONSTRAINT [FK_Student_Person] FOREIGN KEY ([PersonID]) REFERENCES [dbo].[Person] ([ID]);
ALTER TABLE [dbo].[Student] CHECK CONSTRAINT [FK_Student_Person];
ALTER TABLE [dbo].[Student_Course_Teacher] WITH CHECK ADD CONSTRAINT [FK_Student_Course_Teacher_Course] FOREIGN KEY ([CourseID]) REFERENCES [dbo].[Course] ([ID]);
ALTER TABLE [dbo].[Student_Course_Teacher] CHECK CONSTRAINT [FK_Student_Course_Teacher_Course];
ALTER TABLE [dbo].[Student_Course_Teacher] WITH CHECK ADD CONSTRAINT [FK_Student_Course_Teacher_Student] FOREIGN KEY ([StudentID]) REFERENCES [dbo].[Student] ([PersonID]);
ALTER TABLE [dbo].[Student_Course_Teacher] CHECK CONSTRAINT [FK_Student_Course_Teacher_Student];
ALTER TABLE [dbo].[Student_Course_Teacher] WITH CHECK ADD CONSTRAINT [FK_Student_Course_Teacher_Teacher] FOREIGN KEY ([TeacherID]) REFERENCES [dbo].[Teacher] ([PersonID]);
ALTER TABLE [dbo].[Student_Course_Teacher] CHECK CONSTRAINT [FK_Student_Course_Teacher_Teacher];
ALTER TABLE [dbo].[StudentCourseCertificate] WITH CHECK ADD CONSTRAINT [FK_StudentCourseCertificate_Registration] FOREIGN KEY ([RegistrationID]) REFERENCES [dbo].[Student_Course_Teacher] ([ID]);
ALTER TABLE [dbo].[StudentCourseCertificate] CHECK CONSTRAINT [FK_StudentCourseCertificate_Registration];
ALTER TABLE [dbo].[Teacher] WITH CHECK ADD CONSTRAINT [FK_Teacher_Person] FOREIGN KEY ([PersonID]) REFERENCES [dbo].[Person] ([ID]);
ALTER TABLE [dbo].[Teacher] CHECK CONSTRAINT [FK_Teacher_Person];
ALTER TABLE [dbo].[Teacher_Certification] WITH CHECK ADD CONSTRAINT [FK_Teacher_Certification_Certification] FOREIGN KEY ([CertificationID]) REFERENCES [dbo].[Certification] ([ID]);
ALTER TABLE [dbo].[Teacher_Certification] CHECK CONSTRAINT [FK_Teacher_Certification_Certification];
ALTER TABLE [dbo].[Teacher_Certification] WITH CHECK ADD CONSTRAINT [FK_Teacher_Certification_Teacher] FOREIGN KEY ([TeacherID]) REFERENCES [dbo].[Teacher] ([PersonID]);
ALTER TABLE [dbo].[Teacher_Certification] CHECK CONSTRAINT [FK_Teacher_Certification_Teacher];
ALTER TABLE [dbo].[Users] WITH CHECK ADD CONSTRAINT [FK_Users_Person_PersonID] FOREIGN KEY ([PersonID]) REFERENCES [dbo].[Person] ([ID]);
ALTER TABLE [dbo].[Users] CHECK CONSTRAINT [FK_Users_Person_PersonID];
GO

-- Stored procedures and triggers
CREATE   PROCEDURE dbo.DeleteCourse
    @ID int
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        IF OBJECT_ID(N'dbo.Student_Course_Teacher', N'U') IS NOT NULL
        BEGIN
            DECLARE @RegistrationCount int = 0;

            EXEC sys.sp_executesql
                N'SELECT @RegistrationCount = COUNT(1)
                  FROM dbo.Student_Course_Teacher
                  WHERE CourseID = @CourseID;',
                N'@CourseID int, @RegistrationCount int OUTPUT',
                @CourseID = @ID,
                @RegistrationCount = @RegistrationCount OUTPUT;

            IF @RegistrationCount > 0
                THROW 51310, 'Cannot delete this course because it has course registrations. Delete those registrations first.', 1;
        END;

        IF EXISTS (
            SELECT 1
            FROM dbo.CourseSchedule
            WHERE CourseID = @ID
        )
            THROW 51311, 'Cannot delete this course because it has course schedules. Delete those schedules first.', 1;

        IF EXISTS (
            SELECT 1
            FROM dbo.Course
            WHERE PrerequisiteCourseID = @ID
        )
            THROW 51312, 'Cannot delete this course because another course uses it as a prerequisite.', 1;

        DELETE FROM dbo.Course
        WHERE ID = @ID;

        COMMIT TRANSACTION;
        SELECT 'Success' AS Result;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
GO

CREATE   PROCEDURE dbo.DeleteEmployee
    @person_id int
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        DELETE FROM dbo.Employee
        WHERE PersonID = @person_id;

        COMMIT TRANSACTION;
        SELECT 'Success' AS Result;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;

        THROW;
    END CATCH;
END;
GO

CREATE   PROCEDURE dbo.DeleteStudent
    @PersonID int
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        IF EXISTS (
            SELECT 1
            FROM dbo.Student_Course_Teacher
            WHERE StudentID = @PersonID
        )
            THROW 51200, 'Cannot delete this student role because it has course registrations. Delete those registrations first.', 1;

        DELETE FROM dbo.Student
        WHERE PersonID = @PersonID;

        COMMIT TRANSACTION;
        SELECT 'Success' AS Result;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;

        THROW;
    END CATCH
END;
GO

CREATE   PROCEDURE dbo.DeleteTeacher
    @PersonID int
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        IF EXISTS (
            SELECT 1
            FROM dbo.Student_Course_Teacher
            WHERE TeacherID = @PersonID
        )
            THROW 51201, 'Cannot delete this teacher role because it is used in course registrations. Delete those registrations first.', 1;

        IF EXISTS (
            SELECT 1
            FROM dbo.Teacher_Certification
            WHERE TeacherID = @PersonID
        )
            THROW 51202, 'Cannot delete this teacher role because it has certifications. Delete those certifications first.', 1;

        DELETE FROM dbo.Teacher
        WHERE PersonID = @PersonID;

        COMMIT TRANSACTION;
        SELECT 'Success' AS Result;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;

        THROW;
    END CATCH
END;
GO

CREATE   PROCEDURE dbo.RegisterEmployee
    @FirstName nvarchar(20),
    @LastName nvarchar(50),
    @Birthdate date,
    @MaritalStatus nvarchar(20),
    @NationalCode varchar(10),
    @Mobile varchar(11),
    @Address nvarchar(500) = NULL,
    @Gender nvarchar(20),
    @EmailAddress varchar(100) = NULL,
    @EducationID int,
    @TotalChildren tinyint,
    @StartDate date,
    @InsuranceNumber varchar(7),
    @AccountNumber varchar(16),
    @HireDate date,
    @DepartmentID int,
    @JobID int
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        DECLARE @PersonID int;

        INSERT INTO dbo.Person
            (FirstName, LastName, Birthdate, MaritalStatus, NationalCode, Mobile,
             Address, Gender, EmailAddress, EducationID)
        VALUES
            (@FirstName, @LastName, @Birthdate, @MaritalStatus, @NationalCode, @Mobile,
             @Address, @Gender, @EmailAddress, @EducationID);

        SELECT @PersonID = CONVERT(int, SCOPE_IDENTITY());

        INSERT INTO dbo.Employee
            (PersonID, TotalChildren, StartDate, InsuranceNumber,
             AccountNumber, HireDate, DepartmentID, JobID)
        VALUES
            (@PersonID, @TotalChildren, @StartDate, @InsuranceNumber,
             @AccountNumber, @HireDate, @DepartmentID, @JobID);

        COMMIT TRANSACTION;
        SELECT @PersonID AS PersonID;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
GO

CREATE   PROCEDURE dbo.RegisterTeacher
    @FirstName nvarchar(20),
    @LastName nvarchar(50),
    @Birthdate date,
    @MaritalStatus nvarchar(20),
    @NationalCode varchar(10),
    @Mobile varchar(11),
    @Address nvarchar(500) = NULL,
    @Gender nvarchar(20),
    @EmailAddress varchar(100) = NULL,
    @EducationID int,
    @InsuranceNumber varchar(7),
    @AccountNumber varchar(16),
    @StartDate date
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        DECLARE @PersonID int;

        INSERT INTO dbo.Person
            (FirstName, LastName, Birthdate, MaritalStatus, NationalCode, Mobile,
             Address, Gender, EmailAddress, EducationID)
        VALUES
            (@FirstName, @LastName, @Birthdate, @MaritalStatus, @NationalCode, @Mobile,
             @Address, @Gender, @EmailAddress, @EducationID);

        SELECT @PersonID = CONVERT(int, SCOPE_IDENTITY());

        INSERT INTO dbo.Teacher
            (PersonID, InsuranceNumber, AccountNumber, StartDate)
        VALUES
            (@PersonID, @InsuranceNumber, @AccountNumber, @StartDate);

        COMMIT TRANSACTION;
        SELECT @PersonID AS PersonID;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
GO

CREATE   PROCEDURE dbo.UpdateEmployee
    @PersonID int,
    @FirstName nvarchar(20),
    @LastName nvarchar(50),
    @Birthdate date,
    @MaritalStatus nvarchar(20),
    @NationalCode varchar(10),
    @Mobile varchar(11),
    @Address nvarchar(500) = NULL,
    @Gender nvarchar(20),
    @EmailAddress varchar(100) = NULL,
    @EducationID int,
    @TotalChildren tinyint,
    @StartDate date,
    @InsuranceNumber varchar(7),
    @AccountNumber varchar(16),
    @HireDate date,
    @DepartmentID int,
    @JobID int
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        UPDATE dbo.Person
        SET FirstName = @FirstName,
            LastName = @LastName,
            Birthdate = @Birthdate,
            MaritalStatus = @MaritalStatus,
            NationalCode = @NationalCode,
            Mobile = @Mobile,
            Address = @Address,
            Gender = @Gender,
            EmailAddress = @EmailAddress,
            EducationID = @EducationID
        WHERE ID = @PersonID;

        UPDATE dbo.Employee
        SET TotalChildren = @TotalChildren,
            StartDate = @StartDate,
            InsuranceNumber = @InsuranceNumber,
            AccountNumber = @AccountNumber,
            HireDate = @HireDate,
            DepartmentID = @DepartmentID,
            JobID = @JobID
        WHERE PersonID = @PersonID;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
GO

CREATE   PROCEDURE dbo.UpdateTeacher
    @PersonID int,
    @FirstName nvarchar(20),
    @LastName nvarchar(50),
    @Birthdate date,
    @MaritalStatus nvarchar(20),
    @NationalCode varchar(10),
    @Mobile varchar(11),
    @Address nvarchar(500) = NULL,
    @Gender nvarchar(20),
    @EmailAddress varchar(100) = NULL,
    @EducationID int,
    @InsuranceNumber varchar(7),
    @AccountNumber varchar(16),
    @StartDate date
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        UPDATE dbo.Person
        SET FirstName = @FirstName,
            LastName = @LastName,
            Birthdate = @Birthdate,
            MaritalStatus = @MaritalStatus,
            NationalCode = @NationalCode,
            Mobile = @Mobile,
            Address = @Address,
            Gender = @Gender,
            EmailAddress = @EmailAddress,
            EducationID = @EducationID
        WHERE ID = @PersonID;

        UPDATE dbo.Teacher
        SET InsuranceNumber = @InsuranceNumber,
            AccountNumber = @AccountNumber,
            StartDate = @StartDate
        WHERE PersonID = @PersonID;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
GO


CREATE   TRIGGER dbo.[TR_Certification_SetUpdatedAt]
ON dbo.[Certification]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[Certification] AS target
    INNER JOIN inserted
        ON target.[ID] = inserted.[ID];
END;
GO


CREATE   TRIGGER dbo.[TR_Course_SetUpdatedAt]
ON dbo.[Course]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[Course] AS target
    INNER JOIN inserted
        ON target.[ID] = inserted.[ID];
END;
GO


CREATE   TRIGGER dbo.[TR_CourseCategory_SetUpdatedAt]
ON dbo.[CourseCategory]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[CourseCategory] AS target
    INNER JOIN inserted
        ON target.[ID] = inserted.[ID];
END;
GO


CREATE   TRIGGER dbo.[TR_CourseSchedule_SetUpdatedAt]
ON dbo.[CourseSchedule]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[CourseSchedule] AS target
    INNER JOIN inserted
        ON target.[ID] = inserted.[ID];
END;
GO


CREATE   TRIGGER dbo.[TR_Department_SetUpdatedAt]
ON dbo.[Department]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[Department] AS target
    INNER JOIN inserted
        ON target.[ID] = inserted.[ID];
END;
GO


CREATE   TRIGGER dbo.[TR_Education_SetUpdatedAt]
ON dbo.[Education]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[Education] AS target
    INNER JOIN inserted
        ON target.[ID] = inserted.[ID];
END;
GO


CREATE   TRIGGER dbo.[TR_Employee_SetUpdatedAt]
ON dbo.[Employee]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[Employee] AS target
    INNER JOIN inserted
        ON target.[PersonID] = inserted.[PersonID];
END;
GO


CREATE   TRIGGER dbo.[TR_Job_SetUpdatedAt]
ON dbo.[Job]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[Job] AS target
    INNER JOIN inserted
        ON target.[ID] = inserted.[ID];
END;
GO


CREATE   TRIGGER dbo.[TR_Person_SetUpdatedAt]
ON dbo.[Person]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[Person] AS target
    INNER JOIN inserted
        ON target.[ID] = inserted.[ID];
END;
GO

CREATE   TRIGGER dbo.TR_PersonPhoto_SetUpdatedAt
ON dbo.PersonPhoto
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.PersonPhoto AS target
    INNER JOIN inserted
        ON target.PersonID = inserted.PersonID;
END;
GO

CREATE   TRIGGER dbo.TR_Student_Course_Teacher_SetUpdatedAt
ON dbo.Student_Course_Teacher
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.Student_Course_Teacher AS target
    INNER JOIN inserted
        ON target.ID = inserted.ID;
END;
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


CREATE   TRIGGER dbo.[TR_Student_SetUpdatedAt]
ON dbo.[Student]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[Student] AS target
    INNER JOIN inserted
        ON target.[PersonID] = inserted.[PersonID];
END;
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

CREATE   TRIGGER dbo.TR_StudentCourseCertificate_SetUpdatedAt
ON dbo.StudentCourseCertificate
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.StudentCourseCertificate AS target
    INNER JOIN inserted
        ON target.ID = inserted.ID;
END;
GO

CREATE   TRIGGER dbo.TR_Teacher_Certification_SetUpdatedAt
ON dbo.Teacher_Certification
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.Teacher_Certification AS target
    INNER JOIN inserted
        ON target.TeacherID = inserted.TeacherID
       AND target.CertificationID = inserted.CertificationID;
END;
GO


CREATE   TRIGGER dbo.[TR_Teacher_SetUpdatedAt]
ON dbo.[Teacher]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[Teacher] AS target
    INNER JOIN inserted
        ON target.[PersonID] = inserted.[PersonID];
END;
GO


CREATE   TRIGGER dbo.[TR_Users_SetUpdatedAt]
ON dbo.[Users]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF UPDATE(UpdatedAt)
        RETURN;

    UPDATE target
    SET UpdatedAt = SYSUTCDATETIME()
    FROM dbo.[Users] AS target
    INNER JOIN inserted
        ON target.[ID] = inserted.[ID];
END;
GO

