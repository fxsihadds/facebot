import random
from database import User

def roll_color():
  colors = ["🟨","🟦","🟩","🟥","⬜","🟪"]
  c1,c2,c3 = [random.choice(colors) for i in range(3)]
  it = "".join([c1,c2,c3])
  if c1 == c2 == c3:
    return (3, it)
  elif c1 == c2 or c1 == c3 or c2 == c3:
    return (2, it)
  else:
    return (1, it)

async def Func(bot, event):
  args = event.args
  if not args:
    return await event.sendReply("Missing amount of money to bet")
  elif ' ' in args or not args.isalnum():
    return await event.sendReply(f"Invalid value, type '{bot.prefix}help colorgame' to see the usage")
  try:
    amount = int(args)
    user = User(event.author_id)
    if amount > user.money:
      return await event.sendReply("You don't have enough money")
    toTimes, result = roll_color()
    await event.sendReply(f":bold[COLOR GAME]\n{event.line}\n[|{result}|]", True)
    if toTimes == 1:
      now_money = user.subMoney(amount)
      return await event.sendReply(f"You lost {amount}, your now balance is {now_money}")
    elif toTimes == 2:
      now_money = user.addMoney(amount)
      return await event.sendReply(f"The result has 2 same colors, your bet will be double. Your now balance is {now_money}")
    else:
      now_money = user.addMoney(amount*2)
      return await event.sendReply(f"The result has 3 same colors, your bet will be triple. Your now balance is {now_money}")
  except ValueError:
    return await event.sendReply(f"Invalid value, type '{bot.prefix}help colorgame' to see the usage")

config = dict(
  name = "colorgame",
  function = Func,
  author = "Christopher",
  usage = "{p}colorgame [bet money]",
  description = "Play color game and win a momey"
)