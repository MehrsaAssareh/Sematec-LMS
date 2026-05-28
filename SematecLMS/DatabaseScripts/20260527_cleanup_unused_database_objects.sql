USE [SematecLearningManagementSystem];
GO

SET XACT_ABORT ON;
GO

BEGIN TRANSACTION;

IF OBJECT_ID(N'dbo.DeleteCourseCategory', N'P') IS NOT NULL DROP PROCEDURE dbo.DeleteCourseCategory;
IF OBJECT_ID(N'dbo.EnrollmentDelete', N'P') IS NOT NULL DROP PROCEDURE dbo.EnrollmentDelete;
IF OBJECT_ID(N'dbo.EnrollmentInsert', N'P') IS NOT NULL DROP PROCEDURE dbo.EnrollmentInsert;
IF OBJECT_ID(N'dbo.EnrollmentUpdateScore', N'P') IS NOT NULL DROP PROCEDURE dbo.EnrollmentUpdateScore;
IF OBJECT_ID(N'dbo.GetAllCertifications', N'P') IS NOT NULL DROP PROCEDURE dbo.GetAllCertifications;
IF OBJECT_ID(N'dbo.GetAllCourse', N'P') IS NOT NULL DROP PROCEDURE dbo.GetAllCourse;
IF OBJECT_ID(N'dbo.GetAllDepatrmantList', N'P') IS NOT NULL DROP PROCEDURE dbo.GetAllDepatrmantList;
IF OBJECT_ID(N'dbo.GetAllEducationList', N'P') IS NOT NULL DROP PROCEDURE dbo.GetAllEducationList;
IF OBJECT_ID(N'dbo.GetAllJobList', N'P') IS NOT NULL DROP PROCEDURE dbo.GetAllJobList;
IF OBJECT_ID(N'dbo.GetAllTeacherCertifications', N'P') IS NOT NULL DROP PROCEDURE dbo.GetAllTeacherCertifications;
IF OBJECT_ID(N'dbo.GetCourseByID', N'P') IS NOT NULL DROP PROCEDURE dbo.GetCourseByID;
IF OBJECT_ID(N'dbo.GetCourseCategories', N'P') IS NOT NULL DROP PROCEDURE dbo.GetCourseCategories;
IF OBJECT_ID(N'dbo.GetTeacherCertifications', N'P') IS NOT NULL DROP PROCEDURE dbo.GetTeacherCertifications;
IF OBJECT_ID(N'dbo.DeleteTeacherCertification', N'P') IS NOT NULL DROP PROCEDURE dbo.DeleteTeacherCertification;
IF OBJECT_ID(N'dbo.RegisterCourse', N'P') IS NOT NULL DROP PROCEDURE dbo.RegisterCourse;
IF OBJECT_ID(N'dbo.RegisterCourseCategory', N'P') IS NOT NULL DROP PROCEDURE dbo.RegisterCourseCategory;
IF OBJECT_ID(N'dbo.RegisterStudent', N'P') IS NOT NULL DROP PROCEDURE dbo.RegisterStudent;
IF OBJECT_ID(N'dbo.RegisterTeacherCertification', N'P') IS NOT NULL DROP PROCEDURE dbo.RegisterTeacherCertification;
IF OBJECT_ID(N'dbo.sp_InsertTeacherCertification', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_InsertTeacherCertification;
IF OBJECT_ID(N'dbo.SPEnrollmentGetAll', N'P') IS NOT NULL DROP PROCEDURE dbo.SPEnrollmentGetAll;
IF OBJECT_ID(N'dbo.UpdateCourse', N'P') IS NOT NULL DROP PROCEDURE dbo.UpdateCourse;
IF OBJECT_ID(N'dbo.UpdateCourseCategory', N'P') IS NOT NULL DROP PROCEDURE dbo.UpdateCourseCategory;
IF OBJECT_ID(N'dbo.UpdateStudent', N'P') IS NOT NULL DROP PROCEDURE dbo.UpdateStudent;
IF OBJECT_ID(N'dbo.UpdateTeacherCertification', N'P') IS NOT NULL DROP PROCEDURE dbo.UpdateTeacherCertification;

IF OBJECT_ID(N'dbo.sp_alterdiagram', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_alterdiagram;
IF OBJECT_ID(N'dbo.sp_creatediagram', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_creatediagram;
IF OBJECT_ID(N'dbo.sp_dropdiagram', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_dropdiagram;
IF OBJECT_ID(N'dbo.sp_helpdiagramdefinition', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_helpdiagramdefinition;
IF OBJECT_ID(N'dbo.sp_helpdiagrams', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_helpdiagrams;
IF OBJECT_ID(N'dbo.sp_renamediagram', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_renamediagram;
IF OBJECT_ID(N'dbo.sp_upgraddiagrams', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_upgraddiagrams;
IF OBJECT_ID(N'dbo.fn_diagramobjects', N'FN') IS NOT NULL DROP FUNCTION dbo.fn_diagramobjects;
IF OBJECT_ID(N'dbo.sysdiagrams', N'U') IS NOT NULL DROP TABLE dbo.sysdiagrams;

COMMIT TRANSACTION;
GO
