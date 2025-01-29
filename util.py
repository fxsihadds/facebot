import re
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel

user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"

# Console
class PrintBox:
  def __init__(self, title="Panel", border_style='white'):
    self.title = title
    self.border_style = border_style
  def message(self, message):
    Console().print(Panel(message, title=self.title, border_style=self.border_style))

# Text fonts
def font(type, text):
  real = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  def tae(fon, lis):
    output = ""
    for char in lis:
      if char not in list(real):
        output += char
      else:
        vh = real.index(char)
        output += fon[vh]
    return output
  match type:
    case 'bold':
      BOLD = "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
      return tae(BOLD, list(text))
    case 'mono':
      MONO = "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"
      return tae(MONO, list(text))
    case _:
      return text
def text_formatter(text):
  match = re.findall(r":(\w+)\[([^\]]+)\]", text)
  if len(match) < 1:
    return text
  else:
    output = text
    for TYPE, TEXT in match:
      prince_text = font(TYPE, TEXT)
      output = output.replace(f":{TYPE}[{TEXT}]", prince_text)
    return output

# upload image to imgbb
def upload_imgbb(data):
  KEY = "e58feb5f42f2cc77afd40a42e5f9747c"
  base_url = "https://api.imgbb.com/1/upload"
  params = {
    "name": 'greegmon',
    "key": KEY,
    "expiration": 1512000 # 25 weeks, remove this to set no expiration
  }
  data = {"image": data}
  try:
    res = requests.post(base_url,
      params=params,
      data=data,
      timeout=10
    )
    img = res.json()
    if img.get('success'):
      return {
        "image_url": img["data"]["url"],
        "width": img["data"]["width"],
        "height": img["data"]["height"]
      }
    return {
      "error": img["error"]["message"]
    }
  except Exception as e:
    print("\033[0;31mERROR: \033[0m", e)
    return {"error": 'Error while uploading the image'}

# get the link uid
def getUid(link):
  if not link.startswith('https://') or 'facebook.com' not in link:
    return {"error": 'Invalid link'}
  res = requests.get(link)
  if res.status_code == 200:
    pattern = r'(?<=fb://profile/)\d+'
    match = re.search(pattern, res.text)
    if match:
      return match.group(0)
  return {"error": 'Couldn\'t get the user id'}

# get the name
def getName(uid):
  try:
    response = requests.get(f"https://facebook.com/{uid}", headers={
      "User-Agent": 'Mozilla/5.0 (Windows; U; Windows NT 5.0; de-AT; rv:1.7.11) Gecko/20050728'
    })
    html = BeautifulSoup(response.text, 'html.parser')
    title = html.find('title').get_text().strip()
    if 'error' not in title.lower() and 'facebook' not in title.lower() and title != 'Facebook':
      name = title
    else:
      name = 'Facebook User'
    return name
  except Exception as e:
    print("\033[31mERROR: ", e)
    return 'Facebook User'