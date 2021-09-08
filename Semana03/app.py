from flask import Flask
from conexion_bd import base_de_datos
from models.ingrediente import IngredienteModel
from models.receta import RecetaModel
from models.preparacion import PreparacionModel
from models.recetas_ingredientes import RecetaIngredienteModel
from models.log import LogModel
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from controllers.ingrediente import (IngredientesController,
                                     IngredienteController,
                                     FiltroIngredientesController)
from controllers.receta import RecetasController, RecetaController
from controllers.receta_ingrediente import RecetaIngredientesController
from controllers.preparacion import PreparacionesController

from flask_restful import Api
from os import environ
from dotenv import load_dotenv

load_dotenv()

#CONIFGURACION DE SWAGGER
SWAGGER_URL ="/api/docs"
API_URL ="/static/swagger.json"
swagger_blueprint=get_swaggerui_blueprint(
    base_url=SWAGGER_URL,
    api_url =API_URL,
    config={
        "app_name": "Reporterria falaaaasas"
    }
)

#FIN DE CONFIGURACION


app = Flask(__name__)
CORS(app=app, origins="*", methods=["GET", "POST", "PUT", "DELETE"], allow_headers="*")
#CORS(app=app, origins=["http://mipagina.com", "https://segundapagina.com"])
api = Api(app=app)
app.register_blueprint(swagger_blueprint)
#                                        mysql://username:password@host/db_name
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')
# si se establece True SqlAchemy rastreara las modificaciones de los objetos (modelos) y lanzara señales de cambio, su valor predeterminado es None . igual habilita el tracking pero emite una advertencia que en futuras versiones se removera el valor x default None y si o si tendremos que indicar un valor inicial
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# inicia la conexion con la bd para darle las credenciales definidias en el app.config
base_de_datos.init_app(app)

# eliminara todas las tablas registradas en nuestro proyecto
# base_de_datos.drop_all(app=app)


# creara las tablas aun no mapeadas y si todo esta bien no devolvera nada
base_de_datos.create_all(app=app)


@app.route("/")
def initial_controller():
    return {
        "message": "Bienvenido a mi API de REPOSTERIA 🥧"
    }


# ZONA DE ENRUTAMIENTO
api.add_resource(IngredientesController, '/ingredientes')
api.add_resource(IngredienteController, '/ingrediente/<int:id>')
api.add_resource(FiltroIngredientesController, '/buscar_ingrediente')

api.add_resource(RecetasController, '/recetas')
api.add_resource(RecetaController, '/receta/<int:id>')

api.add_resource(RecetaIngredientesController, '/recetas_ingredientes')

api.add_resource(PreparacionesController, '/preparaciones',
                 '/preparaciones/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
