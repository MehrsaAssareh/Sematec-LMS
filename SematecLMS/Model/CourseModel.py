class Course_Model_Class:
    def __init__(self,
                 course_id: int = None,
                 course_code: int = None,
                 course_name: str = None,
                 duration: int = None,
                 syllabus: str = None,
                 cost: int = None,
                 status: str = None,
                 course_category_id: int = None,
                 prerequisite_course_id: int = None):
        self.course_id = course_id
        self.course_code = course_code
        self.course_name = course_name
        self.duration = duration
        self.syllabus = syllabus
        self.cost = cost
        self.status = status
        self.course_category_id = course_category_id
        self.prerequisite_course_id = prerequisite_course_id
