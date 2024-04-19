# GET /principal/teachers
# POST /principal/assignments/grade

""" 
workflow:
> we 're going to create a Blueprint so that all the views associated to the principal is grouped and managed from here.
> then we 're going to register the required views for /assignments, /teachers, /assignments/grade
"""
from flask import Blueprint
from core.apis import decorators

# created a blueprint to manage all the resources from principal.py only.
principal_resources = Blueprint('teacher_assignments_resources', __name__)


# GET /principal/assignments
@principal_resources.get("/assignments", strict_slashes=False)
def list_assignments():
    ...