import asyncio
import random
from pyrogram import Client, filters
from pymongo import MongoClient
from typing import List

# Import modules from your project
from BrandrdXMusic import app as bot
from config import MONGO_DB_URI, SUPPORT_CHAT, adminlist, confirmer
from BrandrdXMusic.utils.database import (
    get_authuser_names,
    get_cmode,
    get_lang,
    get_upvote_count,
    is_active_chat,
    is_maintenance,
    is_nonadmin_chat,
    is_skipmode,
)
from strings import get_string

# Initialize MongoDB client and database
mongo = MongoClient(MONGO_DB_URI)
db = mongo.BrandrdXMusic

# Function to check if a user is an admin
async def is_admins(chat_id):
    try:
        return [admin.user.id for admin in await bot.get_chat_members(chat_id, filter="administrators")]
    except Exception:
        return []

# Function to process a message
async def process_message(chatai, message):
    is_chat = chatai.find({"word": message.text})
    if is_chat.count() > 0:
        K = [x['text'] for x in is_chat]
        hey = random.choice(K)
        is_text = chatai.find_one({"text": hey})
        Yo = is_text['check']
        if Yo == "sticker":
            await message.reply_sticker(hey)
        else:
            await message.reply_text(hey)

# Function to process a reply
async def process_reply(chatai, message, bot):
    getme = await bot.get_me()
    bot_id = getme.id
    if message.reply_to_message.from_user.id == bot_id:
        await process_message(chatai, message)
    else:
        if message.sticker:
            is_chat = chatai.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
            if not is_chat:
                chatai.insert_one({
                    "word": message.reply_to_message.text, 
                    "text": message.sticker.file_id, 
                    "check": "sticker", 
                    "id": message.sticker.file_unique_id
                })
        if message.text:
            is_chat = chatai.find_one({"word": message.reply_to_message.text, "text": message.text})
            if not is_chat:
                chatai.insert_one({
                    "word": message.reply_to_message.text, 
                    "text": message.text, 
                    "check": "none"
                })

# Fetch bot username before defining handlers
async def get_bot_username(client):
    async with client:
        bot_info = await client.get_me()
        return bot_info.username

async def main():
    bot_username = await get_bot_username(bot)

    # MongoDB collections
    vick_collection = db[".couple"]
    chatdb = mongo["Word"]["WordDb"]

    @bot.on_message(
        filters.command(["chatbot off", f"chatbot@{bot_username} off"], prefixes=["/", ".", "?", "-"])
        & ~filters.private)
    async def chatbot_off(client, message):
        if message.from_user:
            user = message.from_user.id
            chat_id = message.chat.id
            if user not in (await is_admins(chat_id)):
                return await message.reply_text("You are not admin")
        is_vick = vick_collection.find_one({"chat_id": message.chat.id})
        if not is_vick:
            vick_collection.insert_one({"chat_id": message.chat.id})
            await message.reply_text("Chatbot Disabled!")
        else:
            await message.reply_text("ChatBot Already Disabled")

    @bot.on_message(
        filters.command(["chatbot on", f"chatbot@{bot_username} on"], prefixes=["/", ".", "?", "-"])
        & ~filters.private)
    async def chatbot_on(client, message):
        if message.from_user:
            user = message.from_user.id
            chat_id = message.chat.id
            if user not in (await is_admins(chat_id)):
                return await message.reply_text("You are not admin")
        is_vick = vick_collection.find_one({"chat_id": message.chat.id})
        if not is_vick:
            await message.reply_text("Chatbot Already Enabled")
        else:
            vick_collection.delete_one({"chat_id": message.chat.id})
            await message.reply_text("ChatBot Enabled!")

    @bot.on_message(
        filters.command(["chatbot", f"chatbot@{bot_username}"], prefixes=["/", ".", "?", "-"])
        & ~filters.private)
    async def chatbot_usage(client, message):
        await message.reply_text("**Usage:**\n/**chatbot [on/off]**\n**Chat-bot commands work in group only!**")

    @bot.on_message(
        (filters.text | filters.sticker)
        & ~filters.private
        & ~filters.bot)
    async def group_message_handler(client, message):
        is_vick = vick_collection.find_one({"chat_id": message.chat.id})
        if not is_vick:
            await client.send_chat_action(message.chat.id, "typing")
            if not message.reply_to_message:
                await process_message(chatdb, message)
            else:
                await process_reply(chatdb, message, bot)

    @bot.on_message(
        (filters.text | filters.sticker)
        & filters.private
        & ~filters.bot)
    async def private_message_handler(client, message):
        await client.send_chat_action(message.chat.id, "typing")
        if not message.reply_to_message:
            await process_message(chatdb, message)
        else:
            await process_reply(chatdb, message, bot)

    await bot.start()

# Run the main function to start the bot
asyncio.run(main())
