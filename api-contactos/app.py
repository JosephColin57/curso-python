from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# Configuracion de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contactos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo — define la tabla en la base de datos
class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email
        }

# Funcion helper para formatear respuestas JSON con acentos.
def respuesta(datos, status=200):
    return app.response_class(
        response=json.dumps(datos, ensure_ascii=False),
        status=status,
        mimetype='application/json'
    )

# Crear tablas al iniciar
with app.app_context():
    db.create_all()

# GET /Contactos -> Listar todos
@app.route('/contactos', methods=['GET'])
def listar_contactos():
    contactos = Contacto.query.all()
    return respuesta([contacto.to_dict() for contacto in contactos])

# GET /Contactos/<id> -> Obtener por ID (uno por uno)
@app.route('/contactos/<int:id>', methods=['GET'])
def obtener_contacto(id):
    contacto = db.session.get(Contacto, id)
    if not contacto:
        return respuesta({'error': 'Contacto no encontrado'}, status=404)
    else:
        return respuesta(contacto.to_dict())

# POST /contactos → crear nuevo
@app.route('/contactos', methods=['POST'])
def crear_contacto():
    datos = request.get_json()
    nuevo = Contacto(
        nombre=datos['nombre'],
        telefono=datos['telefono'],
        email=datos['email']
    )
    db.session.add(nuevo)
    db.session.commit()
    return respuesta(nuevo.to_dict(), status=201)

# PUT /contactos/<id> → actualizar contacto
@app.route('/contactos/<int:id>', methods=['PUT'])
def actualizar_contacto(id):
    contacto = db.session.get(Contacto, id)
    if not contacto:
        return respuesta({'error': 'Contacto no encontrado'}, status=404)
    datos = request.get_json()
    contacto.nombre = datos.get('nombre', contacto.nombre)
    contacto.telefono = datos.get('telefono', contacto.telefono)
    contacto.email = datos.get('email', contacto.email)
    db.session.commit()
    return respuesta(contacto.to_dict())

# DELETE /contactos/<id> → eliminar
@app.route('/contactos/<int:id>', methods=['DELETE'])
def eliminar_contacto(id):
    contacto = db.session.get(Contacto, id)
    if not contacto:
        return respuesta({'error': 'Contacto no encontrado'}, status=404)
    db.session.delete(contacto)
    db.session.commit()
    return respuesta({'mensaje': f'Contacto {id} eliminado'})

if __name__ == '__main__':
    app.run(debug=True)
