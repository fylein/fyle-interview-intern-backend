def get_student_assignments_resources():
    from core.apis.student import student_assignments_resources
    return student_assignments_resources

def get_teacher_assignments_resources():
    from core.apis.teachers import teacher_assignments_resources
    return teacher_assignments_resources

def get_principal_resources():
    from core.apis.principal import principal_resources
    return principal_resources

__all__ = [
    'get_student_assignments_resources',
    'get_teacher_assignments_resources',
    'get_principal_resources'
]
