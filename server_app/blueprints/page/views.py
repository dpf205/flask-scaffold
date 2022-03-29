from flask import Blueprint, render_template
from flask_security import current_user

page = Blueprint("page", __name__, template_folder="templates")


@page.route('/')
def home():
    if current_user.is_authenticated:
        return render_template("page/home.html",
                               current_user=current_user,
                               current_user_is_authenticated=current_user.is_authenticated)
    else:
        return render_template("page/home.html")


@page.route("/terms")
def terms():
    if current_user.is_authenticated:
        return render_template("page/terms.html",
                               current_user=current_user,
                               current_user_is_authenticated=current_user.is_authenticated)
    else:
        return render_template("page/terms.html")


@page.route("/privacy")
def privacy():
    if current_user.is_authenticated:
        return render_template("page/privacy.html",
                               current_user=current_user,
                               current_user_is_authenticated=current_user.is_authenticated)
    else:
        return render_template("page/privacy.html")
