import random
from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont
from BrandrdXMusic import app

def generate_ai_dp(name):
    # Create an image with a plain background
    width, height = 512, 512
    image = Image.new('RGB', (width, height), color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    # Draw the name in the center of the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 80)  # Adjust the font size and style as needed
    text_width, text_height = draw.textsize(name, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, name, (255, 255, 255), font=font)

    # Save the image to a file
    image_path = f"{name}_dp.png"
    image.save(image_path)
    
    return image_path

@app.on_message(filters.command("aidp"))
def aidp_handler(client, message):
    if len(message.command) < 2:
        message.reply_text("Please provide a name. Usage: /aidp [name]")
        return

    name = message.command[1]
    image_path = generate_ai_dp(name)
    
    message.reply_photo(photo=image_path, caption=f"Here is your AI DP for {name}!")

@app.on_message(filters.command("search"))
def search_handler(client, message):
    if len(message.command) < 2:
        message.reply_text("Please provide a name. Usage: /search [name]")
        return
    
    name = message.command[1]
    # For simplicity, we just reply with a message here.
    # You can add actual search functionality as needed.
    message.reply_text(f"Searching for information about {name}...")
