import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from core import create_app, db
from core.models.assignments import Assignment
from sqlalchemy import update


app = create_app()

with app.app_context():
    db.session.execute(
        update(Assignment)
        .where(Assignment.id == 4, Assignment.state == 'GRADED')  # Ensure it is in GRADED state
        .values(state='DRAFT')  
    )
    db.session.commit()  
    print("Assignment state changed to DRAFT for assignment ID 4.")
