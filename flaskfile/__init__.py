from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'fc6285fe00c01600d6b88b6c368eb1'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
lm = LoginManager(app)
lm.login_view = 'login'

from flaskfile import routes