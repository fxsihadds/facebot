async def function(bot, event):
  if event.args:
    return await event.sendReply("This command don't need an arguments")
  bot.reload_modules()
  await event.sendReply("Modules reloaded.")

config = dict(
  name = "reload",
  author = "Christopher",
  function = function,
  adminOnly = True
)