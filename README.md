# Overview
* Backend: Flask, PostgreSQL, Docker -- frontend: Bootstrap 5 and Jinja2 templates, WTForms.
* This repository is intended as a scaffold -- a reusable starting template for a ***development*** environment. 
* The structure follows the [Application Factory Pattern](https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/). 
* Current features: user login / registration, RBAC.
* Additions / refinements will occur -- with priority given to server-side development.

# Initial setup (see example_files/)
Create a `.env` file in the root directory, and set the configuration values as illustrated:

    COMPOSE_PROJECT_NAME=<project name>
    DB_DIALECT_DRIVER=<e.g. postgresql>
    POSTGRES_USER=<postgresql username>
    POSTGRES_PASSWORD=<postgresql password>
    POSTGRES_DOCKER_SERVICE=<e.g. postgres>
    DATABASE_PORT=<.e.g. 5432>
    DATABASE_NANE=<.e.g. dev_db>
    PYTHONUNBUFFERED=true
These values are read by config/settings.py, via the [python-decouple](https://pypi.org/project/python-decouple/) package.

# Authentication and Role-based Access Control 
- This project uses the [Flask-Security-Too](https://flask-security-too.readthedocs.io/en/stable/) package.
  

# Docker
* Within root directory, initialise Docker container and build app `docker-compose up --build` 
* Clean up docker containers, remove dangling images, build and start a new docker image / container:
`docker-compose down && docker-compose rm -f && docker volume rm $(docker volume ls -q) && docker rmi -f -a $(docker images -qf dangling=true) && docker-compose up --build --remove-orphans`


# Database -- PostgreSQL w/ SQLAlchemy ORM
* In `config/settings.py`, set `db_uri` variable to the desired connection string / URL
* Example db_uri string format: " dialect+driver ("postgresql")://<database_owner_username>:<database_owner_password>@<hostname>:<port>/<database_name> "
* E.g. ` db_uri = "postgresql://postgres:1ntrep1d@postgres:5432/dev_db" `
* In `config/settings.py`, set `SQLALCHEMY_DATABASE_URI` equal to `db_uri`, as [SQLALCHEMY_DATABASE_URI](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/) is among the configuration keys 
  currently understood by SQLAlchemy
* This application runs the Postgres db in the same container as the rest of the application. Ergo, <hostname> is set to "postgres", the name of the docker-compose.yml volume.
Otherwise, <hostname>  would be set to <localhost> if not linking the db to the Docker container.
  
# Run Pytest suite in Docker container
* run all tests:
`docker-compose exec <Dockerfile service> <Dockerfile ENV INSTALL_PATH> test`

* run test coverage:
`docker-compose exec <docker-compose.yml service> <Dockerfile ENV INSTALL_PATH> cov`

# Docker commands for the database if using the Click package
* Initialize the database: `docker-compose exec <docker-compose.yml service> <Dockerfile ENV INSTALL_PATH> db init`
* Initialize and seed automatically: `docker-compose exec <docker-compose.yml service> <Dockerfile ENV INSTALL_PATH> db reset`
* Seed the database with an initial user: `docker-compose exec <docker-compose.yml service> <Dockerfile ENV INSTALL_PATH> db seed`
* Reset and seed DB using the test database: `docker-compose exec <docker-compose.yml service> <Dockerfile ENV INSTALL_PATH> db reset --with-testdb`
* Run tests within docker container:
`docker-compose exec <docker-compose.yml service> py.test --cov-report term-missing --cov <Dockerfile ENV INSTALL_PATH>`
* Run static code analysis: 
`docker-compose exec <docker-compose.yml service> flake8 . --exclude  __ init __.py`
* Output total number lines of code within project, by programming language used: `docker-compose exec <docker-compose.yml service> <Dockerfile ENV INSTALL_PATH> loc` 
However, this will include Python docstrings, the CLI  script, if present, and all tests.


# ngrok
- Creates a secure tunnel on the local machine along with a temporary public URL for demonstration, etc. 
  * Download and install from the <docker-compose.yml service>: https://ngrok.com/download. Then, in terminal, enter `./ngrok http  localhost:8000  or '127.0.0.1:8000`
  * Install with Homebrew: `homebrew cask install ngrok`. If you install via Homebrew, you don’t have to type `./ngrok` at the start of each command; you can just type `ngrok`  
  * In either case, after entering `./ngrok http  localhost:8000` or `ngrok` in terminal, copy the ngrok http <Dockerfile ENV INSTALL_PATH> name from the "Fowarding" row (omit the http://)
    and put `<Dockerfile ENV INSTALL_PATH>_NAME = "644f-74-111-99-166.ngrok.io"` in `<Dockerfile ENV INSTALL_PATH>/instance/settings.py`. If absent, Flask will throw a 404.
 

# Planned near-term enhancements (order does not indicate priority)
* Automated CI/CD: Jenkins is the likely option
* Deployment: Terraform deployment scripts -- to DigitalOcean, AWS, and / or GCP -- are forthcoming.
* Sphinx or Swagger Documentation: TBD
* Teraform visualizations: TBD
* Decoupled Vue.js frontend API. Alternatives [Tailwind](https://tailwindcss.com/) and/or [HTMx](https://htmx.org/).
* Dedicated JSON APIs
* Cosmetic frontend improvements
* Apache Airflow ETL 
* Finish writing all ***backend*** tests
* Logging, exception handling, error handling (dedicated error pages)


