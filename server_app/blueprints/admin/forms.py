from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField  # use for file upload https://flask-wtf.readthedocs.io/en/latest/form/#module-flask_wtf.file


# TODO: validators=[Length(min=4, max=50)   HiddenField ?

class RegistrationForm(FlaskForm):
    # username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_new_password = PasswordField("Confirm New Password", validators=[DataRequired()])
    submit = SubmitField("Change Password")


class ActivateUserForm(FlaskForm):
    activate_user_id_field = HiddenField(default='', validators=[DataRequired()])
    activate_user_submit = SubmitField("Activate account")


class DeactivateUserForm(FlaskForm):
    deactivate_user_id_field = HiddenField(default='', validators=[DataRequired()])
    deactivate_user_submit = SubmitField("Deactivate account")


class DeleteUserForm(FlaskForm):
    delete_user_id_field = HiddenField(default='', validators=[DataRequired()])
    delete_user_submit = SubmitField("Delete user")


# N.B. Intentionally duplicated from User RegistrationForm. May will need admin-specific functionality.
class CreateUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create New User")

# class BeginPasswordResetForm(Form):
#     identity = StringField("Username or email",
#                            [DataRequired(),
#                             Length(3, 254),
#                             ensure_identity_exists])


# class PasswordResetForm(FlaskForm):
#     reset_token = HiddenField()
#     password = PasswordField("Password", [DataRequired(), Length(8, 128)])


# class UpdateCredentials(FlaskForm):
#     current_password = PasswordField("Current password",
#                                      [DataRequired(),
#                                       Length(8, 128),
#                                       ensure_existing_password_matches])
#
#     email = EmailField(validators=[
#         Email(),
#         Unique(
#             User.email,
#             get_session=lambda: db.session
#         )
#     ])
#     password = PasswordField("Password", [Optional(), Length(8, 128)])
