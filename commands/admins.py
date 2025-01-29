from database import User

async def Run(bot, event):
  if event.args:
    return await event.sendReply("This command don't need an arguments")
  admins = []
  for uid in bot.admin:
    name = await event.getName(uid)
    if name == 'Facebook User':
      bot.error(f"Couldn't fetch user info - [red]{uid}[/red]", "admins.py")
    admins.append((uid, name))
  
  message = ":bold[BOT ADMIN] ⩇⩇:⩇⩇\n\n"
  for uid, name in admins:
    message += f":bold[NAME]: {name}\n"
    message += f":bold[UID]: {uid}\n"
    message += f"🔗 ⟩⟩ https://facebook.com/{uid}\n\n"
  
  await event.sendReply(message, True)

config = dict(
  name = "admins",
  function = Run,
  author = "Christopher",
  usage = "{p}admins",
  description = "list of bot admins"
)