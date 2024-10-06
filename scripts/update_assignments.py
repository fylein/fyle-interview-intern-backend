from core import create_app, db
from core.models.assignments import Assignment
from sqlalchemy import update

app = create_app()
with app.app_context():
    db.session.execute(update(Assignment).where(Assignment.state == 'graded').values(state='GRADED'))
    db.session.commit()
