import json
import base64
import os
from markdown2 import Markdown
from flask import Flask, jsonify, request, abort
from create_deploy_token import *


app = Flask(__name__)

@app.route('/', methods = ["GET"])
def ok():
  with open('README.md') as f:
    return '<html>' + Markdown().convert(f.read()) + '</html>'

@app.route('/', methods = ["POST"])
def proceed():
  try:
    payload = request.get_json(force=True)
  except Exception as e:
    print(e)
    return jsonify({
        "ok": False,
        "result": None,
        "error": str(e),
#         "message": "payload"
      }), 400

  config = {
    "url": '',
    "username": '',
    "password": '',
    "name": "terraform",
    "read_repository": 0,
    "read_registry": 1,
    "server": ""
  }

  try:
    config.update(**payload)
  except Exception as e:
    print(e)
    return jsonify({
        "ok": False,
        "result": None,
        "error": str(e),
#         "message": "config.update"
      }), 400

  try:
    result = main(config)
    if config["server"]:
      result["dockerconfigjson"] = base64.b64encode(json.dumps({
        "auths":{
          config["server"]:{
            "username": result["username"],
            "password": result["token"],
#             "auth": base64.b64encode(
#               "{}:{}".format(
#                 result["username"],
#                 result["token"]
#               ).encode()
#             ).decode()
          }
        }
      }, default=str).encode()).decode()
    return jsonify({
        "ok": True,
        "result": result,
        "error": None
      }), 200
  except Exception as e:
#     print(e)
#     print(dir(e))
    return jsonify({
        "ok": False,
        "result": None,
        "error": str(e)
      }), 500


if __name__ == '__main__':
  app.run(
    debug = True,
    host = '0.0.0.0',
    port = os.environ.get('PORT', '8080')
  )
