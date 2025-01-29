async def function(bot, data):
    message = data.get("message") or ""
    tid = data.get("thread_id")
    typ = data.get("thread_type")
    mid = data.get("mid")

    def check(text):
        return True if text in message.lower() else False

    if check("junmar"):
        return await bot.sendMessage("Junmar is a fool!!", tid, typ, reply_to_id=mid)
    elif check("greegmon") or check(" greeg "):
        return await bot.sendMessage(
            "There is Majnun, still being silly", tid, typ, reply_to_id=mid
        )
    elif check("prince har"):
        return await bot.sendMessage(
            "No need for Facebook chat application programming interface.",
            tid,
            typ,
            reply_to_id=mid,
        )


config = {"event": "type:messaging", "def": function, "author": "Muhammad Greeg"}
