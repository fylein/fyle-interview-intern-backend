from .principal import principal_assignments_resources

def register_routes(app):
    app.register_blueprint(student_assignments_resources)
    app.register_blueprint(teacher_assignments_resources)
    app.register_blueprint(principal_assignments_resources)  # Register new routes here
