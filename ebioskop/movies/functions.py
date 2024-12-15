from hmac import new
import os
# from sqlalchemy import in_, or_
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread
from werkzeug.utils import secure_filename
from ebioskop import mail, app
from ebioskop.models import User


# Funkcija za čuvanje slike
def save_image(file, filename):
    if file and file.filename:
        filename = secure_filename(filename)
        upload_folder = os.path.join(current_app.root_path, 'static', 'img', 'movies')
        
        # Kreiranje foldera ako ne postoji
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return os.path.join('static', 'img', 'movies', filename)
    else:
        print(f'debug: nije učitan fajl za {filename}!')
    return None


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html_body):
    # app = current_app._get_current_object()
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=recipients)
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_email_about_movie(movie, new_movie=None):
    # Pronađi sve korisnike koji su admini, distributeri ili bioskopi
    recipients = User.query.filter(User.user_type.in_(['admin', 'distributor', 'cinema'])).all() #! nešto mi je sumnjiv ovaj in_???
    print(f'debug: {recipients=}')
    # Kreiraj listu email adresa
    email_list = [user.user_mail for user in recipients]
    print(f'debug: {email_list=}')
    # Pripremi sadržaj emaila
    if new_movie:
        subject = f"Novi film: {movie.local_title}"
    else:
        subject = f"Promjena podataka o filmu: {movie.local_title}"
    poster = movie.poster
    html_body = render_template('message_html_send_email_about_movie.html', 
                                new_movie=new_movie,
                                movie_name=movie.local_title,
                                director=movie.director,
                                distributor=movie.distributor.company_name,
                                release_date=movie.release_date.strftime('%d.%m.%Y'), 
                                poster=poster)
    
    # Pošalji email
    send_email(subject, email_list, html_body)