from flask_restful import Resource
from models.ingrediente import IngredienteModel


class IngredientesController(Resource):
    def get(self):
        print("Ingrso al get")
        return {
            "message": "Bienvenido al get"
        }

    def post(self):
        return {
            "message": "Bienvenido al post"
        }