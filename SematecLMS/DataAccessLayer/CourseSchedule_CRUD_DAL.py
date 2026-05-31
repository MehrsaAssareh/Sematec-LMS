import pyodbc
from DataAccessLayer.DatabaseConfig import CONNECTION_STRING as DB_CONNECTION_STRING
from Model.CourseScheduleModel import CourseSchedule_Model_Class


class CourseSchedule_CRUD_DAL_Class:
    CONNECTION_STRING = DB_CONNECTION_STRING

    def to_db_date(self, value):
        return value.isoformat() if hasattr(value, 'isoformat') else value

    def register_course_schedule(self, schedule_object: CourseSchedule_Model_Class):
        command_text = """
            INSERT INTO dbo.CourseSchedule
                (CourseID, TeacherID, TermNumber, Capacity, RoomName,
                 PlannedBeginningDate, DurationWeek, DurationSessionHour,
                 PlannedFinishingDate, ActualBeginningDate, ActualDurationWeek,
                 ActualFinishingDate, Comments)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                schedule_object.course_id,
                schedule_object.teacher_id,
                schedule_object.term_number,
                schedule_object.capacity,
                schedule_object.room_name,
                self.to_db_date(schedule_object.planned_beginning_date),
                schedule_object.duration_week,
                schedule_object.duration_session_hour,
                self.to_db_date(schedule_object.planned_finishing_date),
                self.to_db_date(schedule_object.actual_beginning_date),
                schedule_object.actual_duration_week,
                self.to_db_date(schedule_object.actual_finishing_date),
                schedule_object.comments
            ))
            connection.commit()

    def get_course_schedules(self, keyword=None):
        command_text = """
            SELECT
                cs.ID,
                cs.CourseID,
                c.CourseName,
                cs.TeacherID,
                teacher_person.FirstName + N' ' + teacher_person.LastName AS TeacherName,
                cs.TermNumber,
                cs.Capacity,
                cs.RoomName,
                CONVERT(varchar(10), cs.PlannedBeginningDate, 23) AS PlannedBeginningDate,
                cs.DurationWeek,
                cs.DurationSessionHour,
                CONVERT(varchar(10), cs.PlannedFinishingDate, 23) AS PlannedFinishingDate,
                CONVERT(varchar(10), cs.ActualBeginningDate, 23) AS ActualBeginningDate,
                cs.ActualDurationWeek,
                CONVERT(varchar(10), cs.ActualFinishingDate, 23) AS ActualFinishingDate,
                cs.Comments
            FROM dbo.CourseSchedule AS cs
            INNER JOIN dbo.Course AS c
                ON c.ID = cs.CourseID
            LEFT JOIN dbo.Teacher AS t
                ON t.PersonID = cs.TeacherID
            LEFT JOIN dbo.Person AS teacher_person
                ON teacher_person.ID = t.PersonID
            WHERE
                ? IS NULL
                OR c.CourseName LIKE ?
                OR teacher_person.FirstName LIKE ?
                OR teacher_person.LastName LIKE ?
                OR cs.RoomName LIKE ?
                OR cs.Comments LIKE ?
                OR CAST(cs.TermNumber AS varchar(20)) LIKE ?
                OR CONVERT(varchar(10), cs.PlannedBeginningDate, 23) LIKE ?
                OR CONVERT(varchar(10), cs.PlannedFinishingDate, 23) LIKE ?
                OR CONVERT(varchar(10), cs.ActualBeginningDate, 23) LIKE ?
                OR CONVERT(varchar(10), cs.ActualFinishingDate, 23) LIKE ?
            ORDER BY cs.PlannedBeginningDate DESC, c.CourseName
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
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            ))
            rows = cursor.fetchall()

        schedules = []
        for row in rows:
            schedules.append(CourseSchedule_Model_Class(
                course_schedule_id=row.ID,
                course_id=row.CourseID,
                course_name=row.CourseName,
                teacher_id=row.TeacherID,
                teacher_name=row.TeacherName,
                term_number=row.TermNumber,
                capacity=row.Capacity,
                room_name=row.RoomName,
                planned_beginning_date=row.PlannedBeginningDate,
                duration_week=row.DurationWeek,
                duration_session_hour=row.DurationSessionHour,
                planned_finishing_date=row.PlannedFinishingDate,
                actual_beginning_date=row.ActualBeginningDate,
                actual_duration_week=row.ActualDurationWeek,
                actual_finishing_date=row.ActualFinishingDate,
                comments=row.Comments
            ))

        return schedules

    def update_course_schedule(self, schedule_object: CourseSchedule_Model_Class):
        command_text = """
            UPDATE dbo.CourseSchedule
            SET CourseID = ?,
                TeacherID = ?,
                TermNumber = ?,
                Capacity = ?,
                RoomName = ?,
                PlannedBeginningDate = ?,
                DurationWeek = ?,
                DurationSessionHour = ?,
                PlannedFinishingDate = ?,
                ActualBeginningDate = ?,
                ActualDurationWeek = ?,
                ActualFinishingDate = ?,
                Comments = ?
            WHERE ID = ?
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                schedule_object.course_id,
                schedule_object.teacher_id,
                schedule_object.term_number,
                schedule_object.capacity,
                schedule_object.room_name,
                self.to_db_date(schedule_object.planned_beginning_date),
                schedule_object.duration_week,
                schedule_object.duration_session_hour,
                self.to_db_date(schedule_object.planned_finishing_date),
                self.to_db_date(schedule_object.actual_beginning_date),
                schedule_object.actual_duration_week,
                self.to_db_date(schedule_object.actual_finishing_date),
                schedule_object.comments,
                schedule_object.course_schedule_id
            ))
            connection.commit()

    def delete_course_schedule(self, course_schedule_id: int):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM dbo.CourseSchedule WHERE ID = ?", course_schedule_id)
            connection.commit()

    def get_form_lookups(self):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT ID, CourseName
                FROM dbo.Course
                WHERE Status = N'Active'
                ORDER BY CourseName
            """)
            course_rows = cursor.fetchall()

            cursor.execute("""
                SELECT t.PersonID, p.FirstName + N' ' + p.LastName AS FullName
                FROM dbo.Teacher AS t
                INNER JOIN dbo.Person AS p ON p.ID = t.PersonID
                ORDER BY p.LastName, p.FirstName
            """)
            teacher_rows = cursor.fetchall()

        return {
            'course': [(row.ID, row.CourseName) for row in course_rows],
            'teacher': [(row.PersonID, row.FullName) for row in teacher_rows]
        }
