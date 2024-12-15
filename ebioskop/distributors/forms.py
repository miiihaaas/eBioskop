import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField, TelField, URLField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from ebioskop.models import Representative
from wtforms import Field
from wtforms.widgets import TextInput


class CustomURLField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return self.data
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0]
        else:
            self.data = ''

    def pre_validate(self, form):
        if self.data:
            if not self.data.strip():
                return

            # Dodajemo http:// ako ne počinje sa http:// ili https://
            if not self.data.startswith(('http://', 'https://')):
                # Ako počinje sa www., dodajemo samo http://
                if self.data.startswith('www.'):
                    self.data = 'http://' + self.data
                else:
                    # Ako ne počinje ni sa www., dodajemo http://www.
                    self.data = 'http://www.' + self.data

            # Proveravamo da li je URL validan nakon transformacije
            url_pattern = re.compile(
                r'^https?://'  # http:// ili https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domen
                r'localhost|'  # localhost
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ili IP
                r'(?::\d+)?'  # opcioni port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

            if not url_pattern.match(self.data):
                raise ValidationError('Molimo unesite ispravnu URL adresu.')


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
    website = CustomURLField('Vebsajt', validators=[Optional(), Length(max=200)])
    
    # Logo field
    logo = FileField('Logotip', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Dozvoljene su samo slike u JPG, JPEG ili PNG formatu!')
    ])
    
    # Social media links
    youtube = CustomURLField('YouTube', validators=[Optional(), Length(max=200)])
    facebook = CustomURLField('Facebook', validators=[Optional(), Length(max=200)])
    instagram = CustomURLField('Instagram', validators=[Optional(), Length(max=200)])
    tiktok = CustomURLField('TikTok', validators=[Optional(), Length(max=200)])
    
    # Representative Distributors (multiple selection)
    representatives = SelectMultipleField(
        'Zastupnici distributera', 
        # choices=[
        #     ('Paramount', 'Paramount'),
        #     ('Universal', 'Universal'),
        #     ('Warner Bros', 'Warner Bros'),
        #     ('Columbia/Sony', 'Columbia/Sony'),
        #     ('Disney', 'Disney'),
        #     ('20th Century Studios', '20th Century Studios'),
        #     ('Drugi', 'Drugi'),
        #     ('Lokalna produkcija', 'Lokalna produkcija')
        # ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Registruj distributera')
    def __init__(self, *args, **kwargs):
        super(RegisterDistributorForm, self).__init__(*args, **kwargs)
        # Dinamički učitavanje predstavnika iz baze
        self.representatives.choices = [(rep.name, rep.name) for rep in Representative.query.all()]


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
    website = CustomURLField('Vebsajt', validators=[Optional(), Length(max=200)])
    
    # Logo field
    logo = FileField('Logotip', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Dozvoljene su samo slike u JPG, JPEG ili PNG formatu!')
    ])
    
    # Social media links
    youtube = CustomURLField('YouTube', validators=[Optional(), Length(max=200)])
    facebook = CustomURLField('Facebook', validators=[Optional(), Length(max=200)])
    instagram = CustomURLField('Instagram', validators=[Optional(), Length(max=200)])
    tiktok = CustomURLField('TikTok', validators=[Optional(), Length(max=200)])
    
    # Representative Distributors (multiple selection)
    representatives = SelectMultipleField(
        'Zastupnici distributera', 
        # choices=[
        #     ('Paramount', 'Paramount'),
        #     ('Universal', 'Universal'),
        #     ('Warner Bros', 'Warner Bros'),
        #     ('Columbia/Sony', 'Columbia/Sony'),
        #     ('Disney', 'Disney'),
        #     ('20th Century Studios', '20th Century Studios'),
        #     ('Drugi', 'Drugi'),
        #     ('Lokalna produkcija', 'Lokalna produkcija')
        # ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Ažuriraj podatke distributera')
    def __init__(self, *args, **kwargs):
        super(EditDistributorForm, self).__init__(*args, **kwargs)
        # Dinamički učitavanje predstavnika iz baze
        self.representatives.choices = [(rep.name, rep.name) for rep in Representative.query.all()]