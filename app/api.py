import json
import importlib
from flask import (
  Blueprint,
  render_template,
  redirect,
  url_for,
  request,
  jsonify
)
from .function import (
  paster
)

api = Blueprint('api',__name__)
restarter = None
def ogag(v):
  global restarter
  restarter = v

@api.route('/bobot', methods=['POST'])
def bobot():
  fbstate = request.form.get('fbstate')
  if fbstate:
    json_fbstate = json.loads(fbstate)
    with open('fbstate.json', 'w') as file:
      json.dump(json_fbstate, file, indent=2)
    if restarter:
      restarter()
  return redirect(url_for('view.root'))

# Paster, like pastebin
@api.route('paster', methods=['POST'])
def api_paster():
  data = request.json
  text = data.get('text')
  if not text:
    return jsonify({"error": "Bobo mag lagay ka ng text"}),403
  response = paster(text, 7)
  status = 200 if 'error' not in response else 500
  response['host'] = request.headers['Host']
  return jsonify(response), status