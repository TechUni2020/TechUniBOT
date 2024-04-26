import os
from flask import Blueprint, request, jsonify
from techuni_object import JoinApplication

app = Blueprint('app', __name__)

with open(os.environ.get("gas_signkey_file"), mode="r") as f:
    secretKey = "".join([k.rstrip("\n") for k in f.readlines()])

@app.route('/join_application',methods=['POST'])
def receive_join_application():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(res='content-type error'), 400

    data: dict = request.json
    try:
        application: JoinApplication = JoinApplication.from_webhook(data, secretKey)
    except ValueError:
        return jsonify(res='invalid sign'), 400

    # apply

    return jsonify(res='ok')

@app.route('/test',methods=['GET'])
def test():
    return jsonify(res=f'ok {secretKey[:10]}')
