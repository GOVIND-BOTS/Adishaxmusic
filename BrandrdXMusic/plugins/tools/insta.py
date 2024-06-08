#loda lelo😁😀

import os
from pyrogram import Client, filters
from BrandrdXMusic import app
from pyrogram.types import Message
import asyncio
from bs4 import BeautifulSoup

L = instaloader.Instaloader()

@app.on_message(filters.private & filters.text)
async def handle_instagram_link(client, message):
    text = message.text
    if "instagram.com" in text:
        await message.reply_text("Downloading the video from Instagram...")
        try:
            L.download_post(instaloader.Post.from_shortcode(L.context, text.split("/")[-2]), target="downloads")
            video_file = next(file for file in os.listdir("downloads") if file.endswith(".mp4"))
            video_path = os.path.join("downloads", video_file)

            await client.send_video(
                chat_id=message.chat.id,
                video=video_path,
                caption="Here is your video!"
            )

            os.remove(video_path)
        except Exception as e:
            await message.reply_text(f"An error occurred: {e}")
    else:
        await message.reply_text("Please send a valid Instagram video link.")
