import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import DateField, FileField, FloatField, IntegerField, SelectMultipleField, StringField, BooleanField, SelectField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Optional, Regexp, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput, TextInput
from wtforms import Field
from ebioskop.distributors.forms import CustomURLField


# Forma za registraciju bioskopa
class RegisterCinemaForm(FlaskForm):
    # Polja za unos podataka o bioskopu
    name = StringField('Naziv bioskopa', validators=[DataRequired(), Length(max=150)])
    country = StringField('Zemlja', validators=[DataRequired(), Length(max=100)])
    address = StringField('Adresa', validators=[DataRequired(), Length(max=200)])
    postal_code = StringField('Poštanski broj', validators=[DataRequired(), Length(max=20)])
    city = StringField('Mesto', validators=[DataRequired(), Length(max=100)])
    municipality = SelectField('Opština', validators=[DataRequired(), Length(max=100)])
    email = StringField('Imejl', validators=[DataRequired(), Length(max=500), Regexp(r'^(\S+@\S+\.\S+)(,\s*\S+@\S+\.\S+)*$', message="Unesite validne email adrese odvojene zarezom")])  # Provera unosa više mejlova odvojenih zarezom
    phone = StringField('Telefon', validators=[DataRequired(), Length(max=20)])
    legal_form = SelectField('Oblik pravnog lica', choices=[('javna ustanova', 'Javna ustanova'), ('kompanija', 'Kompanija')], validators=[DataRequired()])
    pib = StringField('PIB', validators=[DataRequired(), Length(max=20)])
    mb = StringField('MB', validators=[DataRequired(), Length(max=20)])
    website = CustomURLField('Vebsajt', validators=[Optional(), Length(max=200)])
    logo = FileField('Logotip', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
    
    # Polje za unos društvenih mreža
    social_links = TextAreaField('Linkovi društvenih mreža', validators=[Optional(), Length(max=500)])  # Unos u JSON formatu
    
    # Da li je član MKS i EC
    is_member_mkps = BooleanField('Da li je član MKS?', default=False)
    is_member_ec = BooleanField('Da li je član Europa Cinemas?', default=False)
    
    submit = SubmitField('Registruj bioskop')

# Forma za izmenu bioskopa
class EditCinemaForm(FlaskForm):
    # Polja za unos podataka o bioskopu (identična kao kod registracije)
    name = StringField('Naziv bioskopa', validators=[DataRequired(), Length(max=150)])
    country = StringField('Zemlja', validators=[DataRequired(), Length(max=100)])
    address = StringField('Adresa', validators=[DataRequired(), Length(max=200)])
    postal_code = StringField('Poštanski broj', validators=[DataRequired(), Length(max=20)])
    city = StringField('Mesto', validators=[DataRequired(), Length(max=100)])
    municipality = SelectField('Opština', validators=[DataRequired(), Length(max=100)])
    email = StringField('Imejl', validators=[DataRequired(), Length(max=500), Regexp(r'^(\S+@\S+\.\S+)(,\s*\S+@\S+\.\S+)*$', message="Unesite validne email adrese odvojene zarezom")])  # Provera unosa više mejlova odvojenih zarezom
    phone = StringField('Telefon', validators=[DataRequired(), Length(max=20)])
    legal_form = SelectField('Oblik pravnog lica', choices=[('javna ustanova', 'Javna ustanova'), ('kompanija', 'Kompanija')], validators=[DataRequired()])
    pib = StringField('PIB', validators=[DataRequired(), Length(max=20)])
    mb = StringField('MB', validators=[DataRequired(), Length(max=20)])
    website = CustomURLField('Vebsajt', validators=[Optional(), Length(max=200)])
    logo = FileField('Logotip', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
    
    # Polje za unos društvenih mreža
    social_links = TextAreaField('Linkovi društvenih mreža', validators=[Optional(), Length(max=500)])  # Unos u JSON formatu
    
    # Da li je član MKS i EC
    is_member_mkps = BooleanField('Da li je član MKS?', default=False)
    is_member_ec = BooleanField('Da li je član Europa Cinemas?', default=False)
    
    submit = SubmitField('Izmeni bioskop')


class RegisterCinemaRepresentativeForm(FlaskForm):
    first_name = StringField('Ime', validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Prezime', validators=[DataRequired(), Length(min=2, max=100)])
    position = SelectField('Pozicija', choices=[('direktor', 'Direktor'), ('menadžer', 'Menadžer'), ('administracija', 'Administracija')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    phone = StringField('Telefon', validators=[DataRequired(), Length(max=20)])
    photo = FileField('Fotografija', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Samo slike su dozvoljene!')])
    submit = SubmitField('Dodaj predstavnika')


class EditCinemaRepresentativeForm(FlaskForm):
    first_name = StringField('Ime', validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Prezime', validators=[DataRequired(), Length(min=2, max=100)])
    position = SelectField('Pozicija', choices=[('direktor', 'Direktor'), ('menadžer', 'Menadžer'), ('administracija', 'Administracija')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    phone = StringField('Telefon', validators=[DataRequired(), Length(max=20)])
    photo = FileField('Fotografija', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Samo slike su dozvoljene!')])
    submit = SubmitField('Izmeni predstavnika')



# Prilagođeni validator za pozitivan broj
def positive_number_check(form, field):
    if field.data is not None and field.data < 0:
        raise ValidationError('Broj mora biti pozitivan.')


class RegisterCinemaPropertiesForm(FlaskForm):
    local_name = StringField('Lokalni naziv', validators=[DataRequired(message="Lokalni naziv je obavezan.")])
    location = SelectField('Lokacija', choices=[('centar grada', 'Centar grada'), ('širi centar grada', 'Širi centar grada'), ('periferija', 'Periferija')], validators=[DataRequired(message="Lokacija je obavezna.")])
    city_population = IntegerField('Broj stanovnika grada', validators=[DataRequired(message="Broj stanovnika grada je obavezan."), positive_number_check])
    surrounding_population = IntegerField('Broj stanovnika grada sa okolinom', validators=[DataRequired(message="Broj stanovnika grada sa okolinom je obavezan."), positive_number_check])
    has_e_ticket_system = BooleanField('Označiti ukoliko postoji sistem elektronske prodaje karata')
    e_ticket_system = StringField('Sistem za online prodaju karata', validators=[Optional()])
    promotion_methods = TextAreaField('Na koji način vršite promociju bioskopa i reklamiranje filmskog programa?', validators=[DataRequired(message="Metode promocije su obavezne."), Length(max=500)])
    programming_methods = TextAreaField('Na koji način vršite programiranje u vašem bioskopu?', validators=[DataRequired(message="Metode programiranja su obavezne."), Length(max=500)])
    is_distributor = BooleanField('Označiti ako je prikazivač istovremeno i distributer')
    photo_1 = FileField('Fotografija 1', validators=[Optional(), FileAllowed(['jpg', 'png'], 'Samo slike!')])
    photo_2 = FileField('Fotografija 2', validators=[Optional(), FileAllowed(['jpg', 'png'], 'Samo slike!')])
    submit = SubmitField('Registruj Svojstva Bioskopa')

class EditCinemaPropertiesForm(FlaskForm):
    local_name = StringField('Lokalni naziv', validators=[DataRequired(message="Lokalni naziv je obavezan.")])
    location = SelectField('Lokacija', choices=[('centar grada', 'Centar grada'), ('širi centar grada', 'Širi centar grada'), ('periferija', 'Periferija')], validators=[DataRequired(message="Lokacija je obavezna.")])
    city_population = IntegerField('Broj stanovnika grada', validators=[DataRequired(message="Broj stanovnika grada je obavezan."), positive_number_check])
    surrounding_population = IntegerField('Broj stanovnika grada sa okolinom', validators=[DataRequired(message="Broj stanovnika grada sa okolinom je obavezan."), positive_number_check])
    has_e_ticket_system = BooleanField('Označiti ukoliko postoji sistem elektronske prodaje karata?')
    e_ticket_system = StringField('Sistem za online prodaju karata', validators=[Optional()])
    promotion_methods = TextAreaField('Na koji način vršite promociju bioskopa i reklamiranje filmskog programa?', validators=[DataRequired(message="Metode promocije su obavezne."), Length(max=500)])
    programming_methods = TextAreaField('Na koji način vršite programiranje u vašem bioskopu?', validators=[DataRequired(message="Metode programiranja su obavezne."), Length(max=500)])
    is_distributor = BooleanField('Označiti ako je prikazivač istovremeno i distributer')
    photo_1 = FileField('Fotografija 1', validators=[Optional(), FileAllowed(['jpg', 'png'], 'Samo slike!')])
    photo_2 = FileField('Fotografija 2', validators=[Optional(), FileAllowed(['jpg', 'png'], 'Samo slike!')])
    submit = SubmitField('Izmeni Svojstva Bioskopa')


class FinancingSourceForm(FlaskForm):
    source = StringField('Izvor finansiranja')
    percentage = FloatField('Procenat učešća', validators=[Optional(), NumberRange(min=0, max=100)])


class RegisterCinemaHallForm(FlaskForm):
    hall_name = StringField('Naziv sale', validators=[DataRequired(message="Naziv sale je obavezan.")])
    hall_capacity = IntegerField('Broj sedišta', validators=[DataRequired(message="Broj sedišta je obavezan.")])
    
    workdays = SelectMultipleField('Radni dani bioskopa', 
                                choices=[('ponedeljak', 'Ponedeljak'), ('utorak', 'Utorak'),
                                            ('sreda', 'Sreda'), ('četvrtak', 'Četvrtak'),
                                            ('petak', 'Petak'), ('subota', 'Subota'),
                                            ('nedelja', 'Nedelja')],
                                option_widget=CheckboxInput(), 
                                widget=ListWidget(prefix_label=False),
                                validators=[DataRequired(message="Odaberite radne dane.")])
    
    employee_count = IntegerField('Broj zaposlenih u bioskopu', validators=[Optional()])
    year_built = IntegerField('Godina izgradnje', validators=[DataRequired(message="Godina izgradnje je obavezna.")])
    dimensions = StringField('Dimenzije sale (u metrima) [š x d x v]', validators=[DataRequired(message="Dimenzije sale su obavezne.")])
    distance_to_screen = FloatField('Udaljenost kino kabine od projekcionog ekrana (u metrima)', validators=[DataRequired(message="Udaljenost od ekrana je obavezna.")])
    
    has_power_supply = BooleanField('Označite ukoliko je obezbeđeno mrežno napajanje audio i projekcione opreme')
    seat_description = TextAreaField('Opis sedišta (do 300 karaktera)', validators=[DataRequired(message="Opis sedišta je obavezan."), Length(max=300)])
    has_air_conditioning = BooleanField('Označite ukoliko je obezbeđena klimatizacija sale')
    has_heating = BooleanField('Označite ukoliko je obezbeđeno grejanje sale')
    has_acoustic_treatment = BooleanField('Označite ukoliko postoji akustička obrada sale')
    has_acoustic_screen_treatment = BooleanField('Označite ukoliko postoji akustička obrada iza projekcionog ekrana')
    has_interior_project_docs = BooleanField('Označite ukoliko postoji projektna dokumentacija enterijera sale')
    has_tech_project_docs = BooleanField('Označite ukoliko postoji projektna dokumentacija za tehnološku opremu sale')
    
    screen_size = StringField('Veličina projektnog platna (a x b)', validators=[Optional()])
    sound_system = SelectField('Zvuk', choices=[('mono', 'Mono'), ('stereo', 'Stereo'), ('dolby', 'Dolby'), ('digital', 'Digital standard')],
                                validators=[DataRequired(message="Odaberite zvučni sistem.")])
    
    is_digitalized = BooleanField('Označite ukoliko je sala digitalizovana')
    projector_brand = StringField('Brend projektora', validators=[Optional()])
    projector_model = StringField('Model projektora', validators=[Optional()])
    projector_resolution = StringField('Rezolucija projektora', validators=[Optional()])
    projector_lumens = IntegerField('Broj lumena', validators=[Optional()])
    projector_contrast = StringField('Kontrast projektora', validators=[Optional()])
    server_brand = StringField('Brend servera', validators=[Optional()])
    server_model = StringField('Model servera', validators=[Optional()])
    has_3d_equipment = BooleanField('Označiti ukoliko posedujete 3D opremu')
    has_silver_screen = BooleanField('Označiti ukoliko posedujete silver screen')
    
    connected_devices = SelectMultipleField('Konekcije sa glavnim projektorom', choices=[('blu-ray', 'Blu-ray'), ('dvd', 'DVD'), ('racunar', 'Računar')],
                                            option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False),
                                            validators=[Optional()])
    
    installation_date = DateField('Datum instalacije', format='%Y-%m-%d', validators=[Optional()])
    
    acquisition_method = SelectMultipleField('Način nabavke opreme', choices=[('sopstvena_sredstva', 'Sopstvena sredstva'),
                                                                                ('investicija_lokalne_samouprave', 'Investicija lokalne samouprave'),
                                                                                ('nacionalni_konkurs', 'Nacionalni konkurs'),
                                                                                ('evropski_konkurs', 'Evropski konkurs'),
                                                                                ('ugovor_sa_trecim_licima', 'Ugovor sa trećim licima')],
                                                option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False),
                                                validators=[Optional()])
    
    # Polja za video projektor ako sala nije digitalizovana
    has_video_projector = BooleanField('Označiti ukoliko posedujete video projektor (manje rezolucije od 2K)?')
    video_projector_brand = StringField('Brend video projektora', validators=[Optional()])
    video_projector_model = StringField('Model video projektora', validators=[Optional()])
    video_projector_resolution = StringField('Rezolucija video projektora', validators=[Optional()])
    connected_devices_to_video_projector = SelectMultipleField('Konekcije sa video projektorom', choices=[('blu-ray', 'Blu-ray'), ('dvd', 'DVD'), ('racunar', 'Računar')],
                                                                option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False),
                                                                validators=[Optional()])
    
    # Polja za 35mm projektor
    has_35mm_projector = BooleanField('Označiti ukoliko posedujete projektor 35mm')
    projector_35mm_brand = StringField('Brend 35mm projektora', validators=[Optional()])
    projector_35mm_model = StringField('Model 35mm projektora', validators=[Optional()])
    
    submit = SubmitField('Kreiraj salu')
    
    def validate_dimensions(form, field):
        if not re.match(r'^\d+(\.\d+)?\s*x\s*\d+(\.\d+)?\s*x\s*\d+(\.\d+)?$', field.data):
            raise ValidationError('Unesite dimenzije u formatu a x b x c (npr. 10.5 x 8.0 x 3.5)')

    def validate_screen_size(form, field):
        if field.data and not re.match(r'^\d+(\.\d+)?\s*x\s*\d+(\.\d+)?$', field.data):
            raise ValidationError('Unesite veličinu platna u formatu a x b (npr. 10.5 x 6.0)')


class EditCinemaHallForm(RegisterCinemaHallForm):
    submit = SubmitField('Izmeni salu')


class RegisterMemberMKSForm(FlaskForm):
    name = StringField('Ime', validators=[DataRequired(), Length(max=50)])
    surname = StringField('Prezime', validators=[DataRequired(), Length(max=50)])
    address = StringField('Adresa', validators=[Optional(), Length(max=200)])
    city = StringField('Mesto', validators=[Optional(), Length(max=100)])
    cinema_id = SelectField('MKS Cinema', coerce=int, validators=[Optional()])
    cinema_not_mkps = StringField('Non-MKS Cinema', validators=[Optional(), Length(max=100)])
    job_position = StringField('Radno mesto', validators=[Optional(), Length(max=100)])
    emails = TextAreaField('Imejl adresa', validators=[Optional()])
    phones = TextAreaField('Telefon', validators=[Optional()])
    status = SelectField('Status', choices=[('Aktivan', 'Aktivan'), ('Neaktivan', 'Neaktivan'), ('Počasni', 'Počasni')], validators=[DataRequired()])
    submit = SubmitField('Kreiraj MKS člana')

    # def validate(self):
    #     if not super(RegisterMemberMKSForm, self).validate():
    #         return False
        
    #     if not self.cinema.data and not self.cinema_not_mkps.data:
    #         self.cinema.errors.append('Either MKS Cinema or Non-MKS Cinema must be specified.')
    #         return False
        
    #     if self.cinema.data and self.cinema_not_mkps.data:
    #         self.cinema.errors.append('You cannot specify both MKS Cinema and Non-MKS Cinema.')
    #         return False
        
    #     # Validate emails
    #     if self.emails.data:
    #         email_list = [email.strip() for email in self.emails.data.split(',')]
    #         if len(email_list) > 2:
    #             self.emails.errors.append('You can enter up to 2 email addresses.')
    #             return False
    #         for email in email_list:
    #             if not Email()(self, email):
    #                 self.emails.errors.append(f'Invalid email address: {email}')
    #                 return False
        
    #     # Validate phone numbers
    #     if self.phones.data:
    #         phone_list = [phone.strip() for phone in self.phones.data.split(',')]
    #         if len(phone_list) > 2:
    #             self.phones.errors.append('You can enter up to 2 phone numbers.')
    #             return False
    #         for phone in phone_list:
    #             if len(phone) < 6 or len(phone) > 20:
    #                 self.phones.errors.append(f'Invalid phone number length: {phone}')
    #                 return False
        
    #     return True


class EditMemberMKSForm(RegisterMemberMKSForm):
    submit = SubmitField('Izmeni MKSčlana')