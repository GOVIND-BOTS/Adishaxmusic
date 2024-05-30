from pyrogram import Client, filters
from pymongo import MongoClient
import random





@app.on_message(
    filters.command(["chatbot off", f"chatbot@{app.username} off"], prefixes=["/", ".", "?", "-"])
    & ~filters.private
)
async def chatbot_off(client, message):
    vickdb = MongoClient(MONGO_URL)
    vick = vickdb["VickDb"]["Vick"]
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (await is_admins(chat_id)):
            return await message.reply_text("You are not admin")
    is_vick = vick.find_one({"chat_id": message.chat.id})
    if not is_vick:
        vick.insert_one({"chat_id": message.chat.id})
        await message.reply_text(f"Chatbot Disabled!")
    else:
        await message.reply_text(f"ChatBot Already Disabled")

@app.on_message(
    filters.command(["chatbot on", f"chatbot@{app.username} on"], prefixes=["/", ".", "?", "-"])
    & ~filters.private
)
async def chatbot_on(client, message):
    vickdb = MongoClient(MONGO_URL)
    vick = vickdb["VickDb"]["Vick"]
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (await is_admins(chat_id)):
            return await message.reply_text("You are not admin")
    is_vick = vick.find_one({"chat_id": message.chat.id})
    if not is_vick:
        await message.reply_text(f"Chatbot Already Enabled")
    else:
        vick.delete_one({"chat_id": message.chat.id})
        await message.reply_text(f"ChatBot Enabled!")

@app.on_message(
    filters.command(["chatbot", f"chatbot@{app.username}"], prefixes=["/", ".", "?", "-"])
    & ~filters.private
)
async def chatbot(client, message):
    await message.reply_text("**ᴜsᴀɢᴇ:**\n/**chatbot [on/off]**\n**ᴄʜᴀᴛ-ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅ(s) ᴡᴏʀᴋ ɪɴ ɢʀᴏᴜᴘ ᴏɴʟʏ!**")

# Define other functions and handlers


