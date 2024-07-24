# from core import app
# from .responses import APIResponse
# app.response_class = APIResponse

from .student import student_assignments_resources
from .teacher import teacher_assignments_resources
from .principal import principal_assignments_resources

__all__ = [
    'student_assignments_resources',
    'teacher_assignments_resources',
    'principal_assignments_resources'  
]