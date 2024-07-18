from core import db
from core.libs import helpers
from core.libs import helpers, assertions
from core.models.teachers import Teacher


class Principal(db.Model):
    __tablename__ = 'principals'
    id = db.Column(db.Integer, db.Sequence('principals_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Principal %r>' % self.id

    @classmethod
    def get_by_id(cls, _id):
        principal= cls.query.get(_id)
        assertions.assert_auth(principal is not None,'No principal with this id was found')
        return True
