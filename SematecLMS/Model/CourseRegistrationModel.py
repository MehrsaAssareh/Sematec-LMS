class CourseRegistration_Model_class:
    def __init__(self,
                 registration_id: int = None,
                 student_id: int = None,
                 course_id: int = None,
                 teacher_id: int = None,
                 term_number: int = None,
                 score: int = None,
                 student_name: str = None,
                 course_name: str = None,
                 teacher_name: str = None,
                 certificate_id: int = None,
                 certificate_number: str = None,
                 certificate_issue_date=None):
        self.registration_id = registration_id
        self.student_id = student_id
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.term_number = term_number
        self.score = score
        self.student_name = student_name
        self.course_name = course_name
        self.teacher_name = teacher_name
        self.certificate_id = certificate_id
        self.certificate_number = certificate_number
        self.certificate_issue_date = certificate_issue_date
