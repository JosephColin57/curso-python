from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from bson.errors import InvalidId
import json
import os

load_dotenv()

app = Flask(__name__)

# Conexión a MongoDB Atlas
client = MongoClient(os.getenv('MONGO_URI'))
db = client['agenda']
contactos = db['contactos']

def respuesta(datos, status=200):
    return app.response_class(
        response=json.dumps(datos, ensure_ascii=False),
        status=status,
        mimetype='application/json'
    )

def formato(contacto):
    contacto['_id'] = str(contacto['_id'])
    return contacto

# GET /contactos → listar todos
@app.route('/contactos', methods=['GET'])
def listar_contactos():
    lista = [formato(c) for c in contactos.find()]
    return respuesta(lista)

# GET /contactos/<id> → obtener uno
@app.route('/contactos/<id>', methods=['GET'])
def obtener_contacto(id):
    try:
        contacto = contactos.find_one({'_id': ObjectId(id)})
    except InvalidId:
        return respuesta({'error': 'ID inválido'}, 400)
    if not contacto:
        return respuesta({'error': 'Contacto no encontrado'}, 404)
    return respuesta(formato(contacto))

# POST /contactos → crear nuevo
@app.route('/contactos', methods=['POST'])
def crear_contacto():
    datos = request.get_json()
    resultado = contactos.insert_one(datos)
    datos['_id'] = str(resultado.inserted_id)
    return respuesta(datos, 201)

# PUT /contactos/<id> → actualizar
@app.route('/contactos/<id>', methods=['PUT'])
def actualizar_contacto(id):
    try:
        datos = request.get_json()
    except Exception:
        return respuesta({'error': 'Datos inválidos'}, 400)
    try:
        contactos.update_one(
            {'_id': ObjectId(id)},
            {'$set': datos}
        )
    except InvalidId:
        return respuesta({'error': 'ID inválido'}, 400)
    contacto = contactos.find_one({'_id': ObjectId(id)})
    if not contacto:
        return respuesta({'error': 'Contacto no encontrado'}, 404)
    return respuesta(formato(contacto))

# DELETE /contactos/<id> → eliminar
@app.route('/contactos/<id>', methods=['DELETE'])
def eliminar_contacto(id):
    try:
        resultado = contactos.delete_one({'_id': ObjectId(id)})
    except InvalidId:
        return respuesta({'error': 'ID inválido'}, 400)
    if resultado.deleted_count == 0:
        return respuesta({'error': 'Contacto no encontrado'}, 404)
    return respuesta({'mensaje': f'Contacto {id} eliminado'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)