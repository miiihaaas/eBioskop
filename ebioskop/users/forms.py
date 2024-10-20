from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import FileField, StringField, PasswordField, SubmitField, BooleanField, SelectField
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
        ('urednik filmskog programa', 'Urednik filmskog programa')
    ], validators=[DataRequired()])
    phone = StringField('Telefon', validators=[Optional(), Length(max=20)])
    photo = FileField('Fotografija', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Samo slike su dozvoljene!')])
    submit = SubmitField('Kreiraj korisnika')


class EditCinemaManagerForm(RegisterCinemaManagerForm):
    submit = SubmitField('Ažuriraj podatke korisnika')


class RegisterDistributorManagerForm(FlaskForm):
    user_name = StringField('Ime', validators=[DataRequired(), Length(max=255)])
    user_surname = StringField('Prezime', validators=[DataRequired(), Length(max=255)])
    user_mail = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField('Kreiraj korisnika')


class EditDistributorManagerForm(RegisterDistributorManagerForm):
    submit = SubmitField('Ažuriraj podatke korisnika')