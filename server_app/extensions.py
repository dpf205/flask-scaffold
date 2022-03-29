# extensions.py averts some circular import issues.

from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


from flask_babelex import Babel
from flask_mail import Mail


mail = Mail()
db = SQLAlchemy()
babel = Babel()

login_manager = LoginManager()

Base = declarative_base()




