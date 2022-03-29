import datetime
from sqlalchemy_utils import database_exists, create_database, drop_database

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from server_app.extensions import Base

from config.settings import seed_user_dict
from flask_security import hash_password, SQLAlchemySessionUserDatastore

from config.settings import SQLALCHEMY_DATABASE_URI
from server_app.blueprints.users.models import User, Role

engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.query = db_session.query_property()
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)


def init_db():
    """
    Import all modules here that might define models so that they will be registered properly on the metadata.
    Otherwise, you will have to import them first before calling init_db() import models.

    Below, metadata.create_all(bind=engine) takes a checkfirst keyword argument which determines
    whether SQLAlchemy should check whether a table already exists before trying to create it.
    The default value of this argument is True, so once the tables have been created future
    invocations will have no effect.
    """

    import server_app.blueprints.users.models

    Base.metadata.create_all(bind=engine)


def validate_db():
    if database_exists(SQLALCHEMY_DATABASE_URI):
        current_database = SQLALCHEMY_DATABASE_URI.split("/")[-1]
        print(f" \n\n {current_database} already exists. \n\n\n")

    else:
        create_database(SQLALCHEMY_DATABASE_URI)
        current_database = SQLALCHEMY_DATABASE_URI.split("/")[-1]
        print(f"\n\n Creating {current_database}....")
        print(f"\n\n {current_database} was created successfully!  \n\n\n ")


def drop_delete_db():
    if database_exists(SQLALCHEMY_DATABASE_URI):
        drop_database(SQLALCHEMY_DATABASE_URI)
        current_database = SQLALCHEMY_DATABASE_URI.split("/")[-1]
        print(f"\n\n\n dropped/deleted {current_database} successfully! \n\n\n")
    else:
        current_database = SQLALCHEMY_DATABASE_URI.split("/")[-1]
        print(f"\n\n\n {current_database} does not exit! \n\n\n")
