from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SelectMultipleField, DateField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, URL
from wtforms.widgets import ListWidget, CheckboxInput

class RegisterMovieForm(FlaskForm):
    # Polja za unos filma
    original_title = StringField('Originalni naziv filma', validators=[DataRequired(), Length(max=150)])
    local_title = StringField('Lokalni naziv filma', validators=[DataRequired(), Length(max=150)])
    director = StringField('Režiser', validators=[DataRequired(), Length(max=100)])
    actors = TextAreaField('Glumci', validators=[DataRequired()])
    production_country = SelectField('Zemlja produkcije', choices=[], validators=[DataRequired()])  # Dinamički napuniti
    production_company = StringField('Kompanija', validators=[DataRequired(), Length(max=150)])
    production_year = IntegerField('Godina produkcije', validators=[DataRequired(), NumberRange(min=1800, max=2100)])
    duration = IntegerField('Trajanje (u minutima)', validators=[DataRequired(), NumberRange(min=1)])

    # Checkboxes za verzije filma
    versions = SelectMultipleField('Verzije filma', choices=[
        ('originalno', 'Originalno'),
        ('titlovano', 'Titlovano'),
        ('sinhronizovano', 'Sinhronizovano')
    ], option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False), validators=[DataRequired()])

    # Checkboxes za formate projekcije
    projection_formats = SelectMultipleField('Projekcioni format', choices=[
        ('2D', '2D'),
        ('3D', '3D'),
        ('drugo', 'Drugo')
    ], option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False), validators=[DataRequired()])

    poster = URLField('Link do plakata', validators=[DataRequired(), URL()])
    
    # Polja za 3 slike (16:9)
    image_1 = URLField('Slika 1 (16:9)', validators=[DataRequired(), URL()])
    image_2 = URLField('Slika 2 (16:9)', validators=[DataRequired(), URL()])
    image_3 = URLField('Slika 3 (16:9)', validators=[DataRequired(), URL()])

    trailer_link = URLField('Link ka trejleru', validators=[URL()])
    synopsis = TextAreaField('Sinopsis', validators=[DataRequired()])

    # Žanrovi kao checkbox polja - dinamički napuniti kasnije
    genres = SelectMultipleField('Žanr', choices=[], option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False), validators=[DataRequired()])

    release_date = DateField('Datum starta filma', format='%Y-%m-%d', validators=[DataRequired()])

    submit = SubmitField('Dodaj film')


class EditMovieForm(RegisterMovieForm):
    submit = SubmitField('Sačuvaj izmene')
