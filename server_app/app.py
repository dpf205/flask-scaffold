import time
import datetime

from flask import Flask
import flask_wtf
from server_app.extensions import Babel, mail
from server_app.blueprints.users.models import User, Role
from server_app.blueprints.page import page
from server_app.blueprints.admin.views import admin
from server_app.blueprints.users.views import users

from config.settings import SQLALCHEMY_DATABASE_URI, seed_user_dict
from sqlalchemy_utils import database_exists, create_database, drop_database

from server_app.database import db_session, init_db, drop_delete_db
from flask_security import SQLAlchemySessionUserDatastore, hash_password, Security


# TODO: create run.py in root directory
def create_app():
    """
    Create a Flask application using the app factory pattern.
    :return: Flask app
    """

    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.settings')
    app.config.from_pyfile("settings.py", silent=True)

    # TODO: remove drop_delete_db()
    # drop_delete_db()

    @app.before_first_request
    def validate_db():
        if database_exists(SQLALCHEMY_DATABASE_URI):
            current_database = SQLALCHEMY_DATABASE_URI.split("/")[-1]
            print(f" \n\n {current_database} already exists. \n")
        else:
            create_database(SQLALCHEMY_DATABASE_URI)
            current_database = SQLALCHEMY_DATABASE_URI.split("/")[-1]
            print(f"\n\n Creating {current_database}....")
            print(f" {current_database} was created successfully. \n ")

    # Setup Flask-Security. Create_users_if_none() calls init_db() from database.py
    user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
    security = Security(app, user_datastore)

    # Seed the User table with admin and generic user accounts if none exist.
    @app.before_first_request
    def create_users_if_none():
        init_db()

        admin_seed_user = user_datastore.find_user(email=seed_user_dict.get("admin_email"))
        generic_seed_user = user_datastore.find_user(email=seed_user_dict.get("user_email"))

        # Verify the seed admin user does not exist in the User table.
        if not admin_seed_user:
            print(f"\n\n\n Creating seed admin user....")

            # Create the seed 'admin' account
            admin_account = user_datastore.create_user(email=seed_user_dict.get("admin_email"),
                                                       password=hash_password(seed_user_dict.get("admin_password")),
                                                       confirmed_at=datetime.datetime.now())
            # Create the "admin" role.
            admin_role = user_datastore.create_role(name=seed_user_dict.get("admin_role"),
                                                    description=seed_user_dict.get("admin_role_description"))
            # Create a "user" role for the admin account, as an admin user will possess both "admin" and "user" roles.
            user_role_for_admin = user_datastore.create_role(name=seed_user_dict.get("user_role"),
                                                             description=seed_user_dict.get("user_role_description"))

            # Add both the "admin" and "user" roles to the admin account
            user_datastore.add_role_to_user(admin_account, admin_role)
            time.sleep(2)
            user_datastore.add_role_to_user(admin_account, user_role_for_admin)

            db_session.commit()

            time.sleep(2)
            print(f"Seed admin user {seed_user_dict.get('admin_email')} was created.\n")
        else:
            print(f"\n\n\n Seed admin user {admin_seed_user.email} exists.\n\n\n")

        # Verify the generic user does not exist in the User table.
        if not generic_seed_user:
            print(f"\n\n\n Creating generic seed user....")

            # Create the seed 'user' account
            user_account = user_datastore.create_user(email=seed_user_dict.get("user_email"),
                                                      password=hash_password(seed_user_dict.get("user_password")),
                                                      confirmed_at=datetime.datetime.now())

            # Create the seed user role.
            user_role = user_datastore.create_role(name=seed_user_dict.get("user_role"),
                                                   description=seed_user_dict.get("user_role_description"))
            time.sleep(3)
            # Add the 'user' role to the user account.
            user_datastore.add_role_to_user(user_account, user_role)

            db_session.commit()

            time.sleep(2)
            print(f'Seed user {seed_user_dict.get("user_email")} was created.\n\n')
        else:
            print(f'\n Seed user {generic_seed_user.email} exists.\n\n')

    # Register Blueprints
    app.register_blueprint(page)
    app.register_blueprint(admin)
    app.register_blueprint(users)

    # Register / initialize extensions
    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    Babel(app)
    mail.init_app(app)
    flask_wtf.CSRFProtect(app)

    # login_manager.init_app(app)

    return None
