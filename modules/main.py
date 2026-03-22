import os
import re
import sys
import json
import time
import asyncio
import threading
import random
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper
import m3u8
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS, WEBHOOK, PORT
import MSdatabase as db
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from flask import Flask
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# Inline keyboard for start command
BUTTONSCONTACT = InlineKeyboardMarkup([[InlineKeyboardButton(text="🔎Developer", url="https://t.me/SmartBoy_ApnaMS")]])
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="🛠️ Channel", url="https://t.me/Toxic_Official_1"),
            InlineKeyboardButton(text="👑 Owner", url="https://t.me/MR_Toxic_1"),
        ],
    ]
)

my_name = "MS"

# ── Random image list (add/remove URLs freely) ────────────────────────────────
image_list = [
    "https://graph.org/file/a7defa3fc5af14e1ef64d-6aaf13e93fca95cfb2.jpg",
    "https://graph.org/file/0477971c295c3ece935ef-2af948bd4f14c6d1da.jpg",
    "https://graph.org/file/9664850ce3c6ebaa5007e-e812fa25118aa1a1d7.jpg",
    "https://graph.org/file/b7466fa9700260aab4f77-a48f2b54d2f8328112.jpg",
    "https://graph.org/file/2eb3c7ed975b9f9dffaa5-9b991b04b9478b1026.jpg",
    "https://graph.org/file/e5cbc501850bf1c4351f6-2e913a534c92f5f5f8.jpg",
    "https://graph.org/file/b48abf3696926fd6f36b3-9e1be53031a43a444d.jpg",
]
# ─────────────────────────────────────────────────────────────────────────────

cookies_file_path = os.getenv("COOKIES_FILE_PATH", "/modules/youtube_cookies.txt")

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    # Start the bot
    await start_bot()

    # Keep the program running until interrupted
    try:
        await asyncio.Event().wait()
    except Exception:
        await stop_bot()
        
class Data:
    START = (
        "🌟 Welcome Dear🤝 {0}! 🌟\n\n"
    )

# Inline keyboards for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="🛠️ Channel", url="https://t.me/Toxic_Official_1"),
            InlineKeyboardButton(text="👑 Owner", url="https://t.me/MR_Toxic_1"),
        ],
        [
            InlineKeyboardButton(text="🔎 Developer", url="https://t.me/SmartBoy_ApnaMS"),
        ],
    ]
)


# ── Credit name href parser ────────────────────────────────────────────────────
# Supports: "Text|https://url" → "[Text](https://url)" (Telegram markdown link)
# Normal text with no "|" passes through unchanged.
def parse_credit(raw: str) -> str:
    if "|" in raw:
        parts = raw.split("|", 1)
        text = parts[0].strip()
        url  = parts[1].strip()
        return f"[{text}]({url})"
    return raw
# ─────────────────────────────────────────────────────────────────────────────

