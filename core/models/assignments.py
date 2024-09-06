import enum
from core import db
from core.apis.decorators import AuthPrincipal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum
from core.libs.exceptions import FyleError
from core.models.principals import Principal
from sqlalchemy import or_

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
    # bug fix
    content = db.Column(db.Text,nullable=False)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

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
            assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be posted')
            assignment.content = assignment_new.content
        else:
            assignment = assignment_new
            assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be posted')
            db.session.add(assignment_new)

        db.session.flush()
        return assignment

    @classmethod
    def submit(cls, _id, teacher_id, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(assignment.student_id == auth_principal.student_id, 'This assignment belongs to some other student')
        assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be submitted')
        # bug fix
        if assignment.state == AssignmentStateEnum.SUBMITTED:
            assertions.assert_valid(False, 'only a draft assignment can be submitted')
        else:
            assignment.teacher_id = teacher_id
            assignment.state=AssignmentStateEnum.SUBMITTED
            db.session.flush()
            return assignment


    @classmethod
    def mark_grade(cls, _id, grade, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(grade is not None and grade in GradeEnum, 'assignment with empty grade cannot be graded')
        assertions.assert_valid(assignment.state != AssignmentStateEnum.DRAFT, 'Cannot grade an assignment in DRAFT state')
        if not auth_principal.principal_id:
            #bug:  id mismatch
            assertions.assert_valid(assignment.teacher_id == auth_principal.teacher_id,'Assignment belongs to another teacher')
            assertions.assert_valid(assignment.state != AssignmentStateEnum.GRADED, 'Assignment is already graded')
        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED
        db.session.flush()

        return assignment

    @classmethod
    def get_assignments_by_student(cls, student_id):
        return cls.filter(cls.student_id == student_id).all()

    # bug Fix: Retrieve list of assignments on the basis of teacher ID
    @classmethod
    def get_assignments_by_teacher(cls, teacher_id):
        return cls.query.filter(cls.teacher_id == teacher_id).all()

    @classmethod
    def list_all_graded_submitted_assignments(cls):
        return cls.query.filter(
            or_(cls.state == AssignmentStateEnum.SUBMITTED, cls.state == AssignmentStateEnum.GRADED)).all()