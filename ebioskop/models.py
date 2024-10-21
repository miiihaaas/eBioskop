from sqlalchemy import JSON
from sqlalchemy.ext.associationproxy import association_proxy
from ebioskop import app, db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    user_surname = db.Column(db.String(255), nullable=False)
    user_mail = db.Column(db.String(255), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(50), nullable=False) #! admin, distributor, cinema_ceo, cinema, user, producer
    distributor_id = db.Column(db.Integer, db.ForeignKey('distributor.id'), nullable=True)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinemas.id'), nullable=True)
    cinema_properties_id = db.Column(db.Integer, db.ForeignKey('cinema_properties.id'), nullable=True)  # Veza sa CinemaProperties
    
    distributor = db.relationship('Distributor', back_populates='users', uselist=False)
    cinema = db.relationship('Cinema', back_populates='users', uselist=False)
    cinema_properties = db.relationship('CinemaProperties', back_populates='users')

    position = db.Column(db.String(50), nullable=True)  # Može biti 'kinooperater', 'urednik filmskog programa' ili None
    phone = db.Column(db.String(20), nullable=True)
    photo = db.Column(db.String(50), nullable=True)  # Putanja do fotografije
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"{self.id}, '{self.user_name} {self.user_surname}'"
    


class Municipality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    municipality_name = db.Column(db.String(100), nullable=False)
    municipality_zip_code = db.Column(db.String(10), nullable=False)


class Distributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    pib = db.Column(db.String(20), nullable=False)
    mb = db.Column(db.String(20), nullable=False)
    authorized_person = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200), nullable=True)
    
    youtube = db.Column(db.String(200), nullable=True)
    facebook = db.Column(db.String(200), nullable=True)
    instagram = db.Column(db.String(200), nullable=True)
    tiktok = db.Column(db.String(200), nullable=True)

    users = db.relationship('User', back_populates='distributor', uselist=False)
    movies = db.relationship("Movie", back_populates="distributor")
    
    representative_associations = db.relationship('DistributorRepresentative', back_populates='distributor')
    representatives = association_proxy('representative_associations', 'representative')

    def __repr__(self):
        return f'<Distributor {self.company_name}>'

class Representative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    distributor_associations = db.relationship('DistributorRepresentative', back_populates='representative')
    distributors = association_proxy('distributor_associations', 'distributor')

    def __repr__(self):
        return f'<Representative {self.name}>'

class DistributorRepresentative(db.Model):
    distributor_id = db.Column(db.Integer, db.ForeignKey('distributor.id'), primary_key=True)
    representative_id = db.Column(db.Integer, db.ForeignKey('representative.id'), primary_key=True)
    
    distributor = db.relationship('Distributor', back_populates='representative_associations')
    representative = db.relationship('Representative', back_populates='distributor_associations')

    __table_args__ = (
        db.UniqueConstraint('representative_id', 'distributor_id', name='uq_representative_distributor'),
    )


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(200), nullable=False)
    local_title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    actors = db.Column(db.Text, nullable=False)
    production_country = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    production_year = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    versions = db.Column(JSON, nullable=False)  # ["original", "subtitled", "dubbed"]
    projection_formats = db.Column(JSON, nullable=False)  # ["2D", "3D"]
    age_rating = db.Column(db.String(50), nullable=False) #! 5+, 7+, 12+ ...
    poster = db.Column(db.String(200), nullable=True)  # URL to poster image
    images = db.Column(JSON, nullable=True)  # List of URLs to 3 images
    trailer_link = db.Column(db.String(200))
    synopsis = db.Column(db.Text, nullable=False)
    genres = db.Column(JSON, nullable=False)  # List of genres
    release_date = db.Column(db.Date, nullable=False)
    is_showing_finished = db.Column(db.Boolean, default=False)  # "in_showing", "finished_showing", "scheduled_showing" #! prepraviti da bude check polje "Označiti ako je završeno prikazivanje filma"

    distributor_id = db.Column(db.Integer, db.ForeignKey('distributor.id'), nullable=False)
    distributor = db.relationship("Distributor", back_populates="movies")

    projections = db.relationship("Projection", back_populates="movie")

    def __repr__(self):
        return f'<Movie {self.local_title}>'


