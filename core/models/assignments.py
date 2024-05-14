import enum
from core import db
from core.apis.decorators import AuthPrincipal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum


class GradeEnum(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class AssignmentStateEnum(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    GRADED = "GRADED"


class Assignment(db.Model):
    __tablename__ = "assignments"
    id = db.Column(db.Integer, db.Sequence("assignments_id_seq"), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=True)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(
        BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False
    )
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        default=helpers.get_utc_now,
        nullable=False,
        onupdate=helpers.get_utc_now,
    )

    def __repr__(self):
        return "<Assignment %r>" % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def upsert(cls, assignment_new: "Assignment"):
        if assignment_new.id is not None:
            assignment = Assignment.get_by_id(assignment_new.id)
            assertions.assert_found(assignment, "No assignment with this id was found")
            assertions.assert_valid(
                assignment.state == AssignmentStateEnum.DRAFT,
                "only assignment in draft state can be edited",
            )

            assignment.content = assignment_new.content
        else:
            assertions.assert_valid(
                assignment_new.content is not None,
                "assignment with empty content cannot be submitted",
            )

            assignment = assignment_new
            db.session.add(assignment_new)

        db.session.flush()
        return assignment

    @classmethod
    def submit(cls, _id, teacher_id, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, "No assignment with this id was found")
        assertions.assert_valid(
            assignment.student_id == auth_principal.student_id,
            "This assignment belongs to some other student",
        )
        assertions.assert_valid(
            assignment.content is not None,
            "assignment with empty content cannot be submitted",
        )

        #
        assertions.assert_valid(
            assignment.state != AssignmentStateEnum.SUBMITTED,
            "only a draft assignment can be submitted",
        )

        assignment.teacher_id = teacher_id
        assignment.state = AssignmentStateEnum.SUBMITTED
        db.session.flush()

        return assignment

    @classmethod
    def mark_grade(cls, _id, grade, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, "No assignment with this id was found")
        assertions.assert_valid(
            grade is not None, "assignment with empty grade cannot be graded"
        )
        assertions.assert_valid(
            auth_principal.teacher_id == assignment.teacher_id,
            "assignment with empty grade cannot be graded",
        )

        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED
        db.session.flush()

        return assignment

    @classmethod
    def get_assignments_by_student(cls, student_id):
        return cls.filter(cls.student_id == student_id).all()

    @classmethod
    def get_assignments_by_teacher(cls, teacher_id):
        return cls.filter(cls.teacher_id == teacher_id).all()

    @classmethod
    def get_submitted_and_graded_assignments_for_principal(cls, user_id, principal_id):
        # Query assignments filtered by student ID and state (submitted or graded)
        assignments = cls.filter(
            cls.student_id == principal_id,
            (
                (cls.state == AssignmentStateEnum.SUBMITTED)
                | (cls.state == AssignmentStateEnum.GRADED)
            ),
        ).all()
        return assignments

    @classmethod
    def get_all_teachers(cls):
        # Query all teachers
        teachers = Teacher.query.all()
        return teachers

    @classmethod
    def grade_assignment(cls, assignment_id, grade, user_id, principal_id):
        # Retrieve the assignment by ID
        assignment = cls.get_by_id(assignment_id)
        print("assignment:", assignment.state)
        print("assignment:", assignment.content)
        assertions.assert_found(assignment, "No assignment with this id was found")

        # # Check if the assignment belongs to the principal
        # assertions.assert_valid(
        #     assignment.teacher_id == principal_id,
        #     "This assignment does not belong to the principal",
        # )

        assertions.assert_valid(
            assignment.state != AssignmentStateEnum.DRAFT,
            "Cannot grade an assignment that is not in the 'Draft' state",
        )

        # Update the grade and state of the assignment
        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED

        # Flush changes to the database
        db.session.flush()
        db.session.commit()

        return assignment