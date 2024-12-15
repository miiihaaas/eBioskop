from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, TimeField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange

class AddProjectionForm(FlaskForm):
    date = DateField('Datum', validators=[DataRequired()])
    time = TimeField('Vreme', validators=[DataRequired()])
    movie_id = SelectField('Film', coerce=int, validators=[DataRequired()])
    version = SelectField('Verzija', choices=[
        ('original', 'Originalno'),
        ('subtitled', 'Titlovano'),
        ('dubbed', 'Sinhronizovano')
    ], validators=[DataRequired()])
    format = SelectField('Format', choices=[
        ('2D', '2D'),
        ('3D', '3D'),
        ('IMAX', 'IMAX')
    ], validators=[DataRequired()])
    tickets_sold = IntegerField('Broj prodatih ulaznica', validators=[DataRequired(), NumberRange(min=0)])
    revenue = FloatField('Zarada', validators=[DataRequired(), NumberRange(min=0)])
    cinema_hall_id = SelectField('Bioskopska sala', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Dodaj projekciju')