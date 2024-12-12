import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from dotenv import load_dotenv
from flask_caching import Cache

# from ebioskop.models import User
# from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)

# Konfiguracija logovanja
if not os.path.exists('logs'):
    os.mkdir('logs')

# Formatter za logove
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

# Handler za fajl
file_handler = RotatingFileHandler(
    'logs/ebioskop.log', 
    maxBytes=10240000,  # 10MB
    backupCount=10,
    encoding='utf-8'
)
file_handler.setFormatter(formatter)

# Postavljanje nivoa logovanja
if app.debug:
    file_handler.setLevel(logging.DEBUG)
else:
    file_handler.setLevel(logging.INFO)

# Dodavanje handlera u aplikaciju
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
app.logger.info('eBioskop aplikacija je pokrenuta')


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
#kod ispod treba da reši problem Internal Server Error - komunikacija sa serverom
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_APP'] = 'run.py'
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

db = SQLAlchemy(app)
# migrate = Migrate(app, db, compare_type=True, render_as_batch=True) #da primeti izmene npr u dužini stringova
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Molimo Vas da se prijavite.'
app.config['JSON_AS_ASCII'] = False #! da ne bude ascii već utf8
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER') # dodati u .env: 'mail.uplatnice.online'
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT') # dodati u .env: 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
mail = Mail(app)
cache = Cache(app)



from ebioskop.main.routes import main
from ebioskop.users.routes import users
from ebioskop.distributors.routes import distributors
from ebioskop.movies.routes import movies
from ebioskop.cinemas.routes import cinemas
from ebioskop.calendar.routes import calendars
from ebioskop.projections.routes import projections
from ebioskop.errors.routes import errors

from ebioskop.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(distributors)
app.register_blueprint(movies)
app.register_blueprint(cinemas)
app.register_blueprint(calendars)
app.register_blueprint(projections)
app.register_blueprint(errors)