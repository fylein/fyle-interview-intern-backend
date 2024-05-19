import enum
from core import db
from core.apis.decorators import AuthPrincipal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum


class GradeEnum(str, enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class AssignmentStateEnum(str, enum.Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    GRADED = 'GRADED'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=True)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False,
                           onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Assignment %r>' % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def upsert(cls, assignment_new: 'Assignment'):
        if assignment_new.id is not None:
            assignment = Assignment.get_by_id(assignment_new.id)
            assertions.assert_found(assignment, 'No assignment with this id was found')
            assertions.assert_valid(assignment.state == AssignmentStateEnum.DRAFT,
                                    'only assignment in draft state can be edited')

            assignment.content = assignment_new.content
        else:
            assignment = assignment_new
            assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be submitted')
            db.session.add(assignment_new)

        db.session.flush()
        return assignment

    @classmethod
    def submit(cls, _id, teacher_id, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(assignment.student_id == auth_principal.student_id,
                                'This assignment belongs to some other student')
        assertions.assert_valid(assignment.state is not AssignmentStateEnum.SUBMITTED,
                                'only a draft assignment can be submitted')
        assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be submitted')

        assignment.teacher_id = teacher_id
        assignment.state = AssignmentStateEnum.SUBMITTED
        db.session.flush()

        return assignment

    @classmethod
    def mark_grade(cls, _id, grade, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        # assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(grade is not None, 'assignment with empty grade cannot be graded')
        # assertions.assert_valid(assignment.state != AssignmentStateEnum.DRAFT, 'draft assignment cannot be graded')
        # assertions.assert_valid(
        #     (auth_principal.teacher_id is not None and assignment.state != AssignmentStateEnum.GRADED) or auth_principal.principal_id is not None,
        #     'Only teachers and principal can grade the assignments and already graded assignments cannot be graded '
        #     'again by teachers')

        # if auth_principal.teacher_id is not None:
        #     assertions.assert_valid(assignment.state != AssignmentStateEnum.GRADED,
        #                             'already graded assignments cannot be graded again by teachers')
        #     assertions.assert_valid(assignment.teacher_id == auth_principal.teacher_id,
        #                             'assignment has been submitted to another teacher')
        #
        # else:
        #     assertions.assert_valid(auth_principal.principal_id is not None,
        #                             'Only the teacher and principle can grade the assignments')
        #     assignment.grade = grade
        #     assignment.state = AssignmentStateEnum.GRADED

        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED
        db.session.flush()

        return assignment

    @classmethod
    def get_assignments_by_student(cls, student_id):
        return cls.filter(cls.student_id == student_id).all()

    @classmethod
    def get_assignments_by_teacher(cls, teacher_id):
        return cls.filter(cls.teacher_id == teacher_id, cls.state != AssignmentStateEnum.DRAFT).all()

    @classmethod
    def get_all_submitted_or_graded_assignments(cls):
        return cls.filter(cls.state == AssignmentStateEnum.SUBMITTED or cls.state == AssignmentStateEnum.GRADED).all()
