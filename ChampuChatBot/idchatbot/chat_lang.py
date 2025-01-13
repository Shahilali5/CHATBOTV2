from pyrogram import Client, filters
from pyrogram.types import Message
from ChampuChatBot import ChampuChatBot as app, mongo, db
from MukeshAPI import api
import asyncio
from ChampuChatBot.idchatbot.helpers import chatai, languages
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

lang_db = db.ChatLangDb.LangCollection
message_cache = {}

async def get_chat_language(chat_id, bot_id):
    chat_lang = await lang_db.find_one({"chat_id": chat_id, "bot_id": bot_id})
    return chat_lang["language"] if chat_lang and "language" in chat_lang else None

@Client.on_message(filters.command("chatlang", prefixes=[".", "/"]))
async def fetch_chat_lang(client, message):
    chat_id = message.chat.id
    bot_id = client.me.id
    chat_lang = await get_chat_language(chat_id, bot_id)
    await message.reply_text(f"ᴛʜᴇ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇ ʙᴇɪɴɢ ᴜsᴇᴅ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ ɪs: {chat_lang}")

@Client.on_message(filters.text, group=4)
async def store_messages(client, message: Message):
    global message_cache

    chat_id = message.chat.id
    bot_id = client.me.id
    chat_lang = await get_chat_language(chat_id, bot_id)

    if not chat_lang or chat_lang == "nolang":
        if message.from_user and message.from_user.is_bot:
            return

        if chat_id not in message_cache:
            message_cache[chat_id] = []

        message_cache[chat_id].append(message)

        if len(message_cache[chat_id]) >= 30:
            history = "\n\n".join(
                [f"ᴛᴇxᴛ: {msg.text}..." for msg in message_cache[chat_id]]
            )
            user_input = f"""
            sᴇɴᴛᴇɴᴄᴇs ʟɪsᴛ :-
            [
            {history}
            ]

            ᴀʙᴏᴠᴇ ɪs ᴀ ʟɪsᴛ ᴏғ sᴇɴᴛᴇɴᴄᴇs. ᴇᴀᴄʜ sᴇɴᴛᴇɴᴄᴇ ᴄᴏᴜʟᴅ ʙᴇ ɪɴ ᴅɪғғᴇʀᴇɴᴛ ʟᴀɴɢᴜᴀɢᴇs. ᴀɴᴀʟʏᴢᴇ ᴛʜᴇ ʟᴀɴɢᴜᴀɢᴇ ᴏғ ᴇᴀᴄʜ sᴇɴᴛᴇɴᴄᴇ sᴇᴘᴀʀᴀᴛᴇʟʏ ᴀɴᴅ ɪᴅᴇɴᴛɪғʏ ᴛʜᴇ ᴅᴏᴍɪɴᴀɴᴛ ʟᴀɴɢᴜᴀɢᴇ ᴜsᴇᴅ ғᴏʀ ᴇᴀᴄʜ sᴇɴᴛᴇɴᴄᴇ. ᴛʜᴇɴ, ᴄᴏɴsɪᴅᴇʀ ᴛʜᴇ ʟᴀɴɢᴜᴀɢᴇ ᴛʜᴀᴛ ᴀᴘᴘᴇᴀʀs ᴛʜᴇ ᴍᴏsᴛ, ɪɢɴᴏʀɪɴɢ ᴀɴʏ ᴄᴏᴍᴍᴀɴᴅs ʟɪᴋᴇ sᴇɴᴛᴇɴᴄᴇs sᴛᴀʀᴛɪɴɢ ᴡɪᴛʜ /. 
            ᴘʀᴏᴠɪᴅᴇ ᴏɴʟʏ ᴛʜᴇ ᴏғғɪᴄɪᴀʟ ʟᴀɴɢᴜᴀɢᴇ ɴᴀᴍᴇ ᴡɪᴛʜ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇ (ʟɪᴋᴇ 'en' ғᴏʀ ᴇɴɢʟɪsʜ, 'hi' ғᴏʀ ʜɪɴᴅɪ) ɪɴ ᴛʜɪs ғᴏʀᴍᴀᴛ:
            ʟᴀɴɢ ɴᴀᴍᴇ :- ""
            ʟᴀɴɢ ᴄᴏᴅᴇ :- ""
            ᴘʀᴏᴠɪᴅᴇ ᴏɴʟʏ ᴏᴠᴇʀᴀʟʟ [ʟᴀɴɢ ɴᴀᴍᴇ ᴀɴᴅ ʟᴀɴɢ ᴄᴏᴅᴇ] ɪɴ ᴛʜᴇ ᴀʙᴏᴠᴇ ғᴏʀᴍᴀᴛ. ᴅᴏ ɴᴏᴛ ᴘʀᴏᴠɪᴅᴇ ᴀɴʏᴛʜɪɴɢ ᴇʟsᴇ.
            """
            await asyncio.sleep(60)
            response = api.gemini(user_input)
            x = response["results"]
            await message.reply_text(f"**ᴄʜᴀᴛ ʟᴀɴɢᴜᴀɢᴇ ᴅᴇᴛᴇᴄᴛᴇᴅ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ:**\n\n{x}\n\n**ʏᴏᴜ ᴄᴀɴ sᴇᴛ ᴍʏ ʟᴀɴɢᴜᴀɢᴇ ᴜsɪɴɢ /lang**")
            message_cache[chat_id].clear()
