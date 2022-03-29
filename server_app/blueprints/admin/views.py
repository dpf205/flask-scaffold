import time
import datetime
from flask import current_app, Blueprint, render_template, redirect, request, url_for
from flask_security import admin_change_password, verify_password, current_user, roles_required, login_required, hash_password, SQLAlchemySessionUserDatastore
from server_app.database import db_session
from server_app.blueprints.admin.forms import ChangePasswordForm, ActivateUserForm, DeactivateUserForm, DeleteUserForm, CreateUserForm
from config.settings import seed_user_dict
from server_app.blueprints.users.models import User, Role

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)

admin = Blueprint("admin", __name__, template_folder="templates", url_prefix="/admin")


@admin.route("/admin-panel", methods=["GET", "POST"])
@login_required
@roles_required('admin')
def admin_panel():
    # Generate activate / deactivate / create / delete user forms.
    activate_user_form = ActivateUserForm()
    deactivate_user_form = DeactivateUserForm()
    delete_user_form = DeleteUserForm()
    create_user_form = CreateUserForm()

    # TODO: convert code for retrieving users and user's roles to a function and put in database.py

    # Retrieve all users
    all_users_list = User.query.all()  # Returns a list of all users
    return render_template("admin/admin-panel.html",
                           current_user=current_user,
                           activate_user_form=activate_user_form,
                           deactivate_user_form=deactivate_user_form,
                           create_user_form=create_user_form,
                           delete_user_form=delete_user_form,
                           all_users_list=all_users_list,
                           current_admin_user=current_user.email,
                           current_user_is_authenticated=current_user.is_authenticated)


@admin.route("/view-user-account/<int:user_id>/<user_email>", methods=["GET", "POST"])
@login_required
@roles_required('admin')
def view_user_account(user_id=None, user_email=None):
    if user_id is not None and user_email is not None:
        pass
        # This route should link directly from the admin.admin_panel
        # Retrieve and display an individual user account
        # Should probably perform password resets here.

    return render_template("admin/view-user-account.html")


@admin.route("/change-password", methods=["GET", "POST"])
@login_required
@roles_required('admin')
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
            return redirect(url_for("admin.change_password"))
        elif verify_password(form_current_password, hashed_current_password):  # .verify_password() returns boolean
            print("Current password entered incorrectly. Re-try.")
        else:
            # N.B.  Note that this will immediately render the user’s existing sessions(and possibly authentication tokens) invalid.
            admin_change_password(logged_in_user, new_password, notify=False)
            return redirect(url_for("users.login"))
    return render_template("admin/change-password.html",
                           form=form,
                           current_user=current_user,
                           current_user_email=current_user.email,
                           current_user_is_authenticated=current_user.is_authenticated)


@admin.route("/activate-user", methods=["POST"])
@login_required
@roles_required('admin')
def activate_user():
    activate_user_form = ActivateUserForm()
    if request.method == "POST" and activate_user_form.validate_on_submit():
        try:
            user_id = int(activate_user_form.activate_user_id_field.data)
            print(f"activate_user_id_field.data {user_id}", end="\n\n")

            # Use the user.id (or email, as username) to lookup the required user object
            selected_user = user_datastore.find_user(id=user_id)
            user_datastore.activate_user(selected_user)
        except Exception as e:
            print(f"Exception: {e}", end="\n\n\n")
    else:
        print("User (re)activation failed. See exception", end="\n\n\n")
    return redirect(url_for("admin/admin_panel"))


@admin.route("/deactivate-user", methods=["POST"])
@login_required
@roles_required('admin')
def deactivate_user():
    deactivate_user_form = DeactivateUserForm()
    if request.method == "POST" and deactivate_user_form.validate_on_submit():
        try:
            user_id = int(deactivate_user_form.deactivate_user_id_field.data)
            print(f"deactivate_user_id_field.data: {user_id} \n\n")

            # Use the user.id (or email, as username) to get the user object.
            selected_user = user_datastore.find_user(id=user_id)
            user_datastore.deactivate_user(selected_user)
        except Exception as e:
            print(f"Exception: {e}", end="\n\n\n")
    else:
        print("User (re)activation failed. ", end="\n\n\n")
    return redirect(url_for("admin.admin_panel"))


