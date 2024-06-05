import random
import io
from PIL import Image, ImageDraw, ImageFont
import requests
from pyrogram import Client, filters

# List of romantic shayari
romantic_shayari = [
    "तेरे प्यार का कितना खूबसूरत एहसास है, दूर होकर भी लगता है जैसे तू हर पल मेरे पास है।",
    "धड़कनों को कुछ तो काबू में कर ए दिल, अभी तो पलकें झुकाई हैं मुस्कुराना बाकी है उनका।",
    "तुम्हारी यादों में हमें इस कदर प्यार है, हर वक्त हर पल तुम ही हमारे दिल के करीब हो।"
]

# List of general shayari
general_shayari = [
    "ज़िंदगी से बस इतना ही ताल्लुक है मेरा, किसी और को चाहने की गुंजाइश नहीं रहती।",
    "हमसे किसी ने प्यार से देखा भी नहीं है, और हम हैं कि तेरे दीदार की ख्वाहिश लिए बैठे हैं।",
    "हर किसी का प्यार कभी मुकम्मल नहीं होता, किसी को मिल जाता है और किसी का इंतजार रह जाता है।"
]

def create_thumbnail(user_name, shayari):
    # Load a base image or create an empty one
    base_image = Image.new('RGB', (800, 400), (255, 255, 255))

    # Load YouTube-style circle PNG
    circle_url = "URL_TO_YOUR_CIRCLE_PNG"
    circle_img = Image.open(requests.get(circle_url, stream=True).raw).convert("RGBA")

    # Resize and paste the circle image
    circle_img = circle_img.resize((100, 100), Image.ANTIALIAS)
    base_image.paste(circle_img, (350, 150), circle_img)

    # Load user profile image
    user_img_url = "URL_TO_USER_IMAGE"
    user_img = Image.open(requests.get(user_img_url, stream=True).raw).convert("RGBA")

    # Resize user image and make it circular
    user_img = user_img.resize((90, 90), Image.ANTIALIAS)
    mask = Image.new('L', user_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + user_img.size, fill=255)
    user_img.putalpha(mask)
    base_image.paste(user_img, (355, 155), user_img)

    # Draw the shayari text
    draw = ImageDraw.Draw(base_image)
    font = ImageFont.truetype("arial.ttf", 20)
    text_x, text_y = 20, 20
    draw.text((text_x, text_y), shayari, fill="black", font=font)

    # Draw the username
    username_font = ImageFont.truetype("arial.ttf", 20)
    draw.text((20, 350), f"Requested by: {user_name}", fill="black", font=username_font)

    # Save to a bytes object
    img_byte_arr = io.BytesIO()
    base_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr

@app.on_message(filters.command("sshayri"))
async def shayari(client, message):
    user = message.from_user.mention
    shayari_type = random.choice(["romantic", "general"])
    
    if shayari_type == "romantic":
        shayari = random.choice(romantic_shayari)
    else:
        shayari = random.choice(general_shayari)
    
    thumbnail = create_thumbnail(user, shayari)
    await message.reply_photo(photo=thumbnail, caption=f"{shayari}\n\n- {user}")


