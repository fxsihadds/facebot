import requests
import datos
from bs4 import BeautifulSoup
from flask import (
  Blueprint,
  render_template,
  request
)

view = Blueprint('view',__name__)

@view.route('/')
def root():
  return render_template('home.html', title="Update BOT", bot=datos.BOT),200

@view.route('/paster/<path>')
def paster(path):
  res = requests.get(f"https://pastebin.mozilla.org/{path}/raw")
  soup = BeautifulSoup(res.content, 'html.parser')
  val = res.text
  try:
    if soup.find('title').text == "404 Snippet not found":
      val = "Paste not found"
  except Exception as e:
    val = f"{e}"
  finally:
    return render_template('paster.html', text=val, title=f"/paster/{path}"),200