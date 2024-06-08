import os
from pyrogram import Client, filters
from instaloader import Instaloader, Post
from pyrogram.types import Message
from BrandrdXMusic import app
# Initialize Instaloader
L = Instaloader()




@app.on_message(filters.private & filters.text)
async def handle_instagram_link(client, message):
    text = message.text
    if "instagram.com" in text:
        await message.reply_text("Downloading the video from Instagram...")
        try:
            shortcode = text.split("/")[-2] if text.endswith("/") else text.split("/")[-1]
            post = Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target="downloads")
            
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
        # Only reply if the message does not contain an Instagram link
        if "instagram.com" not in text:
            return


