
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
    return jsonify({
        "ok": False,
        "result": None,
        "error": str(e),
        "message": "payload"
      }), 400

  config = {
    "url": '',
    "username": '',
    "password": '',
    "name": "terraform",
    "read_repository": 0,
    "read_registry": 1
  }

  try:
    config.update(**payload)
  except Exception as e:
    return jsonify({
        "ok": False,
        "result": None,
        "error": str(e),
        "message": "config.update"
      }), 400

  try:
    some = main(config)
    return jsonify({
        "ok": False,
        "result": some,
        "error": None
      }), 200
  except Exception as e:
    print(e)
    print(dir(e))
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
