import re
from pyrogram import Client, filters
from pyrogram.types import Message
from BrandrdXMusic import app 
# Define the keywords that are commonly associated with pornographic content
porn_keywords = [
    "porn", "xxx", "sex", "nude", "boobs", "fuck", "pussy", "dick", "cum", "ass",
    "pornhub", "xvideos", "redtube", "brazzers"
]

# Regular expression pattern to match pornographic keywords
porn_pattern = re.compile("|".join(porn_keywords), re.IGNORECASE)



# Function to check for pornographic content in messages
def is_pornographic(message: Message) -> bool:
    if message.text and porn_pattern.search(message.text):
        return True
    if message.caption and porn_pattern.search(message.caption):
        return True
    if message.sticker and porn_pattern.search(message.sticker.emoji):
        return True
    if message.animation and porn_pattern.search(message.animation.file_name):
        return True
    if message.photo and message.photo.file_name and porn_pattern.search(message.photo.file_name):
        return True
    return False

# Handler to delete messages with pornographic content
@app.on_message(filters.group)
def delete_pornographic_messages(client, message: Message):
    if is_pornographic(message):
        message.delete()
        print(f"Deleted message: {message.text or message.caption}")
