

from flask import render_template
from ebioskop import mail, app
from flask_mail import Message

from ebioskop.models import User


def send_projection_notification_email(projection, movie, cinema, cinema_hall):
    """
    Šalje email obaveštenje distributeru o novoj projekciji.
    
    Args:
        projection: Projection model instanca
        movie: Movie model instanca
        cinema: Cinema model instanca
        cinema_hall: CinemaHall model instanca
    """
    distributor = movie.distributor
    if not distributor:
        return False
    distributor_mail = User.query.filter_by(distributor_id=distributor.id).first().user_mail
    admins = User.query.filter_by(user_type='admin').all()
    recipients=[admin.user_mail for admin in admins] + [distributor_mail]
    print(f'debug: {recipients=}')
    
    subject = f'Nova projekcija filma: {movie.local_title}'
    
    # Pripremamo podatke za email template
    email_data = {
        'projection': projection,
        'movie': movie,
        'cinema': cinema,
        'cinema_hall': cinema_hall,
        'distributor': distributor
    }
    
    # Renderujemo HTML template za email
    html_body = render_template('message_html_send_projection_notification_email.html', **email_data)
    
    
    # Kreiramo i šaljemo email
    msg = Message(
        subject=subject,
        recipients=recipients,  # Može biti lista email adresa
        html=html_body,
        sender=app.config['MAIL_USERNAME']  # Izmenite prema vašim potrebama
    )
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Greška prilikom slanja emaila: {str(e)}")
        return False