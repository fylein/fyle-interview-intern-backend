from core import db
from core.libs import helpers


class Teacher(db.Model):
    __tablename__ = 'teachers'
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    id = db.Column(db.Integer, db.Sequence('teachers_id_seq'), primary_key=True)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return '<Teacher %r>' % self.id
    
    @classmethod
    def get_list_of_teachers(cls):
        teachers = cls.query.all()
        return teachers

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()
    
    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)