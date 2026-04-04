from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_final.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email
        }

# Create database tables
with app.app_context():
    db.create_all()

# Helper

def respuesta(datos, status=200):
    return app.response_class(
        response=json.dumps(datos, ensure_ascii=False),
        status=status,
        mimetype='application/json'
    )

# Authentication routes

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return respuesta({'error': 'Email y contraseña son requeridos'}, status=400)

    if Usuario.query.filter_by(email=email).first():
        return respuesta({'error': 'Usuario ya existe'}, status=400)

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = Usuario(email=email, password=hashed_password.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

    return respuesta({'message': 'Usuario registrado exitosamente'}, status=201)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return respuesta({'error': 'Email y contraseña son requeridos'}, status=400)

    user = Usuario.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return respuesta({'error': 'Credenciales inválidas'}, status=401)

    access_token = create_access_token(identity=str(user.id))
    return respuesta({'access_token': access_token})


# Contact management routes

@app.route('/contactos', methods=['GET'])
@jwt_required()
def get_contactos():
    user_id = get_jwt_identity()
    contactos = Contacto.query.filter_by(usuario_id=user_id).all()
    return respuesta([contacto.to_dict() for contacto in contactos])

@app.route('/contactos', methods=['POST'])
@jwt_required()
def add_contacto():
    user_id = get_jwt_identity()
    data = request.get_json()
    nombre = data.get('nombre')
    telefono = data.get('telefono')
    email = data.get('email')

    if not nombre or not telefono or not email:
        return respuesta({'error': 'Nombre, teléfono y email son requeridos'}, status=400)

    new_contacto = Contacto(nombre=nombre, telefono=telefono, email=email, usuario_id=user_id)
    db.session.add(new_contacto)
    db.session.commit()

    return respuesta({'message': 'Contacto agregado exitosamente'}, status=201)

@app.route('/contactos/<int:contacto_id>', methods=['PUT'])
@jwt_required()
def update_contacto(contacto_id):
    user_id = get_jwt_identity()
    contacto = Contacto.query.filter_by(id=contacto_id, usuario_id=user_id).first()

    if not contacto:
        return respuesta({'error': 'Contacto no encontrado'}, status=404)

    data = request.get_json()
    contacto.nombre = data.get('nombre', contacto.nombre)
    contacto.telefono = data.get('telefono', contacto.telefono)
    contacto.email = data.get('email', contacto.email)

    db.session.commit()
    return respuesta({'message': 'Contacto actualizado exitosamente'})

@app.route('/contactos/<int:contacto_id>', methods=['DELETE'])
@jwt_required()
def delete_contacto(contacto_id):
    user_id = get_jwt_identity()
    contacto = Contacto.query.filter_by(id=contacto_id, usuario_id=user_id).first()

    if not contacto:
        return respuesta({'error': 'Contacto no encontrado'}, status=404)

    db.session.delete(contacto)
    db.session.commit()
    return respuesta({'message': 'Contacto eliminado exitosamente'})

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5003)