from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from web3 import Web3
import json
import logging
# APIs
from cartorio import cartorio_api
from fiscal import fiscal_api
from util import util_api


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# ---------------------- SWAGGER ----------------------
SWAGGER_URL = '/ui'  
YAML_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    YAML_URL,
    config={'app_name': "API Cartório e Fiscal"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
# ---------------------- CARTORIO ----------------------
app.register_blueprint(cartorio_api, url_prefix='/cartorio')
# ---------------------- FISCAL ----------------------
app.register_blueprint(fiscal_api, url_prefix='/fiscal')
# ---------------------- UTIL ----------------------
app.register_blueprint(util_api, url_prefix='/util')

CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
