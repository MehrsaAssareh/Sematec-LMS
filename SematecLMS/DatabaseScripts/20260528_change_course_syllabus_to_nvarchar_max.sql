USE [SematecLearningManagementSystem];
GO

ALTER TABLE [dbo].[Course] ALTER COLUMN [Syllabus] nvarchar(MAX) NOT NULL;
GO
