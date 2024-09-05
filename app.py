from flask import Flask
from flask_smorest import Api
from predict import blp as PredictBlueprint

app = Flask(__name__)

# Configuring the app
app.config['API_TITLE'] = 'Prediction API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)

# Register the api blueprint
api.register_blueprint(PredictBlueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
