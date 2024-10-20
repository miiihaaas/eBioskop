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


@main.route('/box_office', methods=['GET', 'POST'])
def box_office():
    route_name = request.endpoint
    totals = []
    return render_template('box_office.html', 
                            route_name=route_name,
                            totals=totals)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    route_name = request.endpoint
    return render_template('contact.html', route_name=route_name)