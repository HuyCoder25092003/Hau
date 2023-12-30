from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary

app = Flask(__name__)
app.secret_key = 'GHFGH&*%^$^*(JHFGHF&Y*R%^$%$^&*TGYGJHFHGVJHGY'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:bomehuytai1@localhost/flightdb?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)
cloudinary.config(
    cloud_name='dexxdoqcx',
    api_key='278211485811135',
    api_secret='5P7IlW3AgwXdC1HfrhPbjP42qvI',
)
