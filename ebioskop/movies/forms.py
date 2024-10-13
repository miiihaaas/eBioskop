from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, TextAreaField, SelectField, IntegerField, SelectMultipleField, DateField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, URL, Optional
from wtforms.widgets import ListWidget, CheckboxInput

class RegisterMovieForm(FlaskForm):
    original_title = StringField('Originalni naziv filma', validators=[DataRequired(), Length(max=200)])
    local_title = StringField('Lokalni naziv filma', validators=[DataRequired(), Length(max=200)])
    director = StringField('Režiser', validators=[DataRequired(), Length(max=100)])
    actors = TextAreaField('Glumci', validators=[DataRequired()])
    production_country = SelectField('Zemlja produkcije filma', validators=[DataRequired()])
    company = StringField('Kompanija', validators=[DataRequired(), Length(max=100)])
    production_year = IntegerField('Godina produkcije', validators=[DataRequired()])
    duration = IntegerField('Trajanje (u minutima)', validators=[DataRequired()])
    
    versions = SelectMultipleField('Verzije filma', choices=[
        ('original', 'Originalno'),
        ('subtitled', 'Titlovano'),
        ('dubbed', 'Sinhronizovano')
    ], validators=[DataRequired()])
    
    projection_formats = SelectMultipleField('Projekcioni format', choices=[
        ('2D', '2D'),
        ('3D', '3D')
    ], validators=[DataRequired()])
    
    poster = FileField('Plakat', validators=[
        Optional(),
        FileAllowed(['jpg', 'png'], 'Samo slike su dozvoljene!')
    ])
    
    image_1 = FileField('Slika 1', validators=[
        Optional(),
        FileAllowed(['jpg', 'png'], 'Samo slike su dozvoljene!')
    ])
    image_2 = FileField('Slika 2', validators=[
        Optional(),
        FileAllowed(['jpg', 'png'], 'Samo slike su dozvoljene!')
    ])
    image_3 = FileField('Slika 3', validators=[
        Optional(),
        FileAllowed(['jpg', 'png'], 'Samo slike su dozvoljene!')
    ])
    
    trailer_link = StringField('Link ka trejleru', validators=[Optional(), URL()])
    synopsis = TextAreaField('Sinopsis', validators=[DataRequired()])
    
    genres = SelectMultipleField('Žanr', choices=[
        # Ovde dodajte listu žanrova prema vašim potrebama
        ('action', 'Akcija'),
        ('comedy', 'Komedija'),
        ('drama', 'Drama'),
        # ... dodajte ostale žanrove
    ], validators=[DataRequired()])
    
    release_date = DateField('Dan, mesec i godina starta filma', validators=[DataRequired()])
    
    submit = SubmitField('Registruj film')


class EditMovieForm(RegisterMovieForm):
    status = SelectField('Status', choices=[
        ('scheduled_showing', 'Planirano prikazivanje'),
        ('in_showing', 'U prikazivanju'),
        ('finished_showing', 'Zavrseno prikazivanje')
    ])
    submit = SubmitField('Sačuvaj izmene')