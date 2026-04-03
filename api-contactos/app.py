from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Base temporal en memoria
contactos = [
    {'id': 1, 'nombre': 'Juan Pérez', 'telefono': '1234567890', 'email': 'juan@mail.com'},
    {'id': 2, 'nombre': 'María Gómez', 'telefono': '9876543210', 'email': 'maria@mail.com'},
    {'id': 3, 'nombre': 'Carlos López', 'telefono': '5555555555', 'email': 'carlos@mail.com'},
]

def respuesta(datos, status=200):
    return app.response_class(
        response=json.dumps(datos, ensure_ascii=False),
        status=status,
        mimetype='application/json'
    )

# GET /Contactos -> Listar todos
@app.route('/contactos', methods=['GET'])
def listar_contactos():
    return respuesta(contactos)

# GET /Contactos/<id> -> Obtener por ID (uno por uno)
@app.route('/contactos/<int:id>', methods=['GET'])
def obtener_contacto(id):
    contacto = next((c for c in contactos if c['id'] == id), None)
    if contacto:
        return respuesta(contacto)
    else:
        return respuesta({'error': 'Contacto no encontrado'}, status=404)
    
# POST /contactos → crear nuevo
@app.route('/contactos', methods=['POST'])
def crear_contacto():
    datos = request.get_json()
    nuevo = {
        'id': len(contactos) + 1,
        'nombre': datos['nombre'],
        'telefono': datos['telefono'],
        'email': datos['email']
    }
    contactos.append(nuevo)
    return respuesta(nuevo, 201)
    
# DELETE /contactos/<id> → eliminar
@app.route('/contactos/<int:id>', methods=['DELETE'])
def eliminar_contacto(id):
    contacto = next((c for c in contactos if c['id'] == id), None)
    if contacto:
        contactos.remove(contacto)
        return respuesta({'mensaje': f'Contacto {id} eliminado'})
    return respuesta({'error': 'Contacto no encontrado'}, 404)

# PUT /contactos/<id> → actualizar contacto
@app.route('/contactos/<int:id>', methods=['PUT'])
def actualizar_contacto(id):
    contacto = next((c for c in contactos if c['id'] == id), None)
    if not contacto:
        return respuesta({'error': 'Contacto no encontrado'}, 404)
    datos = request.get_json()
    contacto['nombre'] = datos.get('nombre', contacto['nombre'])
    contacto['telefono'] = datos.get('telefono', contacto['telefono'])
    contacto['email'] = datos.get('email', contacto['email'])
    return respuesta(contacto)


if __name__ == '__main__':
    app.run(debug=True)
