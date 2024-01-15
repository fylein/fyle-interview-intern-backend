from core import db
from core.libs import helpers
from core.libs import assertions
from core.models.principals import Principal

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, db.Sequence('teachers_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Teacher %r>' % self.id
    
    @classmethod
    def get_by_candidate_id(cls, _id, user_id):
        return cls.query.filter_by(id=_id, user_id=user_id).first()
    
    @classmethod
    def get_all_teachers(cls, principal_id, user_id):
        principal = Principal.get_by_candidate_id(principal_id, user_id)
        assertions.assert_auth(principal is not None, 'Requester\'s user id and principal id combination does not belong to a principal')
        return cls.query.all()
