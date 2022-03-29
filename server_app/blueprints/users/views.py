import datetime
import time
from flask import Blueprint, redirect, url_for, render_template, flash, render_template_string, request, get_flashed_messages

from flask_security import admin_change_password, verify_password, login_user, logout_user, Security, current_user, roles_required, login_required, anonymous_user_required, hash_password, \
    SQLAlchemySessionUserDatastore
from server_app.database import db_session

from config.settings import seed_user_dict

from server_app.blueprints.users.models import User, Role
from server_app.blueprints.users.forms import LoginForm, RegistrationForm, ChangePasswordForm, ActivateUserForm, DeactivateUserForm, DeleteUserForm, CreateUserForm

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)

users = Blueprint("users", __name__, template_folder="templates", url_prefix="/users")


@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    form_email = form.email.data
    form_password = form.password.data
    form_confirm_password = form.confirm_password.data

    if form.validate_on_submit() and request.method == "POST" and form_password == form_confirm_password:

        # Create new user if user email does not exist.
        if not user_datastore.find_user(email=form_email):

            # Add the 'user' role to the new user's account
            new_user_account = user_datastore.create_user(email=form_email,
                                                          password=hash_password(form_password),
                                                          confirmed_at=datetime.datetime.now())

            # A generic "user" account is created by default, as opposed to "admin".
            user_role = user_datastore.create_role(name=seed_user_dict["user_role"],
                                                   description=seed_user_dict["user_role_description"])  # seed_user_dict{} from config/settings.py
            user_datastore.add_role_to_user(new_user_account, user_role)

            db_session.commit()
            time.sleep(2)
            return redirect(url_for("users.login"))
        else:
            return redirect(url_for("users.register"))
    elif request.method == "POST" and form_password != form_confirm_password:
        print("\n\n The passwords do not match. Try again.\n\n")  # TODO: explore Flask-Toastr 0.5.6  as alternative to Flask's flash() for user feedback
        return redirect(url_for("users.register"))
    return render_template("user/register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    # TODO: evaluate Flask-Toastr 0.5.6  as alternative to Flask's flash() for user feedback
    form = LoginForm()
    messages = get_flashed_messages()
    if form.validate_on_submit() and request.method == "POST":
        form_email = form.email.data
        form_password = form.password.data
        existing_user = user_datastore.find_user(email=form_email)

        try:
            # flask_security.verify_password(password, password_hash) returns boolean
            if not existing_user and not verify_password(form_password, existing_user.password):
                print("Incorrect credentials ty again")
                return redirect(url_for("users.login"))

        except Exception as e:
            print(e)
        else:
            login_user(existing_user)
            print("Success! User verified. This user can login!", end="\n\n")
            return redirect(url_for("users.account"))

    return render_template("user/login.html", form=form)


@users.route("/logout")
def logout():
    if request.method == "GET":
        logout_user()
    # TODO: consider redirecting the logged out user to a "You have been logged out!" page.
    return redirect(url_for("page.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    logged_in_user = user_datastore.find_user(email=current_user.email)
    roles = logged_in_user.roles
    current_user_role_list = []
    [current_user_role_list.append(role.name) for role in roles]

    user_is_admin = logged_in_user.has_role("admin")  # returns boolean

    return render_template("user/account.html",
                           user_is_admin=user_is_admin,
                           current_user=current_user,
                           current_user_role_list=current_user_role_list,
                           current_user_is_authenticated=current_user.is_authenticated)


@users.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    # Get current user's identity
    logged_in_user = user_datastore.find_user(email=current_user.email)  # user_object
    hashed_current_password = logged_in_user.password

    user_is_admin = logged_in_user.has_role("admin")  # returns boolean
    if user_is_admin:
        print(f"\n\n\n is user admin? True/False: {user_is_admin} \n\n")

    # Access role(s) for the current user.
    roles = logged_in_user.roles
    current_user_role_list = []
    [current_user_role_list.append(role.name) for role in roles]

    # Password change / update: admin_change_password(user_object, new_password, notify=True/False)
    # N.B. This immediately renders user’s existing sessions(and possibly authentication tokens) invalid
    form = ChangePasswordForm()
    form_current_password = form.current_password.data
    new_password = form.new_password.data
    confirm_new_password = form.confirm_new_password.data

    if form.validate_on_submit() and request.method == "POST":
        if new_password != confirm_new_password:
            return redirect(url_for("users.change_password"))
        elif verify_password(form_current_password, hashed_current_password):  # .verify_password() returns boolean
            print("Current password entered incorrectly. Re-try.")
        else:
            # N.B.  Note that this will immediately render the user’s existing sessions(and possibly authentication tokens) invalid.
            admin_change_password(logged_in_user, new_password, notify=False)
            return redirect(url_for("users.login"))
    return render_template("user/change-password.html",
                           form=form,
                           current_user=current_user,
                           current_user_email=current_user.email,
                           current_user_is_authenticated=current_user.is_authenticated)


