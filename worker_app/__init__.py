from flask import Flask

from config import Config
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
#from flask_login import LoginManager
#from flask_bootstrap import Bootstrap


worker_app = Flask(__name__)
worker_app.config.from_object(Config)
db = SQLAlchemy(worker_app)
#migrate = Migrate(app, db)
#login = LoginManager(app)
#login.login_view = 'login'

from worker_app import routes
#from app import models
#bootstrap = Bootstrap(app)
