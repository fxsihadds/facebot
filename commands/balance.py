from database import User

async def function(bot, event):
  if event.args:
    return await event.sendReply(":mono[This command dont need a parameter]",True)
  user = User(event.author_id)
  return await event.sendReply(f":bold[Balance:] {user.money}",True)

config = {
  "name": 'balance',
  "def": function,
  "author": 'Muhammad Greegmon',
  "description": "Get the current money balance",
  "usage": '{p}bal',
  "usePrefix": False
}