@admin.route("/delete-user", methods=["POST"])
@login_required
@roles_required('admin')
def delete_user():
    delete_user_form = DeleteUserForm()
    if request.method == "POST" and delete_user_form.validate_on_submit():
        try:
            user_id = int(delete_user_form.delete_user_id_field.data)

            # Use the user.id url parameter to lookup the required user object
            selected_user = user_datastore.find_user(id=user_id)
            user_datastore.delete_user(selected_user)
            print(f"delete_user_id_field: {user_id}", end="\n\n")
        except Exception as e:
            print(f"Exception: {e}", end="\n\n\n")
    else:
        print("User deletion failed. ", end="\n\n\n")
        return redirect(url_for("admin.admin_panel"))
    return redirect(url_for("admin.admin_panel"))


@admin.route("/create-user", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def create_user():
    form = CreateUserForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            form_email = form.email.data
            form_password = form.password.data
            form_confirm_password = form.confirm_password.data
            if form_password == form_confirm_password:

                # Create new user if user email does not exist.
                if not user_datastore.find_user(email=form_email):

                    # Add the 'user' role to the new user's account
                    new_user_account = user_datastore.create_user(email=form_email,
                                                                  password=hash_password(form_password),
                                                                  confirmed_at=datetime.datetime.now())

                    # A generic "user" account is created by default, as opposed to "admin".
                    user_role = user_datastore.create_role(name=seed_user_dict.get("user_role"),
                                                           description=seed_user_dict.get("user_role_description"))  # seed_user_dict{} from config/settings.py
                    user_datastore.add_role_to_user(new_user_account, user_role)

                    db_session.commit()
                    time.sleep(2)
                    return redirect(url_for("admin.create_user"))
                else:
                    return redirect(url_for("admin.create_user"))
            elif request.method == "POST" and form_password != form_confirm_password:
                print("\n\n The passwords do not match. Try again.\n\n")  # TODO: explore Flask-Toastr 0.5.6  as alternative to Flask's flash() for user feedback
                return redirect(url_for("admin.create_user"))
            return render_template("admin/create-user.html", form=form)
        except Exception as e:
            print(f"Exception: {e}", end="\n\n\n")

    else:
        redirect(url_for("users.create_user"))
    return render_template("admin/create-user.html",
                           current_user_is_authenticated=current_user.is_authenticated)


@admin.route("/test-route/<int:value1>/<value2>", methods=["GET"])
@login_required
@roles_required('admin')
def send_url_params_via_anchor_tag(value1, value2):
    # TODO: obfuscate url by shortening, etc
    """
    Jinja template example:

    {{user.integer_value}} and {{user.string_value}} are output to the html/template, and an anchor tag is used e.g.
     <a href="{{ url_for('users.url_params_via_anchor_tag', user_id=user.integer_value, username=user.string_value) }}"> Link Text  </a>
     within a file like ' return render_template(users.example_send-url-params-via-anchor-tag.html) '
    """
    #
    print(f"\n\n\n Output value1 {value1} (int) and value2 {value2}\n\n\n.")

    return redirect(url_for("users.send_url_params_via_anchor_tag"))

# TODO: implement the following as needed
# @anonymous_user_required
# @roles_required('admin')
# user_datastore.delete_user(user)
# user_datastore.remove_role_from_user(user, role)
# flask_security.verify_and_update_password(password, user)
# has_permission(permission) # https://flask-security-too.readthedocs.io/en/stable/api.html?highlight=verify_password#flask_security.verify_and_update_password
# has_role(role) # https://flask-security-too.readthedocs.io/en/stable/api.html?highlight=verify_password#flask_security.verify_and_update_password
# add_role_to_user(user, role) # https://flask-security-too.readthedocs.io/en/stable/api.html?highlight=verify_password#flask_security.verify_and_update_password
# user_datastore.delete_user(user) # https://flask-security-too.readthedocs.io/en/stable/api.html?highlight=verify_password#flask_security.verify_and_update_password
# user_datastore.remove_role_from_user(user, role) # https://flask-security-too.readthedocs.io/en/stable/api.html?highlight=verify_password#flask_security.verify_and_update_password
