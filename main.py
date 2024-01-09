
#LIBRERIA PARA EL USO DE FLASK
from flask import Flask,render_template, request,url_for,redirect

#LIBRERIA PARA EL USO DE LA BASE DE DATOS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


app = Flask(__name__)

# CONFIGURO PARAMETRO SQLALCHEMY_DATABASE_URI CON LA UBICACION DE LA BASE DE DATOS
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite"

db = SQLAlchemy(app)

#CREAR TABLA
class Todo(db.Model):
   id:Mapped[int]= mapped_column(db.Integer, primary_key=True, autoincrement=True)
   name:Mapped[str]= mapped_column(db.String, nullable=False)
   state: Mapped[str] = mapped_column(db.String,nullable=False,default='Incompleto')
   

# CREAR LA BASE DE DATOS Y TABLAS
with app.app_context():
    db.create_all()


#RUTAS DE LA APLICACION

@app.route("/",methods=['GET','POST'])
def home():
   #SI DISTE CLICK EN AGREGAR
   if request.method == 'POST':
       name = request.form.get('name')
       if name:
           obj= Todo(name=name)
           db.session.add(obj)
           db.session.commit()
   py_lista_tareas = Todo.query.all()
   return render_template('select.html',lista_Tareas = py_lista_tareas)

@app.route("/insert")
def insert():
    return 'ESTO ES UNA PRUEBA INSERTAR'

@app.route("/update/<id>")
def update(id):
   obj=Todo.query.filter_by(id=id).first()
   obj.state= "Completo"
   db.session.commit()
   return redirect(url_for('home'))

@app.route("/delete/<id>")
def delete(id):
   obj=Todo.query.filter_by(id=id).first()
   db.session.delete(obj)
   db.session.commit()
   py_lista_tareas = Todo.query.all()
   return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)