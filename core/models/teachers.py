from sqlalchemy.orm import joinedload
from core import db
from core.libs import helpers
from .users import User

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, db.Sequence('teachers_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False,
                           onupdate=helpers.get_utc_now)

    user = db.relationship('User', backref='teachers', lazy=True)

    def __repr__(self):
        return '<Teacher %r>' % self.id

    @classmethod
    def get_all_teacher(cls):
        # Eager load the 'user' relationship
        return cls.query.options(joinedload(cls.user)).all()
