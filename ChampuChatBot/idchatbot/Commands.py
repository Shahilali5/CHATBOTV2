import random
import os
import sys
from MukeshAPI import api
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
from ChampuChatBot.database.chats import add_served_chat
from ChampuChatBot.database.users import add_served_user
from config import MONGO_URL
from ChampuChatBot import ChampuChatBot, mongo, LOGGER, db
from ChampuChatBot.idchatbot.helpers import chatai, languages
import asyncio

translator = GoogleTranslator()

lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status


async def get_chat_language(chat_id, bot_id):
    chat_lang = await lang_db.find_one({"chat_id": chat_id, "bot_id": bot_id})
    return chat_lang["language"] if chat_lang and "language" in chat_lang else None
   
    
@Client.on_message(filters.command("status", prefixes=[".", "/"]))
async def status_command(client: Client, message: Message):
    chat_id = message.chat.id
    bot_id = client.me.id
    chat_status = await status_db.find_one({"chat_id": chat_id, "bot_id": bot_id})
    if chat_status:
        current_status = chat_status.get("status", "not found")
        await message.reply(f"ᴄʜᴀᴛʙᴏᴛ sᴛᴀᴛᴜs ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ: **{current_status}**")
    else:
        await message.reply("ɴᴏ sᴛᴀᴛᴜs ғᴏᴜɴᴅ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.")

@Client.on_message(filters.command(["resetlang", "nolang"], prefixes=[".", "/"]))
async def reset_language(client: Client, message: Message):
    chat_id = message.chat.id
    bot_id = client.me.id
    lang_db.update_one(
        {"chat_id": chat_id, "bot_id": bot_id},
        {"$set": {"language": "nolang"}},
        upsert=True
    )
    await message.reply_text("**ʙᴏᴛ ʟᴀɴɢᴜᴀɢᴇ ʜᴀs ʙᴇᴇɴ ʀᴇsᴇᴛ ɪɴ ᴛʜɪs ᴄʜᴀᴛ ᴛᴏ ᴍɪx ʟᴀɴɢᴜᴀɢᴇ.**")


@Client.on_message(filters.command("chatbot", prefixes=[".", "/"]))
async def chatbot_command(client: Client, message: Message):
    command = message.text.split()
    if len(command) > 1:
        flag = command[1].lower()
        chat_id = message.chat.id
        bot_id = client.me.id

        if flag in ["on", "enable"]:
            status_db.update_one(
                {"chat_id": chat_id, "bot_id": bot_id},
                {"$set": {"status": "enabled"}},
                upsert=True
            )
            await message.reply_text(f"ᴄʜᴀᴛʙᴏᴛ ʜᴀs ʙᴇᴇɴ **enabled** ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ ✅.")
        elif flag in ["off", "disable"]:
            status_db.update_one(
                {"chat_id": chat_id, "bot_id": bot_id},
                {"$set": {"status": "disabled"}},
                upsert=True
            )
            await message.reply_text(f"ᴄʜᴀᴛʙᴏᴛ ʜᴀs ʙᴇᴇɴ **disable** ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ ❌.")
        else:
            await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴏᴘᴛɪᴏɴ! ᴜsᴇ `/chatbot on` ᴏʀ `/chatbot off`.")
    else:
        await message.reply_text(
            "ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀɴ ᴏᴘᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ᴛʜᴇ ᴄʜᴀᴛʙᴏᴛ.\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/chatbot on` ᴏʀ `/chatbot off`"
        )



@Client.on_message(filters.command(["lang", "language", "setlang"], prefixes=[".", "/"]))
async def set_language(client: Client, message: Message):
    command = message.text.split()
    if len(command) > 1:
        lang_code = command[1]
        chat_id = message.chat.id
        bot_id = client.me.id
        lang_db.update_one(
            {"chat_id": chat_id, "bot_id": bot_id},
            {"$set": {"language": lang_code}},
            upsert=True
        )
        await message.reply_text(f"ʟᴀɴɢᴜᴀɢᴇ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴛᴏ `{lang_code}`.")
    else:
        await message.reply_text(
            "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ sᴇᴛ ʏᴏᴜʀ ᴄʜᴀᴛ ʟᴀɴɢᴜᴀɢᴇ.\n"
            "**ᴇxᴀᴍᴘʟᴇ:** `/lang en`\n\n"
            "**ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇ ʟɪsᴛ ᴡɪᴛʜ ɴᴀᴍᴇs:**"
            f"{languages}"
        )
