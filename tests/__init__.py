from core.server import create_app

def configure_app_for_testing():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///./test.sqlite3'
    })
    return app
