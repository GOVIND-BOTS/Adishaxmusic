import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from BrandrdXMusic import app 

@app.on_message(filters.private & filters.text)
async def handle_instagram_link(client, message):
    text = message.text
    if "instagram.com" in text:
        await message.reply_text("Downloading the video from Instagram...")
        try:
            # Use a public Instagram video download API
            api_url = "https://api.instagramdownloader.io/download"
            response = requests.get(api_url, params={"url": text})

            if response.status_code == 200:
                json_response = response.json()
                video_url = json_response.get("video_url")

                if video_url:
                    video_response = requests.get(video_url)
                    video_path = os.path.join("downloads", "video.mp4")

                    with open(video_path, "wb") as file:
                        file.write(video_response.content)

                    await client.send_video(
                        chat_id=message.chat.id,
                        video=video_path,
                        caption="Here is your video!"
                    )

                    os.remove(video_path)
                else:
                    await message.reply_text("No video found at the provided link.")
            else:
                await message.reply_text("Failed to retrieve video. Please try again later.")

        except Exception as e:
            await message.reply_text(f"An error occurred: {e}")
    else:
        # Only reply if the message does not contain an Instagram link
        if "instagram.com" not in text:
            return




