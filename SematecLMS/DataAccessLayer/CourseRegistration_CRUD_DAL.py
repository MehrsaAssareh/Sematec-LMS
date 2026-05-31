import pyodbc
import uuid
from datetime import date, datetime
from DataAccessLayer.DatabaseConfig import CONNECTION_STRING as DB_CONNECTION_STRING
from Model.CourseRegistrationModel import CourseRegistration_Model_class


class CourseRegistration_CRUD_DAL_Class:
    CONNECTION_STRING = DB_CONNECTION_STRING

    def register_course_registration(self, registration_object: CourseRegistration_Model_class):
        command_text = """
            INSERT INTO dbo.Student_Course_Teacher
                (StudentID, CourseID, TeacherID, TermNumber, Score)
            VALUES (?, ?, ?, ?, ?)
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                registration_object.student_id,
                registration_object.course_id,
                registration_object.teacher_id,
                registration_object.term_number,
                registration_object.score
            ))
            connection.commit()

    def get_course_registrations(self, keyword=None):
        command_text = """
            SELECT
                sct.ID,
                sct.StudentID,
                sct.CourseID,
                sct.TeacherID,
                sct.TermNumber,
                sct.Score,
                student_person.FirstName + N' ' + student_person.LastName AS StudentName,
                c.CourseName,
                teacher_person.FirstName + N' ' + teacher_person.LastName AS TeacherName,
                certificate.ID AS CertificateID,
                certificate.CertificateNumber,
                certificate.IssueDate AS CertificateIssueDate
            FROM dbo.Student_Course_Teacher AS sct
            INNER JOIN dbo.Student AS s ON s.PersonID = sct.StudentID
            INNER JOIN dbo.Person AS student_person ON student_person.ID = s.PersonID
            INNER JOIN dbo.Course AS c ON c.ID = sct.CourseID
            INNER JOIN dbo.Teacher AS t ON t.PersonID = sct.TeacherID
            INNER JOIN dbo.Person AS teacher_person ON teacher_person.ID = t.PersonID
            LEFT JOIN dbo.StudentCourseCertificate AS certificate ON certificate.RegistrationID = sct.ID
            WHERE
                ? IS NULL
                OR student_person.FirstName LIKE ?
                OR student_person.LastName LIKE ?
                OR c.CourseName LIKE ?
                OR teacher_person.FirstName LIKE ?
                OR teacher_person.LastName LIKE ?
                OR CAST(sct.TermNumber AS varchar(20)) LIKE ?
                OR certificate.CertificateNumber LIKE ?
            ORDER BY sct.TermNumber, c.CourseName, student_person.LastName
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
                search_value
            ))
            rows = cursor.fetchall()

        registrations = []
        for row in rows:
            registrations.append(CourseRegistration_Model_class(
                registration_id=row.ID,
                student_id=row.StudentID,
                course_id=row.CourseID,
                teacher_id=row.TeacherID,
                term_number=row.TermNumber,
                score=row.Score,
                student_name=row.StudentName,
                course_name=row.CourseName,
                teacher_name=row.TeacherName,
                certificate_id=row.CertificateID,
                certificate_number=row.CertificateNumber,
                certificate_issue_date=row.CertificateIssueDate
            ))

        return registrations

    def update_course_registration(self, registration_object: CourseRegistration_Model_class, registration_id):
        command_text = """
            UPDATE dbo.Student_Course_Teacher
            SET StudentID = ?,
                CourseID = ?,
                TeacherID = ?,
                TermNumber = ?,
                Score = ?
            WHERE ID = ?
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                registration_object.student_id,
                registration_object.course_id,
                registration_object.teacher_id,
                registration_object.term_number,
                registration_object.score,
                registration_id
            ))
            connection.commit()

    def course_registration_has_certificate(self, registration_id):
        command_text = """
            SELECT COUNT(1)
            FROM dbo.StudentCourseCertificate
            WHERE RegistrationID = ?
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, registration_id)
            return cursor.fetchone()[0] > 0

    def delete_course_registration(self, registration_id):
        command_text = """
            DELETE FROM dbo.Student_Course_Teacher
            WHERE ID = ?
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, registration_id)
            connection.commit()

    def get_form_lookups(self):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT s.PersonID, p.FirstName + N' ' + p.LastName AS FullName
                FROM dbo.Student AS s
                INNER JOIN dbo.Person AS p ON p.ID = s.PersonID
                ORDER BY p.LastName, p.FirstName
            """)
            student_rows = cursor.fetchall()

            cursor.execute("SELECT ID, CourseName FROM dbo.Course ORDER BY CourseName")
            course_rows = cursor.fetchall()

            cursor.execute("""
                SELECT t.PersonID, p.FirstName + N' ' + p.LastName AS FullName
                FROM dbo.Teacher AS t
                INNER JOIN dbo.Person AS p ON p.ID = t.PersonID
                ORDER BY p.LastName, p.FirstName
            """)
            teacher_rows = cursor.fetchall()

        return {
            'student': [(row.PersonID, row.FullName) for row in student_rows],
            'course': [(row.ID, row.CourseName) for row in course_rows],
            'teacher': [(row.PersonID, row.FullName) for row in teacher_rows]
        }

    def make_student_course_certificate(self, registration_id):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    sct.ID,
                    sct.Score,
                    certificate.ID AS CertificateID,
                    certificate.CertificateNumber,
                    certificate.IssueDate AS CertificateIssueDate,
                    student_person.FirstName + N' ' + student_person.LastName AS StudentName,
                    c.CourseName,
                    schedule.ScheduleID,
                    schedule.ActualFinishingDate
                FROM dbo.Student_Course_Teacher AS sct
                INNER JOIN dbo.Student AS s ON s.PersonID = sct.StudentID
                INNER JOIN dbo.Person AS student_person ON student_person.ID = s.PersonID
                INNER JOIN dbo.Course AS c ON c.ID = sct.CourseID
                LEFT JOIN dbo.StudentCourseCertificate AS certificate ON certificate.RegistrationID = sct.ID
                OUTER APPLY (
                    SELECT TOP (1)
                        cs.ID AS ScheduleID,
                        cs.ActualFinishingDate
                    FROM dbo.CourseSchedule AS cs
                    WHERE cs.CourseID = sct.CourseID
                      AND cs.TeacherID = sct.TeacherID
                      AND cs.TermNumber = sct.TermNumber
                    ORDER BY
                        CASE WHEN cs.ActualFinishingDate IS NULL THEN 1 ELSE 0 END,
                        cs.ActualFinishingDate DESC,
                        cs.PlannedFinishingDate DESC,
                        cs.ID DESC
                ) AS schedule
                WHERE sct.ID = ?
            """, registration_id)
            registration = cursor.fetchone()

            if not registration:
                raise ValueError('Please select a valid course registration.')

            if registration.Score is None:
                raise ValueError('Please enter and save a final score before making a certificate.')

            if registration.ScheduleID is None:
                raise ValueError('Please create a matching course schedule before making a certificate.')

            if registration.ActualFinishingDate is None:
                raise ValueError('Please enter and save the course Actual Finishing Date before making a certificate.')

            actual_finishing_date = registration.ActualFinishingDate
            if isinstance(actual_finishing_date, datetime):
                actual_finishing_date = actual_finishing_date.date()
            elif isinstance(actual_finishing_date, str):
                actual_finishing_date = datetime.strptime(actual_finishing_date[:10], '%Y-%m-%d').date()

            if actual_finishing_date > date.today():
                raise ValueError('The course Actual Finishing Date is in the future.')

            if registration.CertificateID:
                return self.create_certificate_result(registration, created=False)

            placeholder_number = f"P-{uuid.uuid4().hex[:24]}"
            cursor.execute("""
                INSERT INTO dbo.StudentCourseCertificate
                    (RegistrationID, CertificateNumber, IssueDate)
                OUTPUT inserted.ID
                VALUES (?, ?, CONVERT(date, GETDATE()))
            """, registration_id, placeholder_number)
            certificate_id = cursor.fetchone()[0]
            cursor.execute("SELECT CONVERT(int, YEAR(GETDATE()))")
            certificate_year = cursor.fetchone()[0]
            certificate_number = f"CERT-{certificate_year}-{certificate_id:06d}"

            cursor.execute("""
                UPDATE dbo.StudentCourseCertificate
                SET CertificateNumber = ?
                WHERE ID = ?
            """, certificate_number, certificate_id)
            connection.commit()

            cursor.execute("""
                SELECT
                    sct.ID,
                    sct.Score,
                    certificate.ID AS CertificateID,
                    certificate.CertificateNumber,
                    certificate.IssueDate AS CertificateIssueDate,
                    student_person.FirstName + N' ' + student_person.LastName AS StudentName,
                    c.CourseName
                FROM dbo.Student_Course_Teacher AS sct
                INNER JOIN dbo.Student AS s ON s.PersonID = sct.StudentID
                INNER JOIN dbo.Person AS student_person ON student_person.ID = s.PersonID
                INNER JOIN dbo.Course AS c ON c.ID = sct.CourseID
                INNER JOIN dbo.StudentCourseCertificate AS certificate ON certificate.RegistrationID = sct.ID
                WHERE sct.ID = ?
            """, registration_id)
            return self.create_certificate_result(cursor.fetchone(), created=True)

    def get_student_course_certificate_pdf_data(self, registration_id):
        command_text = """
            SELECT
                sct.ID AS RegistrationID,
                sct.StudentID,
                sct.CourseID,
                sct.TeacherID,
                sct.TermNumber,
                sct.Score,
                student_person.FirstName + N' ' + student_person.LastName AS StudentName,
                student_person.NationalCode,
                c.CourseCode,
                c.CourseName,
                c.Duration,
                teacher_person.FirstName + N' ' + teacher_person.LastName AS TeacherName,
                certificate.ID AS CertificateID,
                certificate.CertificateNumber,
                certificate.IssueDate AS CertificateIssueDate,
                schedule.PlannedBeginningDate,
                schedule.PlannedFinishingDate,
                schedule.ActualBeginningDate,
                schedule.ActualFinishingDate,
                photo.PhotoContent,
                photo.FileName AS PhotoFileName,
                photo.ContentType AS PhotoContentType
            FROM dbo.Student_Course_Teacher AS sct
            INNER JOIN dbo.Student AS s ON s.PersonID = sct.StudentID
            INNER JOIN dbo.Person AS student_person ON student_person.ID = s.PersonID
            INNER JOIN dbo.Course AS c ON c.ID = sct.CourseID
            INNER JOIN dbo.Teacher AS t ON t.PersonID = sct.TeacherID
            INNER JOIN dbo.Person AS teacher_person ON teacher_person.ID = t.PersonID
            INNER JOIN dbo.StudentCourseCertificate AS certificate ON certificate.RegistrationID = sct.ID
            OUTER APPLY (
                SELECT TOP (1)
                    cs.PlannedBeginningDate,
                    cs.PlannedFinishingDate,
                    cs.ActualBeginningDate,
                    cs.ActualFinishingDate
                FROM dbo.CourseSchedule AS cs
                WHERE cs.CourseID = sct.CourseID
                  AND cs.TeacherID = sct.TeacherID
                  AND cs.TermNumber = sct.TermNumber
                ORDER BY
                    CASE WHEN cs.ActualFinishingDate IS NULL THEN 1 ELSE 0 END,
                    cs.ActualFinishingDate DESC,
                    cs.PlannedFinishingDate DESC,
                    cs.ID DESC
            ) AS schedule
            LEFT JOIN dbo.PersonPhoto AS photo ON photo.PersonID = sct.StudentID
            WHERE sct.ID = ?
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, registration_id)
            row = cursor.fetchone()

        if not row:
            raise ValueError('Please make the certificate before exporting the PDF.')

        if row.PhotoContent is None:
            raise ValueError('Please save a student photo before exporting the certificate PDF.')

        return {
            'registration_id': row.RegistrationID,
            'student_id': row.StudentID,
            'course_id': row.CourseID,
            'teacher_id': row.TeacherID,
            'term_number': row.TermNumber,
            'score': row.Score,
            'student_name': row.StudentName,
            'national_code': row.NationalCode,
            'course_code': row.CourseCode,
            'course_name': row.CourseName,
            'course_duration': row.Duration,
            'teacher_name': row.TeacherName,
            'certificate_id': row.CertificateID,
            'certificate_number': row.CertificateNumber,
            'certificate_issue_date': row.CertificateIssueDate,
            'planned_beginning_date': row.PlannedBeginningDate,
            'planned_finishing_date': row.PlannedFinishingDate,
            'actual_beginning_date': row.ActualBeginningDate,
            'actual_finishing_date': row.ActualFinishingDate,
            'photo_content': bytes(row.PhotoContent),
            'photo_file_name': row.PhotoFileName,
            'photo_content_type': row.PhotoContentType
        }

    def create_certificate_result(self, row, created):
        return {
            'created': created,
            'certificate_id': row.CertificateID,
            'certificate_number': row.CertificateNumber,
            'certificate_issue_date': row.CertificateIssueDate,
            'student_name': row.StudentName,
            'course_name': row.CourseName
        }
