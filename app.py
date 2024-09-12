from flask import Flask, jsonify, abort, make_response, request
from models import plytoteka


app = Flask(__name__)
app.config["SECRET_KEY"] = "doremifasola"

@app.route("/api/v1/plytoteka", methods=["GET"])
def plytoteka_list_api_v1():
    return jsonify(plytoteka.all())

@app.route("/api/v1/plytoteka/", methods=["POST"])
def create_plyta():
    if not request.json or not 'artysta' in request.json:
        abort(400)
    plyta = {
        'id': plytoteka.all()[-1]['id'] + 1,
        'artysta': request.json['artysta'],
        'plyta' : request.json['plyta'],
        'rok_wydania' : request.json['rok_wydania'],
        'opis': request.json.get('opis', ""),
        'w_kolekcji': False
    }
    plytoteka.create(plyta)
    return jsonify({'plyta': plyta}), 201

@app.route("/api/v1/plytoteka/<int:plytoteka_id>", methods = ['DELETE'])
def delete_plyta(plytoteka_id):
    result = plytoteka.delete(plytoteka_id)
    if not result:
        abort(404)
    return jsonify({'result':result})

@app.route("/api/v1/plytoteka/<int:plytoteka_id>", methods = ["PUT"])
def update_plyta(plytoteka_id):
    plyta = plytoteka.get(plytoteka_id)
    if not plyta:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'artysta' in data and not isinstance(data.get('artysta'), str),
        'plyta' in data and not isinstance(data.get('plyta'), str),
        'rok_wydania' in data and not isinstance(data.get('rok_wydania'),int),
        'opis' in data and not isinstance(data.get('opis'), str),
        'w_kolekcji' in data and not isinstance(data.get('w_kolekcji'), bool)
    ]):
        abort(400)
    plyta = {
        'artysta': data.get('artysta', plyta['artysta']),
        'plyta': data.get('plyta', plyta['plyta']),
        'rok_wydania': data.get('rok_wydania', plyta['rok_wydania']),
        'opis': data.get('opis', plyta['opis']),
        'w_kolekcji': data.get('w_kolekcji', plyta['w_kolekcji'])
    }
    plytoteka.update(plytoteka_id, plyta)
    return jsonify({'plyta': plyta})

@app.route("/api/v1/plytoteka/<int:plytoteka_id>", methods=["GET"])
def get_plytoteka(plytoteka_id):
    plyta = plytoteka.get(plytoteka_id)
    if not plyta:
        abort(404)
    return jsonify({'plyta':plyta})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)