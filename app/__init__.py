from flask import Flask

#from flask_googlemaps import GoogleMaps
#from flask_googlemaps import Map

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
bootstrap = Bootstrap(app)

# you can set key as config
#app.config['GOOGLEMAPS_KEY'] = "AIzaSyDFg_Ffjib_aMSSju_6Y5uo12xdjg4679c"
#GoogleMaps(app)
