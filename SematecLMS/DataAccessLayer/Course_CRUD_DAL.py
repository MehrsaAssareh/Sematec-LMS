import pyodbc

from DataAccessLayer.DatabaseConfig import CONNECTION_STRING as DB_CONNECTION_STRING
from Model.CourseModel import Course_Model_Class


class Course_CRUD_DAL_Class:
    CONNECTION_STRING = DB_CONNECTION_STRING

    def register_course(self, course_object: Course_Model_Class):
        command_text = """
            INSERT INTO dbo.Course
                (CourseCode, CourseName, Duration, Syllabus, Cost, Status,
                 CourseCategoryID, PrerequisiteCourseID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                course_object.course_code,
                course_object.course_name,
                course_object.duration,
                course_object.syllabus,
                course_object.cost,
                course_object.status,
                course_object.course_category_id,
                course_object.prerequisite_course_id
            ))
            connection.commit()

    def get_courses(self, keyword=None):
        command_text = """
            SELECT
                c.ID,
                c.CourseCode,
                c.CourseName,
                c.Duration,
                c.Syllabus,
                c.Cost,
                c.Status,
                c.CourseCategoryID,
                cc.CourseCategoryName,
                c.PrerequisiteCourseID,
                prereq.CourseName AS PrerequisiteCourseName
            FROM dbo.Course AS c
            LEFT JOIN dbo.CourseCategory AS cc ON cc.ID = c.CourseCategoryID
            LEFT JOIN dbo.Course AS prereq ON prereq.ID = c.PrerequisiteCourseID
            WHERE
                ? IS NULL
                OR CAST(c.CourseCode AS varchar(20)) LIKE ?
                OR c.CourseName LIKE ?
                OR c.Status LIKE ?
                OR cc.CourseCategoryName LIKE ?
                OR prereq.CourseName LIKE ?
            ORDER BY c.ID
        """
        search_value = None if not keyword else f"%{keyword}%"

        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            ))
            rows = cursor.fetchall()

        courses = []
        for row in rows:
            courses.append(Course_Model_Class(
                course_id=row.ID,
                course_code=row.CourseCode,
                course_name=row.CourseName,
                duration=row.Duration,
                syllabus=row.Syllabus,
                cost=row.Cost,
                status=row.Status,
                course_category_id=row.CourseCategoryID,
                prerequisite_course_id=row.PrerequisiteCourseID
            ))

        return courses

    def update_course(self, course_object: Course_Model_Class):
        command_text = """
            UPDATE dbo.Course
            SET CourseCode = ?,
                CourseName = ?,
                Duration = ?,
                Syllabus = ?,
                Cost = ?,
                Status = ?,
                CourseCategoryID = ?,
                PrerequisiteCourseID = ?
            WHERE ID = ?
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                course_object.course_code,
                course_object.course_name,
                course_object.duration,
                course_object.syllabus,
                course_object.cost,
                course_object.status,
                course_object.course_category_id,
                course_object.prerequisite_course_id,
                course_object.course_id
            ))
            connection.commit()

    def delete_course(self, course_id: int):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("EXEC dbo.DeleteCourse ?", course_id)
            row = cursor.fetchone()
            connection.commit()
            return row.Result if row else 'Success'

    def get_form_lookups(self):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT ID, CourseCategoryName FROM dbo.CourseCategory ORDER BY CourseCategoryName")
            category_rows = cursor.fetchall()

            cursor.execute("SELECT ID, CourseName FROM dbo.Course ORDER BY CourseName")
            course_rows = cursor.fetchall()

        return {
            'category': [(row.ID, row.CourseCategoryName) for row in category_rows],
            'course': [(row.ID, row.CourseName) for row in course_rows]
        }
