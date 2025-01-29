import requests
from bs4 import BeautifulSoup


user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"

# paste api
def paster(paste: str, exp: int|None = 1) -> dict:
  try:
    session = requests.Session()
    url = "https://pastebin.mozilla.org";
    
    headers = {
      "Content-Type": 'application/x-www-form-urlencoded',
      "User-Agent": user_agent,
      "Referer": url
    }
    data = {}
    
    res = session.get(url).content
    soup = BeautifulSoup(res, 'html.parser')
    form = soup.find('form')
    token = form.find('input', attrs={"name":"csrfmiddlewaretoken"}).get('value')
    
    data["csrfmiddlewaretoken"] = token
    data["title"] = ''
    data["lexer"] = '_text'
    data["expires"] = 86400*exp
    data["content"] = paste
    
    response = session.post(url, data=data, headers=headers)
    resHtml = BeautifulSoup(response.content, 'html.parser')
    
    ul = resHtml.find('ul',id="snippetOptions")
    resTitle = resHtml.find('title').getText()
    
    expire = ul.find('li',class_='option-type').getText().split('in: ')[1].strip()
    path = resTitle.split('Pastebin')[1].split(' ')[0]
    text = ul.find("textarea", id="copySnippetSource").getText()
    return {
      "path": '/paster' + path,
      "text": text,
      "expire": ' '.join(expire.split('\xa0'))
    }
  except Exception as e:
    print("Exception: ", e)
    return {"error": f"{e}"}