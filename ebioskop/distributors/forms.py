from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField, TelField, URLField
from wtforms.validators import DataRequired, Email, Length, Optional, URL
from wtforms.widgets import ListWidget, CheckboxInput


class RegisterDistributorForm(FlaskForm):
    company_name = StringField('Naziv kompanije', validators=[DataRequired(), Length(max=150)])
    country = StringField('Zemlja', validators=[DataRequired(), Length(max=100)])
    address = StringField('Adresa', validators=[DataRequired(), Length(max=200)])
    postal_code = StringField('Poštanski broj', validators=[DataRequired(), Length(max=20)])
    city = StringField('Mesto', validators=[DataRequired(), Length(max=100)])
    email = StringField('Imejl', validators=[DataRequired(), Email(), Length(max=200)])
    phone = TelField('Telefon', validators=[DataRequired(), Length(max=50)])
    pib = StringField('PIB', validators=[DataRequired(), Length(max=20)])
    mb = StringField('MB', validators=[DataRequired(), Length(max=20)])
    authorized_person = StringField('Ovlašćeno lice', validators=[DataRequired(), Length(max=100)])
    website = URLField('Vebsajt', validators=[Optional(), URL(), Length(max=200)])
    
    # Social media links
    youtube = URLField('YouTube', validators=[Optional(), URL(), Length(max=200)])
    facebook = URLField('Facebook', validators=[Optional(), URL(), Length(max=200)])
    instagram = URLField('Instagram', validators=[Optional(), URL(), Length(max=200)])
    tiktok = URLField('TikTok', validators=[Optional(), URL(), Length(max=200)])
    
    # Representative Distributors (multiple selection)
    representatives = SelectMultipleField(
        'Zastupnici distributera', 
        choices=[
            ('Paramount', 'Paramount'),
            ('Universal', 'Universal'),
            ('Warner Bros', 'Warner Bros'),
            ('Columbia/Sony', 'Columbia/Sony'),
            ('Disney', 'Disney'),
            ('20th Century Studios', '20th Century Studios'),
            ('Drugi', 'Drugi'),
            ('Lokalna produkcija', 'Lokalna produkcija')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Registruj distributera')


class EditDistributorForm(FlaskForm):
    company_name = StringField('Naziv kompanije', validators=[DataRequired(), Length(max=150)])
    country = StringField('Zemlja', validators=[DataRequired(), Length(max=100)])
    address = StringField('Adresa', validators=[DataRequired(), Length(max=200)])
    postal_code = StringField('Poštanski broj', validators=[DataRequired(), Length(max=20)])
    city = StringField('Mesto', validators=[DataRequired(), Length(max=100)])
    email = StringField('Imejl', validators=[DataRequired(), Email(), Length(max=200)])
    phone = TelField('Telefon', validators=[DataRequired(), Length(max=50)])
    pib = StringField('PIB', validators=[DataRequired(), Length(max=20)])
    mb = StringField('MB', validators=[DataRequired(), Length(max=20)])
    authorized_person = StringField('Ovlašćeno lice', validators=[DataRequired(), Length(max=100)])
    website = URLField('Vebsajt', validators=[Optional(), URL(), Length(max=200)])
    
    # Social media links
    youtube = URLField('YouTube', validators=[Optional(), URL(), Length(max=200)])
    facebook = URLField('Facebook', validators=[Optional(), URL(), Length(max=200)])
    instagram = URLField('Instagram', validators=[Optional(), URL(), Length(max=200)])
    tiktok = URLField('TikTok', validators=[Optional(), URL(), Length(max=200)])
    
    # Representative Distributors (multiple selection)
    representatives = SelectMultipleField(
        'Zastupnici distributera', 
        choices=[
            ('Paramount', 'Paramount'),
            ('Universal', 'Universal'),
            ('Warner Bros', 'Warner Bros'),
            ('Columbia/Sony', 'Columbia/Sony'),
            ('Disney', 'Disney'),
            ('20th Century Studios', '20th Century Studios'),
            ('Drugi', 'Drugi'),
            ('Lokalna produkcija', 'Lokalna produkcija')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Ažuriraj podatke distributera')