class MemberMKPS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinemas.id'))
    cinema = db.relationship('Cinema', backref='members')
    cinema_not_mkps = db.Column(db.String(100))
    job_position = db.Column(db.String(100))
    emails = db.Column(db.String(250))  # Store multiple emails as a comma-separated string
    phones = db.Column(db.String(100))  # Store multiple phone numbers as a comma-separated string
    status = db.Column(db.String(20), default='active')  # active/inactive/honorary

    def set_emails(self, email_list):
        self.emails = ','.join(email_list)

    def get_emails(self):
        return self.emails.split(',') if self.emails else []

    def set_phones(self, phone_list):
        self.phones = ','.join(phone_list)

    def get_phones(self):
        return self.phones.split(',') if self.phones else []


class Cinema(db.Model):
    __tablename__ = 'cinemas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    municipality = db.Column(db.String(100), nullable=False)  # Novo polje za opštinu
    email = db.Column(db.String(500), nullable=False)  # Povećana dužina za više email adresa
    phone = db.Column(db.String(20), nullable=False)
    legal_form = db.Column(db.String(50), nullable=False)
    pib = db.Column(db.String(20), nullable=False)
    mb = db.Column(db.String(20), nullable=False)
    website = db.Column(db.String(200))
    social_links = db.Column(db.Text)  # Promena u Text za jednostavnije rukovanje
    is_member_mkps = db.Column(db.Boolean, default=False)
    is_member_ec = db.Column(db.Boolean, default=False)
    
    users = db.relationship('User', back_populates='cinema', uselist=False)
    properties = db.relationship('CinemaProperties', back_populates='cinema', uselist=False)
    representatives = db.relationship('CinemaRepresentative', back_populates='cinema')
    
    def get_emails(self):
        return [email.strip() for email in self.email.split(',')]

    def set_emails(self, email_list):
        self.email = ', '.join(email.strip() for email in email_list)


class CinemaRepresentative(db.Model):
    __tablename__ = 'cinema_representatives'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)  # Padajući meni, npr. 'direktor'
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    photo = db.Column(db.String(200))  # URL do fotografije
    
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinemas.id'), nullable=False)
    cinema = db.relationship('Cinema', back_populates='representatives')


class CinemaProperties(db.Model):
    __tablename__ = 'cinema_properties'
    
    id = db.Column(db.Integer, primary_key=True)
    local_name = db.Column(db.String(100), nullable=False)  # Lokalni naziv bioskopa
    location = db.Column(db.String(50), nullable=False)  # Padajući meni: centar grada / širi centar grada / periferija
    city_population = db.Column(db.Integer, nullable=False)
    surrounding_population = db.Column(db.Integer, nullable=False)
    has_e_ticket_system = db.Column(db.Boolean, nullable=False)  # Da li postoji sistem elektronske prodaje karata?
    e_ticket_system = db.Column(db.String(100))  # Ako postoji sistem elektronske prodaje, navesti koji
    promotion_methods = db.Column(db.Text, nullable=False)  # Način promocije i reklamiranja
    programming_methods = db.Column(db.Text, nullable=False)  # Način programiranja
    is_distributor = db.Column(db.Boolean, nullable=False)  # Da li je istovremeno i distributer?
    photo_1 = db.Column(db.String(200))  # Naziv fajla za prvu fotografiju
    photo_2 = db.Column(db.String(200))  # Naziv fajla za drugu fotografiju
    
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinemas.id'), nullable=False)
    
    cinema = db.relationship('Cinema', back_populates='properties')
    users = db.relationship('User', back_populates='cinema_properties')
    halls = db.relationship('CinemaHall', back_populates='cinema_properties')

    def __repr__(self):
        return f'<CinemaProperties {self.local_name}>'
    


