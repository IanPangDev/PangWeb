import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "portfolio_page.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False