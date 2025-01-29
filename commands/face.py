import requests
import re
import os
import shutil


async def function(bot, event):
    if not event.args:
        return await event.sendReply(
            event.font(":mono[Please provide a TikTok video URL.]")
        )
    # Get the TikTok URL from the user's message
    url = event.args

    loading = await bot.sendMessage(
        event.font(":mono[Downloading TikTok video, please wait...]"),
        event.thread_id,
        event.thread_type,
    )

    try:
        await tiktok(url, bot, event)
        await bot.sendLocalFiles(
            "commands/cache/video.mp4",
            thread_id=event.thread_id,
            thread_type=event.thread_type,
        )
        await bot.unsend(loading)
        os.remove("commands/cache/video.mp4")

    except Exception as e:
        print(f"\033[91m[ERROR] \033[0m{e}")
        await event.sendReply(event.font(f":mono[ভাই আমাকে কম করেন, আমার ডুলা ছোট{e}]"))


async def tiktok(url: str, bot, event):
    # URL and payload
    data_url = "https://snap-insta.app/wp-json/visolix/api/download"
    payload = {"url": url, "format": "", "captcha_response": None}

    # Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
    }

    try:
        response = requests.post(data_url, json=payload, headers=headers)
        if response.status_code == 200:
            html_content = response.json()["data"]

            # Regular expression to find the HD download link ID
            match = re.search(
                r'href="https:\/\/snap-insta\.app\/wp-content\/plugins\/visolix-video-downloader\/includes\/\.\.\/dl\.php\?id=([a-f0-9]+)"',
                html_content,
            )
            if match:
                hd_download_id = match.group(1)
                download_url = f"https://snap-insta.app/wp-content/plugins/visolix-video-downloader/dl.php?id={hd_download_id}&countdown=0"
                file_path = os.path.join("commands/cache", "video.mp4")

                # Download the video
                response = requests.get(download_url)
                if response.status_code == 200:
                    with open(file_path, "wb") as file:
                        file.write(response.content)
                    print(f"Download successful! File saved to {file_path}")
                else:
                    print(f"Failed to download. Status code: {response.status_code}")
            else:
                await bot.sendMessage(
                    event.font(
                        ":mono[ বালের লিংক দেও, তোমার প্রেমিকার লিংক দিতে পারো না।]"
                    ),
                    event.thread_id,
                    event.thread_type,
                )
        else:
            print(f"Failed with status code {response.status_code}")
            print("Response text:", response.text)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


config = {
    "name": "dlTk",
    "def": function,
    "author": "Sihad",
    "usage": "{p}tk [TikTok URL]",
    "description": "Download TikTok Video",
    "usePrefix": True,
}