class CinemaHall(db.Model):
    __tablename__ = 'cinema_halls'
    
    id = db.Column(db.Integer, primary_key=True)
    hall_name = db.Column(db.String(100), nullable=False)  # Naziv sale
    hall_capacity = db.Column(db.Integer, nullable=False)  # Broj sedišta
    workdays = db.Column(JSON, nullable=False)  # Radni dani bioskopa (čuvani kao JSON)
    employee_count = db.Column(db.Integer)  # Koliko ljudi je zaposleno u bioskopu
    year_built = db.Column(db.Integer, nullable=False)  # Godina izgradnje
    dimensions = db.Column(db.String(50), nullable=False)  # Dimenzije sale a x b x c
    distance_to_screen = db.Column(db.Float, nullable=False)  # Udaljenost kino kabine od projekcionog ekrana
    has_power_supply = db.Column(db.Boolean, nullable=False)  # Obezbeđeno mrežno napajanje audio i projekcione opreme
    seat_description = db.Column(db.String(300), nullable=False)  # Opis sedišta u sali
    has_air_conditioning = db.Column(db.Boolean, nullable=False)  # Obezbeđena klimatizacija sale
    has_heating = db.Column(db.Boolean, nullable=False)  # Obezbeđeno grejanje sale
    has_acoustic_treatment = db.Column(db.Boolean, nullable=False)  # Akustička obrada sale
    has_acoustic_screen_treatment = db.Column(db.Boolean, nullable=False)  # Akustička obrada iza projekcionog ekrana
    has_interior_project_docs = db.Column(db.Boolean, nullable=False)  # Da li postoji projektna dokumentacija enterijera sale
    has_tech_project_docs = db.Column(db.Boolean, nullable=False)  # Da li postoji projektna dokumentacija za tehnološku opremu sale
    screen_size = db.Column(db.String(50))  # Veličina projektnog platna a x b
    sound_system = db.Column(db.String(50), nullable=False)  # Zvuk (mono / stereo / dolby / digital standard)
    is_digitalized = db.Column(db.Boolean, nullable=False)  # Da li je sala digitalizovana
    
    # Polja koja se pojavljuju ako je sala digitalizovana
    projector_brand = db.Column(db.String(100))  # Brend projektora
    projector_model = db.Column(db.String(100))  # Model projektora
    projector_resolution = db.Column(db.String(50))  # Rezolucija projektora
    projector_lumens = db.Column(db.Integer)  # Broj lumena
    projector_contrast = db.Column(db.String(50))  # Kontrast projektora
    server_brand = db.Column(db.String(100))  # Brend servera
    server_model = db.Column(db.String(100))  # Model servera
    has_3d_equipment = db.Column(db.Boolean)  # Da li poseduje 3D opremu
    has_silver_screen = db.Column(db.Boolean)  # Da li poseduje silver screen (ako postoji 3D oprema)
    
    # Ostala oprema
    connected_devices = db.Column(JSON)  # Povezani uređaji (Blue-ray, DVD, računar)
    installation_date = db.Column(db.Date)  # Datum instalacije
    acquisition_method = db.Column(JSON)  # Način nabavke opreme i procenat finansiranja
    
    # Polja koja se pojavljuju ako sala nije digitalizovana
    has_video_projector = db.Column(db.Boolean)  # Da li posedujete video projektor (manje rezolucije od 2K)
    video_projector_brand = db.Column(db.String(100))  # Brend video projektora
    video_projector_model = db.Column(db.String(100))  # Model video projektora
    video_projector_resolution = db.Column(db.String(50))  # Rezolucija video projektora
    connected_devices_to_video_projector = db.Column(JSON)  # Povezani uređaji na video projektor
    
    # 35mm projektor
    has_35mm_projector = db.Column(db.Boolean)  # Da li posedujete projektor 35mm
    projector_35mm_brand = db.Column(db.String(100))  # Brend 35mm projektora
    projector_35mm_model = db.Column(db.String(100))  # Model 35mm projektora
    
    cinema_properties_id = db.Column(db.Integer, db.ForeignKey('cinema_properties.id'), nullable=False)
    cinema_properties = db.relationship('CinemaProperties', back_populates='halls')
    
    projections = db.relationship("Projection", back_populates="cinema_hall")


class Projection(db.Model):
    __tablename__ = 'projections'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    version = db.Column(db.String(50), nullable=False)  # "original", "subtitled", "dubbed"
    format = db.Column(db.String(10), nullable=False)  # "2D", "3D"
    tickets_sold = db.Column(db.Integer, default=0)
    revenue = db.Column(db.Float, default=0.0)

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    movie = db.relationship("Movie", back_populates="projections")

    cinema_hall_id = db.Column(db.Integer, db.ForeignKey('cinema_halls.id'), nullable=False)
    cinema_hall = db.relationship("CinemaHall", back_populates="projections")

    def __repr__(self):
        return f'<Projection {self.movie.local_title} on {self.date} at {self.time}>'


with app.app_context():
    db.create_all()
    db.session.commit()