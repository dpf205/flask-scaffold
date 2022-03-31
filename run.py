# from config.settings import SQLALCHEMY_DATABASE_URI
# from server_app.app import create_app
# from sqlalchemy_utils import database_exists, create_database
#
#
# def validate_db():
#     if database_exists(SQLALCHEMY_DATABASE_URI):
#         current_database = SQLALCHEMY_DATABASE_URI.split("/")[-1]
#         print(f" \n\n {current_database} already exists. \n")
#     else:
#         create_database(SQLALCHEMY_DATABASE_URI)
#         current_database = SQLALCHEMY_DATABASE_URI.split("/")[-1]
#         print(f"\n\n Creating {current_database}....")
#         print(f" {current_database} was created successfully. \n ")
#
#
# app = create_app()
#
# if __name__ == "__main__":
#     app.run(host='localhost', port=8000, debug=True)
