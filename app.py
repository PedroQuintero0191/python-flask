from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
import os
import datetime
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)


app = Flask(__name__)
app.config["SECRET_KEY"] = "hola"
con = sqlite3.connect("base.db") #conecto a la base
c = con.cursor() #defino el cursor
#c.execute("DROP TABLE Archivos")
c.execute("CREATE TABLE if not exists Archivos (Nombre TEXT, Fecha TEXT, Archivo BOLB)") #Crea la tabla
con.commit()
con.close()


@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        fecha = datetime.date.today()
        con = sqlite3.connect("base.db") #conecto a la base
        c = con.cursor() #defino el cursor
        c.execute("INSERT INTO Archivos VALUES (?, ?, ?)", (f.filename, fecha, f.read()))
        con.commit()
        con.close()
        return 'file uploaded successfully'
    return render_template('upload.html')

@app.route("/download", methods=["GET", "POST"])
def download():
    form = formarchivos()
    if form.validate_on_submit():
        session["nombrelec"] = form.nombrelec.data
        #print(session["nombrelec"])
        con = sqlite3.connect("base.db") #conecto a la base
        c = con.cursor() #defino el cursor
        c.execute("SELECT Archivo FROM Archivos WHERE Nombre= ?", ([form.nombrelec.data]))
        arch = c.fetchone()

        dire = "C:/Users/Usuario/Desktop/"+session["nombrelec"]
        with open(dire, "wb") as output_file:         
            output_file.write(arch[0])
        con.commit()
        con.close()


    return render_template("download.html", form=form)

class formarchivos(FlaskForm):
    con = sqlite3.connect("base.db") #conecto a la base
    c = con.cursor() #defino el cursor
    c.execute("SELECT Nombre FROM Archivos")
    lista = [line[0] for line in c]
    con.commit()
    con.close()
    nombres = [(c,c) for c in lista]
    nombrelec = SelectField('Elija nombre', choices = nombres)
    buscar = SubmitField("Bajar")

if __name__ == '__main__':
   app.run(debug = True)