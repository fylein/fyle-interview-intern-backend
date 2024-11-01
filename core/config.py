import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./store.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

def get_sqlite_uri():
    return os.getenv('SQLALCHEMY_DATABASE_URI', Config.SQLALCHEMY_DATABASE_URI)
