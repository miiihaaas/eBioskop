from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import FileField, StringField, PasswordField, SubmitField, BooleanField, SelectField, TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_wtf.file import FileAllowed
from ebioskop import db
from ebioskop.models import User


class LoginForm(FlaskForm):
    email = StringField('Mejl', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    remember = BooleanField('Zapamti me')
    submit = SubmitField('Ulogujte se')
    

class RequestResetForm(FlaskForm):
    email = StringField('Mejl', validators=[DataRequired(), Email()])
    submit = SubmitField('Zatražite reset lozinke')

    def validate_email(self, email):
        user = User.query.filter_by(user_mail=email.data).first()
        if user is None:
            raise ValidationError('Ne postoji korisnik sa Vašim emailom. Zatražite od vašeg administratora da Vam otvori nalog.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova lozinka', validators=[DataRequired()])
    confirm_password = PasswordField('Potvrdite novu lozinku', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Resetujte lozinku')


class RegisterCinemaManagerForm(FlaskForm):
    user_name = StringField('Ime', validators=[DataRequired(), Length(max=255)])
    user_surname = StringField('Prezime', validators=[DataRequired(), Length(max=255)])
    user_mail = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    position = SelectField('Pozicija', choices=[
        ('', 'Izaberite poziciju'),
        ('kinooperater', 'Kinooperater'),
        ('urednik filmskog programa', 'Urednik filmskog programa'),
        ('direktor', 'Direktor'),
        ('ostalo', 'Ostalo')
    ], validators=[DataRequired()])
    phone = StringField('Telefon', validators=[Optional(), Length(max=20)])
    photo = FileField('Fotografija', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Samo slike su dozvoljene!')])
    submit = SubmitField('Kreiraj profil korisnika')


class EditCinemaManagerForm(RegisterCinemaManagerForm):
    submit = SubmitField('Ažuriraj podatke profila korisnika')


class RegisterDistributorManagerForm(FlaskForm):
    user_name = StringField('Ime', validators=[DataRequired(), Length(max=255)])
    user_surname = StringField('Prezime', validators=[DataRequired(), Length(max=255)])
    user_mail = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField('Kreiraj profil korisnika')


class EditDistributorManagerForm(RegisterDistributorManagerForm):
    submit = SubmitField('Ažuriraj podatke profila korisnika')


class PrivilegedUserForm(FlaskForm):
    user_name = StringField('Ime', 
        validators=[DataRequired(message='Ime je obavezno polje'), 
                   Length(min=2, max=50, message='Ime mora biti između 2 i 50 karaktera')])
    
    user_surname = StringField('Prezime', 
        validators=[DataRequired(message='Prezime je obavezno polje'), 
                   Length(min=2, max=50, message='Prezime mora biti između 2 i 50 karaktera')])
    
    user_mail = StringField('Email',
        validators=[DataRequired(message='Email je obavezno polje'),
                   Email(message='Unesite validnu email adresu')])
    
    phone = TelField('Telefon')
    
    photo = FileField('Profilna fotografija',
                     validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                          message='Dozvoljena je samo jpg, jpeg ili png fotografija')])
    
    submit = SubmitField('Sačuvaj')

    def validate_user_mail(self, user_mail):
        """Provera da li email već postoji u bazi"""
        user = User.query.filter_by(user_mail=user_mail.data).first()
        if user:
            raise ValidationError('Email adresa je već registrovana u sistemu.')

class EditPrivilegedUserForm(PrivilegedUserForm):
    submit = SubmitField('Ažuriraj')

    def __init__(self, original_email, *args, **kwargs):
        super(EditPrivilegedUserForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_user_mail(self, user_mail):
        """Provera da li email već postoji u bazi, ali dozvoljava isti email trenutnom korisniku"""
        if user_mail.data != self.original_email:
            user = User.query.filter_by(user_mail=user_mail.data).first()
            if user:
                raise ValidationError('Email adresa je već registrovana u sistemu.')