# Define the start command handler
@bot.on_message(filters.command("start"))
async def start(client: Client, msg: Message):
    db.register_user(msg.from_user.id)
    start_message = await client.send_message(
        msg.chat.id,
        Data.START.format(msg.from_user.mention)
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        Data.START.format(msg.from_user.mention) +
        "Initializing Uploader bot... 🤖\n\n"
        "Progress: [⬜⬜⬜⬜⬜⬜⬜⬜⬜] 0%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        Data.START.format(msg.from_user.mention) +
        "Loading features... ⏳\n\n"
        "Progress: [🟥🟥🟥⬜⬜⬜⬜⬜⬜] 25%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        Data.START.format(msg.from_user.mention) +
        "This may take a moment, sit back and relax! 🥵\n\n"
        "Progress: [🟧🟧🟧🟧🟧⬜⬜⬜⬜] 50%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        Data.START.format(msg.from_user.mention) +
        "Checking Bot Status... 🔍\n\n"
        "Progress: [🟨🟨🟨🟨🟨🟨🟨⬜⬜] 75%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.delete()
    await client.send_photo(
        msg.chat.id,
        photo=random.choice(image_list),
        caption=(
            Data.START.format(msg.from_user.mention) +
            "✅ Bot Ready! Command is Private Dear.🌚\n"
            "**Bot Made BY @SmartBoy_ApnaMS** 🔍\n\n Chek Now Your Subscription /myplan OR For Help /help OR our total users /users is Live Now🤩."
            "Progress: [🟩🟩🟩🟩🟩🟩🟩🟩🟩] 100%\n\n"
        ),
        reply_markup=keyboard
    )

@bot.on_message(filters.command(["stop"]) )
async def restart_handler(_, m):
    await m.reply_text("🛑**STOPPED**🛑", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command("addauth") & filters.private)
async def add_auth_user(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command🤡.")

    # Format: /addauth <user_id> <num> <unit> <nickname>
    # Example: /addauth 123456789 01 week Mahira
    try:
        cmd = message.command
        if len(cmd) < 5:
            return await message.reply_text(
                "❌ Wrong format!\n\n"
                "✅ Correct: `/addauth <user_id> <num> <unit> <nickname>`\n"
                "📌 Example: `/addauth 123456789 01 week Mahira`\n\n"
                "⏱ Units: `day` | `week` | `month` | `year`"
            )
        user_id = int(cmd[1])
        duration_str = f"{cmd[2]} {cmd[3]}"   # e.g. "01 week"
        nickname = cmd[4]

        expires, err = db.add_auth_user(user_id, duration_str, nickname)
        if err:
            return await message.reply_text(f"❌ Error: {err}")

        # Also add to in-memory AUTH_USERS if not present
        if user_id not in AUTH_USERS:
            AUTH_USERS.append(user_id)

        await message.reply_text(
            f"✅ **User Authorized Successfully!**\n\n"
            f"👤 **User ID:** `{user_id}`\n"
            f"🏷 **Nickname:** `{nickname}`\n"
            f"⏱ **Duration:** `{cmd[2]} {cmd[3]}`\n"
            f"📅 **Expires At:** `{expires.strftime('%Y-%m-%d %H:%M:%S')}`"
        )
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid user ID🙄.")


@bot.on_message(filters.command("rmauth") & filters.private)
async def remove_auth_user(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command🤡.")

    try:
        user_id_to_remove = int(message.command[1])
        removed = db.remove_auth_user(user_id_to_remove)
        if not removed:
            await message.reply_text("User ID is not in the authorized users list🤡.")
        else:
            if user_id_to_remove in AUTH_USERS:
                AUTH_USERS.remove(user_id_to_remove)
            await message.reply_text(f"✅ User ID `{user_id_to_remove}` removed from authorized users.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid user ID🙄.")


@bot.on_message(filters.command("users"))
async def list_auth_users(client: Client, message: Message):
    db.register_user(message.from_user.id)
    uid = message.from_user.id
    auth_users_data = db.get_all_auth_users()
    valid_count = len(db.get_auth_user_ids())

    if uid == OWNER:
        # ── OWNER view ────────────────────────────────────────────
        lines = [
            "👑 **Welcome Boss to check our Database!**\n",
            f"🗄️ **Total Authorised Users:** `{valid_count}`\n",
            "━━━━━━━━━━━━━━━━━━━━━━\n"
        ]
        if not auth_users_data:
            lines.append("_No authorized users yet._")
        else:
            for i, (uid_str, info) in enumerate(auth_users_data.items(), 1):
                nickname = info.get("nickname", "N/A")
                granted = info.get("granted_at", "N/A")
                expires = info.get("expires_at", "N/A")
                lines.append(
                    f"**{i}.** 👤 `{uid_str}`\n"
                    f"   🏷 Nickname: `{nickname}`\n"
                    f"   📅 Granted: `{granted}`\n"
                    f"   ⏳ Expires: `{expires}`\n"
                )
        await message.reply_photo(
            photo=random.choice(image_list),
            caption="".join(lines)
        )

    else:
        # ── Common header for all non-owners ──────────────────────
        header = (
            f"🗄️ **Welcome to our Database!**\n\n"
            f"✨ **Total Authorised Users:** `{valid_count}`\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )

        if db.is_authorized(uid):
            # ── Authorised user view ───────────────────────────────
            shayari = (
                "\n\n💫 _تیرا نام ہمارے دل میں ہے،_\n"
                "_تو ہمارا خاص ہے ہمیشہ کے لیے۔_ 🌹"
            )
            footer = (
                f"\n\n💚 **Don't worry, you are also in our authorized users!**\n"
                f"📋 Tap on /myplan to know your plan details.\n"
                f"⚠️ Facing any issue? Contact: @SmartBoy_ApnaMS"
            )
            await message.reply_photo(
                photo=random.choice(image_list),
                caption=header + shayari + footer
            )

        else:
            # ── Unauthorised user view ─────────────────────────────
            footer = (
                f"\n\n🌟 **Don't worry — you can also become a part of our Premium Family!**\n"
                f"We'd love to have you on board. Join thousands of happy users today. 🚀\n\n"
                f"📋 Check plans: /help\n"
                f"💬 Contact: @SmartBoy_ApnaMS"
            )
            await message.reply_photo(
                photo=random.choice(image_list),
                caption=header + footer
            )


@bot.on_message(filters.command("help"))
async def help_handler(client: Client, message: Message):
    db.register_user(message.from_user.id)
    help_text = (
        "╔══════════════════════════╗\n"
        "║  🤖 **SmartyMS Uploader Bot**  ║\n"
        "╚══════════════════════════╝\n\n"
        "📋 **Commands:**\n"
        "┣ /start — Start the Bot\n"
        "┣ /darling — 📥 TXT Batch Downloader\n"
        "┣ /myplan — 📊 Check Your Plan\n"
        "┣ /users — 🗄️ Database Info\n"
        "┗ /help — ❓ This Menu\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "💎 **Subscription Plans**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🟢 **Basic Plan**\n"
        "   ₹ 45 Per Week\n\n"
        "🥈 **Silver Plan**\n"
        "   ₹ 200 Per Month\n\n"
        "🥇 **Gold Plan**\n"
        "   ₹ 500 Per 3 Months\n\n"
        "💠 **Diamond Plan**\n"
        "   ₹ 800 Per 7 Months\n\n"
        "⚡ **Pro Plan**\n"
        "   ₹ 900 Per Year\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🌟 **MS Special Subscription**\n"
        "   🎁 For MS Friends — _First Time:_\n"
        "   ✨ **15 Minutes FREE Trailer**\n"
        "   🏷 **25% OFF** on Monthly & Yearly Plans\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📊 Check your current plan: /myplan\n"
        "💬 Know more? Talk to Admin: @SmartBoy_ApnaMS"
    )
    await message.reply_photo(
        photo=random.choice(image_list),
        caption=help_text
    )


@bot.on_message(filters.command("myplan"))
async def myplan_handler(client: Client, message: Message):
    db.register_user(message.from_user.id)
    uid = message.from_user.id
    info = db.get_auth_user(uid)

    if not info:
        await message.reply_photo(
            photo=random.choice(image_list),
            caption=(
                "🚫 **Not Authorized!**\n\n"
                "You don't have an active subscription yet.\n\n"
                "📋 Check plans: /help\n"
                "💬 Contact: @SmartBoy_ApnaMS"
            )
        )
        return

    from datetime import datetime
    now = datetime.now()
    try:
        granted_dt = datetime.strptime(info["granted_at"], "%Y-%m-%d %H:%M:%S")
        expires_dt = datetime.strptime(info["expires_at"], "%Y-%m-%d %H:%M:%S")
    except Exception:
        await message.reply_text("❌ Could not read your plan data. Contact @SmartBoy_ApnaMS")
        return

    if now >= expires_dt:
        await message.reply_photo(
            photo=random.choice(image_list),
            caption=(
                "⏰ **Your Subscription Has Expired!**\n\n"
                "📋 Renew via: /help\n"
                "💬 Contact: @SmartBoy_ApnaMS"
            )
        )
        return

    # Time remaining
    remaining = expires_dt - now
    remaining_days = remaining.days
    remaining_hours = remaining.seconds // 3600
    remaining_mins = (remaining.seconds % 3600) // 60

    nickname = info.get("nickname", "N/A")

    await message.reply_photo(
        photo=random.choice(image_list),
        caption=(
            f"🙏 **Thank You for Being Our Premium Member!** 💖\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 **Your Plan Details**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 **Name:** `{nickname}`\n"
            f"🆔 **User ID:** `{uid}`\n\n"
            f"📅 **Granted At:** `{granted_dt.strftime('%d %b %Y, %I:%M %p')}`\n"
            f"⏳ **Expires At:** `{expires_dt.strftime('%d %b %Y, %I:%M %p')}`\n\n"
            f"⏱ **Time Remaining:**\n"
            f"   `{remaining_days}` Days & `{remaining_hours}` Hours & `{remaining_mins}` Minutes\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 View plans: /help\n"
            f"💬 Any issue? Contact: @SmartBoy_ApnaMS"
        )
    )


@bot.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(client: Client, message: Message):
    if message.from_user.id != OWNER:
        return await message.reply_text("you are not my owner 😒.")

    # Must be a reply to the content to broadcast
    if not message.reply_to_message:
        return await message.reply_text(
            "📢 **Broadcast Mode**\n\n"
            "please Boss reply with such a content for brodcasting."
        )

    content = message.reply_to_message
    all_users = db.get_all_user_ids()

    if not all_users:
        return await message.reply_text("❌ No users in database yet.")

    sent = 0
    failed = 0
    status_msg = await message.reply_text(f"📤 Broadcasting to `{len(all_users)}` users...")

    for user_id in all_users:
        try:
            await content.copy(user_id)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)  # small delay to avoid flood

    await status_msg.edit_text(
        f"✅ **Broadcast Complete!**\n\n"
        f"📨 Sent: `{sent}`\n"
        f"❌ Failed: `{failed}`\n"
        f"👥 Total: `{len(all_users)}`"
    )

# ── /addchannel ────────────────────────────────────────────────────────────────
@bot.on_message(filters.command("addchannel"))
async def addchannel_handler(client: Client, message: Message):
    uid = message.from_user.id if message.from_user else None
    if uid != OWNER and not db.is_authorized(uid):
        return await message.reply_text("🚫 Only Authorized Users & Owner can use this command.")
    try:
        chat_id = int(message.command[1])
    except (IndexError, ValueError):
        return await message.reply_text(
            "❌ Wrong format!\n\n"
            "✅ Use: `/addchannel -100XXXXXXXXXX`\n"
            "📌 Example: `/addchannel -1001234567890`\n\n"
            "⚠️ The `-` sign is required for channel/group IDs."
        )
    db.add_channel(chat_id)
    await message.reply_text(
        f"✅ **Channel/Group Added Successfully!**\n\n"
        f"🆔 Chat ID: `{chat_id}`\n\n"
        f"Bot will now work in this chat for authorized users. 🚀"
    )


# ── /rmchannel ─────────────────────────────────────────────────────────────────
@bot.on_message(filters.command("rmchannel"))
async def rmchannel_handler(client: Client, message: Message):
    if message.from_user.id != OWNER:
        return await message.reply_text("🚫 Only Owner can remove channels.")
    try:
        chat_id = int(message.command[1])
    except (IndexError, ValueError):
        return await message.reply_text("❌ Use: `/rmchannel -100XXXXXXXXXX`")
    removed = db.remove_channel(chat_id)
    if removed:
        await message.reply_text(f"✅ Chat ID `{chat_id}` removed from allowed list.")
    else:
        await message.reply_text(f"❌ Chat ID `{chat_id}` was not in the list.")


# ── /channels ──────────────────────────────────────────────────────────────────
@bot.on_message(filters.command("channels") & filters.private)
async def list_channels_handler(client: Client, message: Message):
    if message.from_user.id != OWNER:
        return await message.reply_text("🚫 Only Owner can view this list.")
    channels = db.get_all_channels()
    if not channels:
        return await message.reply_text("📭 No channels/groups added yet.")
    lines = ["📋 **Allowed Channels & Groups:**\n"]
    for i, cid in enumerate(channels, 1):
        lines.append(f"**{i}.** `{cid}`")
    await message.reply_text("\n".join(lines))





@bot.on_message(filters.command(["darling"]) )
async def txt_handler(bot: Client, m: Message):
    db.register_user(m.from_user.id)

    # ── Auth Check (DM + allowed channel/group) ────────────────
    is_dm = m.chat.type.name == "PRIVATE"
    chat_allowed = db.is_allowed_chat(m.chat.id)
    user_auth = db.is_authorized(m.from_user.id)

    if not (user_auth or (chat_allowed and user_auth)):
        return await m.reply_photo(
            photo=random.choice(image_list),
            caption=(
                "🚫 **First Buy a Premium Subscription first Baby** 💎\n\n"
                "📋 Check plans: /help\n"
                "💬 Contact: @SmartBoy_ApnaMS"
            )
        )
    await m.reply_text("✅ **Great You are My Favourite Costumer** 🌟")
    # ────────────────────────────────────────────────────────────

    editable = await m.reply_text(f"**🔹Hi I am Poweful Lovely TXT Downloader📥 Bot.**\n🔹**Send me the TXT file and Just wait and Watch😚.**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = f"@SmartBoy_ApnaMS"
    token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzYxNTE3MzAuMTI2LCJkYXRhIjp7Il9pZCI6IjYzMDRjMmY3Yzc5NjBlMDAxODAwNDQ4NyIsInVzZXJuYW1lIjoiNzc2MTAxNzc3MCIsImZpcnN0TmFtZSI6IkplZXYgbmFyYXlhbiIsImxhc3ROYW1lIjoic2FoIiwib3JnYW5pemF0aW9uIjp7Il9pZCI6IjVlYjM5M2VlOTVmYWI3NDY4YTc5ZDE4OSIsIndlYnNpdGUiOiJwaHlzaWNzd2FsbGFoLmNvbSIsIm5hbWUiOiJQaHlzaWNzd2FsbGFoIn0sImVtYWlsIjoiV1dXLkpFRVZOQVJBWUFOU0FIQEdNQUlMLkNPTSIsInJvbGVzIjpbIjViMjdiZDk2NTg0MmY5NTBhNzc4YzZlZiJdLCJjb3VudHJ5R3JvdXAiOiJJTiIsInR5cGUiOiJVU0VSIn0sImlhdCI6MTczNTU0NjkzMH0.iImf90mFu_cI-xINBv4t0jVz-rWK1zeXOIwIFvkrS0M"
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("Hii Cutie Pie.🌚😘")
        os.remove(x)
        return
   
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download🤔 initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    try:
        arg = int(raw_text)
    except:
        arg = 1
    await editable.edit("**Enter Your Batch Name or send '/ms' for grabing from text filename.😉**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == '/ms':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution.\n Eg : 144, 250, 360, 480, 720 or 1080😚**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    await editable.edit("**Enter Your Name or send '/Baby' for use default.🌚\n Eg :@SmartBoy_ApnaMS **")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == '/Baby':
        CR = credit
    else:
        CR = parse_credit(raw_text3)
        
    await editable.edit("**Enter Your PW Token For 𝐌𝐏𝐃 𝐔𝐑𝐋  or send '/vip' for use default🎀**")
    input4: Message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text
    await input4.delete(True)
    if raw_text4 == '/vip':
        MR = token
    else:
        MR = raw_text4
        
    await editable.edit("Now send the **Thumb url**\n**Eg: Who's End With .jpg** ``\n\nor Send `no`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    count =int(raw_text)    
    try:
        for i in range(arg-1, len(links)):

            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url or "tencdn.classplusapp" in url or "webvideos.classplusapp.com" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "videos.classplusapp.com" in url or "media-cdn-a.classplusapp" in url or "media-cdn.classplusapp" in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']

            
            #elif '/master.mpd' in url:
             #id =  url.split("/")[-2]
             #url = f"https://player.muftukmall.site/?id={id}"
            #elif '/master.mpd' in url:
             #id =  url.split("/")[-2]
             #url = f"https://anonymouspwplayer-907e62cf4891.herokuapp.com/pw?url={url}?token={raw_text4}"
            #url = f"https://madxapi-d0cbf6ac738c.herokuapp.com/{id}/master.m3u8?token={raw_text4}"
            elif"d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
             url = f"https://anonymouspwplayer-907e62cf4891.herokuapp.com/pw?url={url}&token={raw_text4}"
                     
                                                         
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]} {my_name}'
                      
            
            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                url = url.split("bcov_auth")[0]+bcov
                
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'

            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                
                cc = f'**📹 VID_ID: {str(count).zfill(3)}.\n\n📝 Title: {name1} {res}.mkv\n\n<pre><code>📚 Batch Name: {b_name}</code></pre>\n\n📥 Extracted By♠ : {CR}\n\n**∘𒆜━━━❀💚𝐌𝐒🤍❀━━━𒆜∘**'
                cc1 = f'**💾 PDF_ID: {str(count).zfill(3)}.\n\n📝 Title: {name1} .pdf\n\n<pre><code>📚 Batch Name: {b_name}</code></pre>\n\n📥 Extracted By♠ : {CR}\n\n**∘𒆜━━━❀💚𝐌𝐒🤍❀━━━𒆜∘**'
                    
                
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

        # Send a GET request to download the PDF
                        response = scraper.get(url)

        # Check if the response status is OK
                        if response.status_code == 200:
            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue                       
                          
                else:
                    Show = f"✰🖥️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝗪𝗮𝗶𝘁..🤖🚀 »\n\n📝 Title:- `{name}\n\n📹 𝐐𝐮𝐥𝐢𝐭𝐲 » {raw_text2}`\n\n**🔗 𝐔𝐑𝐋 »** `{url}`\n\n**𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲🧸: ✦ @SmartBoy_ApnaMS ❖"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"⌘✰𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝗙𝗮𝗶𝗹𝗲𝗱⛔\n\n⌘ 𝐍𝐚𝐦𝐞🌟 » {name}\n⌘ 𝐋𝐢𝐧𝐤🖥️ » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("𝐀𝐋𝐋 𝐃𝐎𝐍𝐄 NOW TIMES FOR REACTIONS.✅🔸")

# Advance

@bot.on_message(filters.command(["darling"]) )
async def txt_handler(bot: Client, m: Message):
    db.register_user(m.from_user.id)

    # ── Auth Check (DM + allowed channel/group) ────────────────
    user_auth = db.is_authorized(m.from_user.id)
    chat_allowed = db.is_allowed_chat(m.chat.id)

    if not (user_auth or (chat_allowed and user_auth)):
        return await m.reply_photo(
            photo=random.choice(image_list),
            caption=(
                "🚫 **First Buy a Premium Subscription first Baby** 💎\n\n"
                "📋 Check plans: /help\n"
                "💬 Contact: @SmartBoy_ApnaMS"
            )
        )
    await m.reply_text("✅ **Great You are My Favourite Costumer** 🌟")
    # ────────────────────────────────────────────────────────────

    editable = await m.reply_text(f"**🔹Hi I am Poweful Lovely TXT Downloader📥 Bot.**\n🔹**Send me the TXT file and Just wait and Watch🥵.**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = f"@SmartBoy_ApnaMS"
    token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzYxNTE3MzAuMTI2LCJkYXRhIjp7Il9pZCI6IjYzMDRjMmY3Yzc5NjBlMDAxODAwNDQ4NyIsInVzZXJuYW1lIjoiNzc2MTAxNzc3MCIsImZpcnN0TmFtZSI6IkplZXYgbmFyYXlhbiIsImxhc3ROYW1lIjoic2FoIiwib3JnYW5pemF0aW9uIjp7Il9pZCI6IjVlYjM5M2VlOTVmYWI3NDY4YTc5ZDE4OSIsIndlYnNpdGUiOiJwaHlzaWNzd2FsbGFoLmNvbSIsIm5hbWUiOiJQaHlzaWNzd2FsbGFoIn0sImVtYWlsIjoiV1dXLkpFRVZOQVJBWUFOU0FIQEdNQUlMLkNPTSIsInJvbGVzIjpbIjViMjdiZDk2NTg0MmY5NTBhNzc4YzZlZiJdLCJjb3VudHJ5R3JvdXAiOiJJTiIsInR5cGUiOiJVU0VSIn0sImlhdCI6MTczNTU0NjkzMH0.iImf90mFu_cI-xINBv4t0jVz-rWK1zeXOIwIFvkrS0M"
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("Hii Cutie Pie.🌚😘")
        os.remove(x)
        return
   
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download🤔 initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    try:
        arg = int(raw_text)
    except:
        arg = 1
    await editable.edit("**Enter Your Batch Name or send '/ms' for grabing from text filename.🌚**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == '/ms':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution.\n Eg : 144, 240, 360, 480, 720 or 1080😚**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    await editable.edit("**Enter Your Name or send '/Baby' for use default.😗\n Eg : @SmartBoy_ApnaMS**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == '/Baby':
        CR = credit
    else:
        CR = parse_credit(raw_text3)
        
       
    await editable.edit("Now send the **Thumb url**\n**Eg Who's End With .jpg:** ``\n\nor Send `no`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://files.catbox.moe/mwhput.jpg"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    count =int(raw_text)    
    try:
        for i in range(arg-1, len(links)):

            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url or "tencdn.classplusapp" in url or "webvideos.classplusapp.com" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "videos.classplusapp.com" in url or "media-cdn-a.classplusapp" in url or "media-cdn.classplusapp" in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']

            elif "apps-s3-jw-prod.utkarshapp.com" in url:
                if 'enc_plain_mp4' in url:
                    url = url.replace(url.split("/")[-1], res+'.mp4')
                    
                elif 'Key-Pair-Id' in url:
                    url = None
                    
                elif '.m3u8' in url:
                    q = ((m3u8.loads(requests.get(url).text)).data['playlists'][1]['uri']).split("/")[0]
                    x = url.split("/")[5]
                    x = url.replace(x, "")
                    url = ((m3u8.loads(requests.get(url).text)).data['playlists'][1]['uri']).replace(q+"/", x)
                    
            elif '/master.mpd' in url:
             vid_id =  url.split("/")[-2]
             url =  f"https://pw-url-api-v1mf.onrender.com/process?v=https://sec1.pw.live/{vid_id}/master.mpd&quality={raw_text2}"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]} {my_name}'
          

            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                url = url.split("bcov_auth")[0]+bcov
                
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'

            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
        
                cc = f'**📹 VID_ID: {str(count).zfill(3)}.\n\nTitle: {name1} STUDENTS💛{res}.mkv\n\n📚 Batch Name: {b_name}\n\n📥 Extracted By♠ : {CR}\n\n**∘𒆜━━━❀🩷𝐌𝐒🤍❀━━━𒆜∘**'
                cc1 = f'**💾 PDF_ID: {str(count).zfill(3)}.\n\nTitle: {name1} STUDENTS💛.pdf\n\n📚 Batch Name: {b_name}\n\n📥 Extracted By♠ : {CR}\n\n**∘𒆜━━━❀🩷𝐌𝐒🤍❀━━━𒆜∘**'
                    
                
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

        # Send a GET request to download the PDF
                        response = scraper.get(url)

        # Check if the response status is OK
                        if response.status_code == 200:
            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue                       
                          
                else:
                    Show = f"✰🖥️𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝗪𝗮𝗶𝘁..🤖🚀»\n\n📝 Title:- `{name}\n\n🖥️ 𝐐𝐮𝐥𝐢𝐭𝐲 » {raw_text2}`\n\n**🔗 𝐔𝐑𝐋 »** `{url}`\n\n**𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲🧸: ✦ @SmartBoy_ApnaMS✰"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"⌘ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝗙𝗮𝗶𝗹𝗲𝗱⛔\n\n⌘ 𝐍𝐚𝐦𝐞🌟 » {name}\n⌘ 𝐋𝐢𝐧𝐤 » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("𝐀𝐋𝐋 𝐃𝐎𝐍𝐄 NOW TIMES FOR REACTIONS.✅🔸")


# ─── Flask keep-alive server for Render ───────────────────────────────────────
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return 'Bot is running! @SmartBoy_ApnaMS'

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    flask_app.run(host="0.0.0.0", port=port)

# Start Flask in background thread so Render detects open port
threading.Thread(target=run_flask, daemon=True).start()
# ─────────────────────────────────────────

bot.run()
