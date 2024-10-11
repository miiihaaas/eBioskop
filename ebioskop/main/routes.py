from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_mail import Message, Mail


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    route_name = request.endpoint
    return render_template('home.html', route_name=route_name)


@main.route('/faq', methods=['GET', 'POST'])
def faq():
    route_name = request.endpoint
    return render_template('faq.html', route_name=route_name)