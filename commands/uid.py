async def uid(bot, data):
    tid = data.thread_id
    if not data.args and not data.reply:
        sender = data.author_id
        await bot.shareContact(f"{sender}", sender, tid)
    elif len(data.message_object.mentions) != 0:
        n = [x.thread_id for x in data.message_object.mentions]
        if len(n) == 1:
            k = await data.getName(n[0])
            return await bot.shareContact(f"{k}: {n[0]}", n[0], tid)
        m = list()
        for Id in n:
            v = await data.getName(Id)
            m.append(f"{v}: {Id}")
        await data.sendReply("\n".join(m))
    elif data.reply:
        sender = data.reply.author
        await bot.shareContact(f"{sender}", sender, tid)

config = {
    "name": 'uid',
    "def": uid,
    "usePrefix": False
}
