from pyrogram import Client, filters
from pymongo import MongoClient
import random
from BrandrdXMusic import app as bot

# Fetch bot username
async def get_bot_username():
    async with bot:
        bot_info = await bot.get_me()
        return bot_info.username

# Handler for turning the chatbot off
@bot.on_message(
    filters.command(["chatbot off", f"chatbot@{await get_bot_username()} off"], prefixes=["/", ".", "?", "-"])
    & ~filters.private)
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
        await message.reply_text("Chatbot Disabled!")
    else:
        await message.reply_text("ChatBot Already Disabled")

# Handler for turning the chatbot on
@bot.on_message(
    filters.command(["chatbot on", f"chatbot@{await get_bot_username()} on"], prefixes=["/", ".", "?", "-"])
    & ~filters.private)
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
        await message.reply_text("Chatbot Already Enabled")
    else:
        vick.delete_one({"chat_id": message.chat.id})
        await message.reply_text("ChatBot Enabled!")

# Handler for showing chatbot usage
@bot.on_message(
    filters.command(["chatbot", f"chatbot@{await get_bot_username()}"], prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatbot_usage(client, message):
    await message.reply_text("**Usage:**\n/**chatbot [on/off]**\n**Chat-bot commands work in group only!**")

# General handler for messages in groups
@bot.on_message(
    (filters.text | filters.sticker)
    & ~filters.private
    & ~filters.bot)
async def group_message_handler(client, message):
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]
    vickdb = MongoClient(MONGO_URL)
    vick = vickdb["VickDb"]["Vick"]
    is_vick = vick.find_one({"chat_id": message.chat.id})

    if not is_vick:
        await client.send_chat_action(message.chat.id, "typing")
        if not message.reply_to_message:
            process_message(chatai, message)
        else:
            await process_reply(chatai, message, bot)

# Function to process a message
async def process_message(chatai, message):
    K = []
    is_chat = chatai.find({"word": message.text})
    k = chatai.find_one({"word": message.text})
    if k:
        for x in is_chat:
            K.append(x['text'])
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
        K = []
        is_chat = chatai.find({"word": message.text})
        k = chatai.find_one({"word": message.text})
        if k:
            for x in is_chat:
                K.append(x['text'])
            hey = random.choice(K)
            is_text = chatai.find_one({"text": hey})
            Yo = is_text['check']
            if Yo == "sticker":
                await message.reply_sticker(hey)
            else:
                await message.reply_text(hey)
    else:
        if message.sticker:
            is_chat = chatai.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
            if not is_chat:
                chatai.insert_one({"word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
        if message.text:
            is_chat = chatai.find_one({"word": message.reply_to_message.text, "text": message.text})
            if not is_chat:
                chatai.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})

# Handler for messages in private chats
@bot.on_message(
    (filters.text | filters.sticker)
    & filters.private
    & ~filters.bot)
async def private_message_handler(client, message):
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]
    await client.send_chat_action(message.chat.id, "typing")
    if not message.reply_to_message:
        process_message(chatai, message)
    else:
        await process_reply(chatai, message, bot)

# Function to check if a user is an admin
async def is_admins(chat_id):
    return [admin.user.id for admin in await bot.get_chat_members(chat_id, filter="administrators")]


