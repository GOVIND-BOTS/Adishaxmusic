from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
BrandrdXMusic import app 

# Welcome new members
@app.on_message(filters.new_chat_members)
def welcome(client, message: Message):
    for member in message.new_chat_members:
        message.reply_text(f"Welcome {member.mention} to the group!")

# Respond to messages
@app.on_message(filters.text & filters.group)
def group_message(client, message: Message):
    if message.text.lower() == "hello":
        message.reply_text("Hello! How can I help you?")
    elif message.text.lower() == "help":
        message.reply_text("Sure, what do you need help with?")
