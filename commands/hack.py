from PIL import Image, ImageDraw, ImageFont
import requests

def Draw(profilePath, name="Facebook user", output='commands/cache/output.jpg'):
    try:
        base_image_path = 'commands/cache/hack.jpg'
        base_image = Image.open(base_image_path)
        
        draw = ImageDraw.Draw(base_image)
        
        font = ImageFont.truetype('commands/cache/font/Roboto.ttf', 35)
        draw.text((230, 585), name, fill=(30, 103, 204), font=font)
        
        overlay_image_path = profilePath
        overlay_image = Image.open(overlay_image_path)
        
        if overlay_image.mode != 'RGBA':
            overlay_image = overlay_image.convert('RGBA')
        
        overlay_image = overlay_image.resize((120, 120))
        
        position = (90, 544)
        base_image.paste(overlay_image, position, overlay_image)
        
        base_image.save(output)
        return output
    except Exception as error:
        print("\033[31mERROR: \033[0m", error)

async def Hack(bot, event):
    uid = event.author_id
    name = event.author_name
    if event.args:
        obj = event.message_object
        if len(obj.mentions) != 0:
            uid = obj.mentions[0].thread_id
            name = await event.getName(uid)
        else:
            if ' ' in event.args:
                return await obj.reply(f"Invalid usage, type '{bot.prefix}help hack' to see the usage")
            try:
                v = int(event.args)
                name = await event.getName(v)
                uid = v
            except ValueError:
                return await obj.reply(f"Invalid usage, type '{bot.prefix}help hack' to see the usage")
    elif event.reply:
        uid = event.reply.author
        name = await event.getName(uid)
    try:
        res = requests.get(f"https://graph.facebook.com/{uid}/picture?width=720&height=720&access_token=6628568379%7Cc1e620fa708a1d5696fb991c1bde5662")
        with open('commands/cache/profile.jpg', 'wb') as profile:
            profile.write(res.content)
        hacked = Draw('commands/cache/profile.jpg', name)
        if isinstance(hacked, tuple):
            bot.error(f"Error while drawing the hack image", 'hack.py')
        await bot.sendLocalFiles(
            hacked,
            f"Successfully hacked, the password has been sent to {'the owner' if uid == event.author_id else event.author_name}.",
            event.thread_id,
            event.thread_type
        )
    except Exception as e:
        await event.sendReply(f"{e}", True)
        bot.error(f"{e}", 'hack.py')

config = dict(
    name="hack",
    function=Hack,
    usage="{p}hack [<None>|<reply>|<mention>|<uid>]",
    author='Muhammad Greeg',
    usePrefix=False
)
