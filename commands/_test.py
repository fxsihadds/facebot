import requests

async def Run(bot, event):
  message = "Hahhahahhaha"
  res = requests.post('http://localhost:5000/api/paster', json={"text": message})
  data = res.json()
  await event.sendReply(f"Expired: {data.get('expire')}\nLink: {data['host']}{data['path']}")
  
config = dict(
  name = "test",
  function = Run,
  adminOnly = True
)