from flask_restful import Resource, request, reqparse
import sqlalchemy
from models.ingrediente import IngredienteModel
from conexion_bd import base_de_datos
from models.log import LogModel

serializador = reqparse.RequestParser()

serializador.add_argument(
    'nombre',
    required=True,
    location='json',
    help='falta el nombre',
    type=str,

)

class IngredientesController(Resource):
    def get(self):
        ingredientes = base_de_datos.session.query(IngredienteModel).all()
        resultado = []
        for ingrediente in ingredientes:
            #print(ingrediente)
            diccionario = ingrediente.__dict__
            del diccionario['_sa_instance_state']
            resultado.append(diccionario)
        print(resultado)
        return {
            "message": None,
            "content": resultado
        }

    def post(self):
        
        try:
            data = serializador.parse_args()

            nuevoIngrediente = IngredienteModel(ingredienteNombre = data["nombre"])
            base_de_datos.session.add(nuevoIngrediente)
            base_de_datos.session.commit()
            #print(nuevoIngrediente.__dict__)
            json = {
                "id": nuevoIngrediente.ingredienteId,
                "nombre": nuevoIngrediente.ingredienteNombre
            }
            
            return {
                "message": "Ingrediente creado exitosamente",
                "content": json
            }, 201
        except sqlalchemy.exc.DataError as err:
            base_de_datos.session.rollback()
            nuevoLog = LogModel()
            nuevoLog.logRazon = str(err)
            base_de_datos.session.add(nuevoLog)
            base_de_datos.session.commit()
            return {
                "message": "Error al ingresar el expediente"
            }, 500
        except sqlalchemy.exc.IntegrityError as err:
            base_de_datos.session.rollback()
            nuevoLog = LogModel()
            nuevoLog.logRazon = str(err)
            base_de_datos.session.add(nuevoLog)
            base_de_datos.session.commit()
            return {
                "message": "Ese ingrediente ya existe"
            }, 500
        except Exception as err:
            return {
                "message": "Error desconocido"
            }, 500

class IngredienteController(Resource):
    def get(self, id):

        #resultado = base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteId == id)
        resultado = base_de_datos.session.query(IngredienteModel).filter_by(ingredienteId = id).first()
        print(resultado)
        if resultado:
            data = resultado.__dict__
            del data['_sa_instance_state']
            return {
               "message": None,
               "content": data
            }
        else:
            return {
               "message": "El ingrediente no existe",
               "content": None
            }, 404

    def put(self):
        pass

    def delete(self):
        pass