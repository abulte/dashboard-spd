import os
import dataset

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from marshmallow import ValidationError
from slugify import slugify

from backend.schemas import MeasurementSchema

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")
# CORS only for local dev
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

db = dataset.connect(os.getenv('DATABASE_URL'))


@app.route("/api/measurements", methods=['POST'])
def add_measurement():
    schema = MeasurementSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return {'error': err.messages}, 400
    project = slugify(data["project"])
    table = db[project]
    db_data = {
        "project": project,
        "interval_start": data["interval"]["start"],
        "interval_end": data["interval"]["end"],
        "measurement_name": data["measurement"]["name"],
        "measurement_value": data["measurement"]["value"],
        "measurement_unit": data["measurement"]["unit"],
    }
    table.insert(db_data)
    return db_data, 201


@app.route("/api/measurements/<string:project>", methods=['GET'])
def get_measurements(project):
    project = slugify(project)
    table = db[project]
    return jsonify(list(table.find(project=project)))


@app.route("/", defaults={"path": ""})
# allows routing in vuejs
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")
