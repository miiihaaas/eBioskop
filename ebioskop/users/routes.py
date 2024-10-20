import os
from ebioskop import bcrypt
from flask import Blueprint, app, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from ebioskop import mail, db
from ebioskop.models import User
from ebioskop.users.forms import EditCinemaManagerForm, EditDistributorManagerForm, LoginForm, RegisterCinemaManagerForm, RegisterDistributorManagerForm, RequestResetForm, ResetPasswordForm


users = Blueprint('users', __name__)


@users.route("/login", methods=['GET', 'POST'])
def login():
    route_name = request.endpoint
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_mail=form.email.data).first()
        if user and bcrypt.check_password_hash(user.user_password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            print(user.user_name)
            flash(f'Dobro došli, {user.user_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Neispravni podaci za prijavu.', 'danger')
    return render_template('login.html', title='Login', form=form, route_name=route_name)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Zahtev za resetovanje lozinke', sender='noreply@uplatnice.online', recipients=[user.user_mail])
    msg.body = f'''Da biste resetovali lozinku, kliknite na sledeći link:
{url_for('users.reset_token', token=token, _external=True)}

Ako Vi niste napavili ovaj zahtev, molim Vas ignorišite ovaj mejl i neće biti napravljene nikakve izmene na Vašem nalogu.
    '''
    mail.send(msg)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    route_name = request.endpoint
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user  = User.query.filter_by(user_mail=form.email.data).first()
        send_reset_email(user)
        flash('Mejl je poslat na Vašu adresu sa instrukcijama za resetovanje lozinke. ', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Resetovanje lozinke', form=form, legend='', route_name=route_name)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    route_name = request.endpoint
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Ovo je nevažeći ili istekli token.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.user_password = hashed_password
        db.session.commit()
        flash(f'Vaša lozinka je ažurirana!', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Resetovanje lozinke', form=form, legend='Resetovanje lozinke', route_name=route_name)


@users.route("/register_cinema_manager/<int:cinema_properties_id>", methods=['GET', 'POST'])
def register_cinema_manager(cinema_properties_id):
    route_name = request.endpoint
    form = RegisterCinemaManagerForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash("test")
        
        new_user = User(
            user_name=form.user_name.data,
            user_surname=form.user_surname.data,
            user_mail=form.user_mail.data,
            user_password=hashed_password,
            user_type="cinema",
            cinema_properties_id=cinema_properties_id,
            position=form.position.data,
            phone=form.phone.data
        )

        db.session.add(new_user)
        db.session.flush()  # This will assign an ID to new_user

        if form.photo.data:
            # Create directory if it doesn't exist
            upload_dir = os.path.join(app.root_path, 'static', 'img', 'users')
            os.makedirs(upload_dir, exist_ok=True)

            # Generate filename
            filename = f'user_{new_user.id:03d}'
            file_extension = os.path.splitext(form.photo.data.filename)[1]
            filename_with_extension = filename + file_extension

            # Save file
            filepath = os.path.join(upload_dir, filename_with_extension)
            form.photo.data.save(filepath)

            # Update user's photo field
            new_user.photo = filename_with_extension

        db.session.commit()

        flash('Novi menadžer bioskopa je uspešno registrovan!', 'success')
        return redirect(url_for('cinemas.edit_cinema_properties', cinema_properties_id=cinema_properties_id))

    return render_template('cinema_manager.html', form=form, route_name=route_name)


@users.route("/edit_cinema_manager/<int:user_id>", methods=['GET', 'POST'])
def edit_cinema_manager(user_id):
    route_name = request.endpoint
    user = User.query.get(user_id)
    form = EditCinemaManagerForm(obj=user)

    if form.validate_on_submit():
        user.user_name = form.user_name.data
        user.user_surname = form.user_surname.data
        user.user_mail = form.user_mail.data
        user.position = form.position.data
        user.phone = form.phone.data

        if form.photo.data:
            # Delete old photo if exists
            # if user.photo:
            #     old_photo_path = os.path.join(app.root_path, 'static', 'img', 'users', user.photo)
            #     if os.path.exists(old_photo_path):
            #         os.remove(old_photo_path)

            # Save new photo
            upload_dir = os.path.join(current_app.root_path, 'static', 'img', 'users')
            os.makedirs(upload_dir, exist_ok=True)

            filename = f'user_{user.id:03d}'
            file_extension = os.path.splitext(form.photo.data.filename)[1]
            filename_with_extension = filename + file_extension

            filepath = os.path.join(upload_dir, filename_with_extension)
            form.photo.data.save(filepath)

            user.photo = filename_with_extension

        db.session.commit()
        flash('Podaci menadžera bioskopa su uspešno ažurirani!', 'success')
        return redirect(url_for('cinemas.edit_cinema_properties', cinema_properties_id=user.cinema_properties_id))

    return render_template('cinema_manager.html', form=form, route_name=route_name, user=user)


@users.route("/register_distributor_manager/<int:distributor_id>", methods=['GET', 'POST'])
def register_distributor_manager(distributor_id):
    route_name = request.endpoint
    form = RegisterDistributorManagerForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash("test")
        
        new_user = User(
            user_name=form.user_name.data,
            user_surname=form.user_surname.data,
            user_mail=form.user_mail.data,
            user_password=hashed_password,
            user_type="distributor",
            distributor_id=distributor_id,
            cinema_id=None,
            cinema_properties_id=None,
            position=None,
            phone=None,
            photo=None
        )

        db.session.add(new_user)
        db.session.commit()
        flash('Novi distributer je uspešno registrovan.', 'success')
        return redirect(url_for('distributor.edit_distributor', distributor_id=distributor_id))

    return render_template('distributor_manager.html', form=form, route_name=route_name)


@users.route("/edit_distributor_manager/<int:user_id>", methods=['GET', 'POST'])
def edit_distributor_manager(user_id):
    route_name = request.endpoint
    user = User.query.get(user_id)
    form = EditDistributorManagerForm(obj=user)

    if form.validate_on_submit():
        user.user_name = form.user_name.data
        user.user_surname = form.user_surname.data
        user.user_mail = form.user_mail.data

        db.session.commit()
        flash('Podaci distributera su uspešno ažurirani.', 'success')
        return redirect(url_for('distributor.edit_distributor', distributor_id=user.distributor_id))

    return render_template('distributor_manager.html', form=form, route_name=route_name, user=user)