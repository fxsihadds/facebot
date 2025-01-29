import yt_dlp
import os
import json

async def function(bot, event):
    if not event.args:
        return await event.sendReply(
            event.font(":mono[Please provide a Youtube video URL.]")
        )
    # get link from users
    url = event.args

    loading = await bot.sendMessage(
        event.font(":mono[Downloading Youtube Video, please wait...]"),
        event.thread_id,
        event.thread_type,
    )

    try:
        path = await download_video_as_mp3(url, bot, event)
        print(path)
        await bot.sendLocalFiles(
            path,
            thread_id=event.thread_id,
            thread_type=event.thread_type,
        )
        await bot.unsend(loading)
        os.remove(path)

    except Exception as e:
        print(f"\033[91m[ERROR] \033[0m{e}")
        await event.sendReply(event.font(f":mono[ভাই আমাকে কম করেন, আমার ডুলা ছোট {e}]"))
        os.remove(path)


async def download_video_as_mp3(url, bot, event):
    output_dir = "facebot/commands/cache"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "cookiefile": r"commands/cache/cookies.txt",
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return os.path.join(output_dir, os.listdir(output_dir)[0])


config = {
    "name": "ytmp3",
    "def": function,
    "author": "Sihad",
    "usage": "{p}YT [Youtube URL]",
    "description": "Download Youtube MP3",
    "usePrefix": True,
}
