from flask import Flask, render_template, jsonify, request, send_from_directory, abort, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_restful import Api
from routes.routes import initialize_routes
from routes.errors import errors

load_dotenv('../.env')
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app, errors=errors)
cors = CORS(app, resources={r"": {"origins": "*"}})


initialize_routes(api)

app.run(port=3000, host='0.0.0.0')