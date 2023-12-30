from flightapp import app
from flask import render_template
import utils
import cloudinary.uploader

@app.route('/')
def trangchu():
    return render_template('index.html')


@app.route('/banve')
def banve():
    return render_template('BanVe.html')


@app.route('/trangchu/muave')
def muave():
    return render_template('DatVe.html')


if __name__ == '__main__':
    from flightapp.admin import *
    app.run(debug=True)
