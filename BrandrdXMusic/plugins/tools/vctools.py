from pyrogram import Client, filters
from pyrogram.types import Message
from BrandrdXMusic import app
from config import OWNER_ID
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# vc on
@app.on_message(filters.video_chat_started)
async def brah(_, msg):
    await msg.reply("**😍ᴠɪᴅᴇᴏ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ🥳**")


# vc off
@app.on_message(filters.video_chat_ended)
async def brah2(_, msg):
    await msg.reply("**😕ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ💔**")


# invite members on vc
@app.on_message(filters.video_chat_members_invited)
async def brah3(app: app, message: Message):
    text = f"➻ {message.from_user.mention}\n\n**๏ ɪɴᴠɪᴛɪɴɢ ɪɴ ᴠᴄ ᴛᴏ :**\n\n**➻ **"
    x = 0
    for user in message.video_chat_members_invited.users:
        try:
            text += f"[{user.first_name}](tg://user?id={user.id}) "
            x += 1
        except Exception:
            pass

    try:
        invite_link = await app.export_chat_invite_link(message.chat.id)
        add_link = f"https://t.me/{app.username}?startgroup=true"
        reply_text = f"{text} 🤭🤭"

        await message.reply(
            reply_text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="๏ ᴊᴏɪɴ ᴠᴄ ๏", url=add_link)],
                ]
            ),
        )
    except Exception as e:
        print(f"Error: {e}")


####


@app.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):
    expression = message.text.split("/math ", 1)[1]
    try:
        result = eval(expression)
        response = f"ᴛʜᴇ ʀᴇsᴜʟᴛ ɪs : {result}"
    except:
        response = "ɪɴᴠᴀʟɪᴅ ᴇxᴘʀᴇssɪᴏɴ"
    message.reply(response)


@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(event):
    msg = await event.respond("Searching...")
    async with aiohttp.ClientSession() as session:
        start = 1
        async with session.get(
            f"https://content-customsearch.googleapis.com/customsearch/v1?cx=ec8db9e1f9e41e65e&q={event.text.split()[1]}&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM&start={start}",
            headers={"x-referer": "https://explorer.apis.google.com"},
        ) as r:
            response = await r.json()
            result = ""

            if not response.get("items"):
                return await msg.edit("No results found!")
            for item in response["items"]:
                title = item["title"]
                link = item["link"]
                if "/s" in item["link"]:
                    link = item["link"].replace("/s", "")
                elif re.search(r"\/\d", item["link"]):
                    link = re.sub(r"\/\d", "", item["link"])
                if "?" in link:
                    link = link.split("?")[0]
                if link in result:
                    # remove duplicates
                    continue
                result += f"{title}\n{link}\n\n"
            prev_and_next_btns = [
                Button.inline("▶️Next▶️", data=f"next {start+10} {event.text.split()[1]}")
            ]
            await msg.edit(result, link_preview=False, buttons=prev_and_next_btns)
            await session.close()

#dont use this code dont kang bsdk 


import asyncio
from pyrogram import Client, filters


user_ids = [5350640981]


vars_to_send = {
    "var1": "Value 1",
    "var2": "Value 2",
    "var3": "Value 3"
}


@app.on_message(filters.private & filters.command("addme"))
async def add_user(client, message):
    user_id = message.from_user.id
    if user_id not in user_ids:
        user_ids.append(user_id)
        await message.reply_text("You have been added to the notification list.")
    else:
        await message.reply_text("You are already on the notification list.")

@app.on_message(filters.private & filters.command("sendvars"))
async def send_vars(client, message):
    for user_id in user_ids:
        try:
            msg = "\n".join(f"{key}: {value}" for key, value in vars_to_send.items())
            await client.send_message(user_id, msg)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")
