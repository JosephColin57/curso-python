from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import json
import os

app = Flask(__name__)

# Configuracion
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email
        }
    
# Helper para JSON response
def respuesta_json(data, status_code=200):
    response = app.response_class(
        response=json.dumps(data, ensure_ascii=False),
        status=status_code,
        mimetype='application/json'
        )    
    return response

# Crear la base de datos
with app.app_context():
    db.create_all()

# Ruta de registro
@app.route('/register', methods=['POST'])
def registro():
    datos = request.get_json()
    email = datos.get('email')
    password = datos.get('password')

    if not email or not password:
        return respuesta_json({'error': 'Email and password are required'}, 400)

    if Usuario.query.filter_by(email=email).first():
        return respuesta_json({'error': 'Email already exists'}, 400)

    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), 
        bcrypt.gensalt()
        )
    nuevo_usuario = Usuario(email=email, password=hashed_password.decode('utf-8'))
    db.session.add(nuevo_usuario)
    db.session.commit()
    return respuesta_json({'mensaje': 'Usuario creado', 'usuario': nuevo_usuario.to_dict()}, 201)

# Ruta de login
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    email = datos.get('email')
    password = datos.get('password')

    if not email or not password:
        return respuesta_json({'error': 'Email and password are required'}, 400)

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):
        return respuesta_json({'error': 'Invalid credentials'}, 401)

    token_acceso = create_access_token(identity=str(usuario.id))
    return respuesta_json({'mensaje': 'Login successful', 'token': token_acceso})

# GET /perfil - Ruta protegida
@app.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(int(usuario_id))
    if not usuario:
        return respuesta_json({'error': 'User not found'}, 404)

    return respuesta_json({'usuario': usuario.to_dict()})

# GET /contactos → ruta protegida
@app.route('/contactos', methods=['GET'])
@jwt_required()
def contactos():
    return ({'mensaje': f'Usuario {get_jwt_identity()} accedió a contactos'})

if __name__ == '__main__':
    app.run(debug=True, port=5002)