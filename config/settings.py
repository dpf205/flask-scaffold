import secrets
from datetime import timedelta
from decouple import config

PRODUCTION = False

DEVELOPMENT = True

DEBUG = True
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

# Server setup
SERVER_NAME = "localhost:8000"
FLASK_RUN_PORT = 8000

# Flask-Security -- Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt.
SECURITY_PASSWORD_HASH = 'bcrypt'
SECRET_KEY = str(secrets.SystemRandom().getrandbits(128))
SECURITY_PASSWORD_SALT = str(secrets.SystemRandom().getrandbits(128))
SECURITY_PASSWORD_SINGLE_HASH = True
SECURITY_JOIN_USER_ROLES = True
REMEMBER_COOKIE_DURATION = timedelta(days=90)

# Postgresql Database.
"""
SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
Example db_uri format:  dialect+driver <postgresql>://<postgresql username>:<postgresql password>@<hostname>:<postgres db port>/<database_name>
E.g. postgresql://postgres:password@postgres:5432/database_name
Note: the preceding examples refer to the username / password that are set during the initial Postgresql installation and setup. 
"""

# <hostname> is set to "postgres" instead of "localhost" to run the Postgres db in the same Docker container as the rest of the application,
# E.g. 'volumes: postgres', as shown in the /docker-compose.yml file.

db_dialect_driver = config('DB_DIALECT_DRIVER')
postgres_user = config('POSTGRES_USER')
postgres_password = config('POSTGRES_PASSWORD')
postgres_docker_hostname = config('POSTGRES_DOCKER_HOSTNAME')
database_port = config('DATABASE_PORT')

prod_database_name = config('PROD_DATABASE_NAME')
test_database_name = config('TEST_DATABASE_NAME')
dev_database_name = config('DEV_DATABASE_NAME')


dev_db_uri = f'{db_dialect_driver}://{postgres_user}:{postgres_password}@{postgres_docker_hostname}:{database_port}/{dev_database_name}'
prod_db_uri = f'{db_dialect_driver}://{postgres_user}:{postgres_password}@{postgres_docker_hostname}:{database_port}/{prod_database_name}'
test_db_uri = f'{db_dialect_driver}://{postgres_user}:{postgres_password}@{postgres_docker_hostname}:{database_port}/{test_database_name}'

db_uri = dev_db_uri

SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Seed development, test, or production db with admin/regular user(s) and their associated roles.
"""
As shown in https://flask-security-too.readthedocs.io/en/stable/api.html?highlight=has_role()#flask_security.
The has_role() method, from the User Object Helpers class flask_security.UserMixin, iterates through self.roles. 
The roles attribute, in the User model, is a list of Role objects.
Define User and Role models such that the User model has a many-to-many relationship to the Role model set in the User.roles attribute.
"""

seed_user_dict = {
    "admin_email": "admin@example.com",
    "admin_password": "adminpassword",
    "admin_role": "admin",  # this is created as a list of role object(s): an admin user will possess both admin and user roles.
    "admin_role_description": "This account has an 'admin' role. Therefore, it has full access to all application features enabled for the organisation -- by default. Admins can create/delete 'user' accounts and grant/revoke their associated permissions. The admin roles is empowered to access everything 'user' roles can access, as they posses a 'user' role as well.",

    "user_email": "user@example.com",
    "user_password": "userpassword",
    "user_role": "user",  # this is created as a list of role object(s) [{user}]
    "user_role_description": "This account has a generic 'user' role. Typically, this role allows limited access to the application's features, as determined by the 'admin' role. At the discretion of the admin(s), permissions will vary for accounts which possess only the 'user' role."

}

# Flask-Mail.
MAIL_DEFAULT_SENDER = 'contact@local.host'  # default
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'fake34088@gmail.com'
MAIL_PASSWORD = 'fakeuser123@'

# Flask-Babel.
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish'
}

BABEL_DEFAULT_LOCALE = 'en'
