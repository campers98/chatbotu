"""
ɢɪᴛʜᴜʙ -Abishnoi69
ᴛᴇʟᴇɢʀᴀᴍ @Abishnoi1M / @Abishnoi_bots 

"""
import random

import requests
from pymongo import MongoClient
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from AsuX import *

USERS_GROUP = 11


from config import MONGO_DB_URL, AI_BID, AI_API_KEY

# Connect to MongoDB
chatbotdb = MongoClient(MONGO_DB_URL)
chatbotai = chatbotdb["Word"]["WordDb"]
chat_settings = chatbotdb["ChatSettings"]["Settings"]

# Define the command handler to toggle the chatbot
async def toggle_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    chat_setting = chat_settings.find_one({"chat_id": chat.id})
    if chat_setting and chat_setting.get("chatbot_enabled", False):
        chat_settings.update_one({"chat_id": chat.id}, {"$set": {"chatbot_enabled": False}})
        await update.message.reply_text("Chatbot has been disabled in this chat.")
    else:
        chat_settings.update_one({"chat_id": chat.id}, {"$set": {"chatbot_enabled": True}}, upsert=True)
        await update.message.reply_text("Chatbot has been enabled in this chat.")

# Log user messages and respond if the chatbot is enabled
async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message
    
    # Check if chatbot is enabled for this chat
    chat_setting = chat_settings.find_one({"chat_id": chat.id})
    if not (chat_setting and chat_setting.get("chatbot_enabled", False)):
        return
    
    try:
        if (
            message.text.startswith("!")
            or message.text.startswith("/")
            or message.text.startswith("?")
            or message.text.startswith("@")
            or message.text.startswith("#")
        ):
            return
    except Exception:
        pass
    
    if not message.reply_to_message:
        K = []
        is_chat = chatbotai.find({"chat": chat.id, "word": message.text})
        for x in is_chat:
            K.append(x["text"])
        if K:
            hey = random.choice(K)
            is_text = chatbotai.find_one({"chat": chat.id, "text": hey})
            Yo = is_text["check"]
        else:
            r = requests.get(
                f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}"
            )
            hey = r.json()["cnt"]
            Yo = None
        if Yo == "sticker":
            await message.reply_sticker(f"{hey}")
        if not Yo == "sticker":
            await message.reply_text(f"{hey}")
    if message.reply_to_message:
        if message.reply_to_message.from_user.id == BOT_ID:
            K = []
            is_chat = chatbotai.find({"chat": chat.id, "word": message.text})
            for x in is_chat:
                K.append(x["text"])
            if K:
                hey = random.choice(K)
                is_text = chatbotai.find_one({"chat": chat.id, "text": hey})
                Yo = is_text["check"]
            else:
                r = requests.get(
                    f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}"
                )
                hey = r.json()["cnt"]
                Yo = None
            if Yo == "sticker":
                await message.reply_sticker(f"{hey}")
            if not Yo == "sticker":
                await message.reply_text(f"{hey}")
        if not message.reply_to_message.from_user.id == BOT_ID:
            if message.sticker:
                is_chat = chatbotai.find_one(
                    {
                        "chat": chat.id,
                        "word": message.reply_to_message.text,
                        "id": message.sticker.file_unique_id,
                    }
                )
                if not is_chat:
                    chatbotai.insert_one(
                        {
                            "chat": chat.id,
                            "word": message.reply_to_message.text,
                            "text": message.sticker.file_id,
                            "check": "sticker",
                            "id": message.sticker.file_unique_id,
                        }
                    )
            if message.text:
                is_chat = chatbotai.find_one(
                    {
                        "chat": chat.id,
                        "word": message.reply_to_message.text,
                        "text": message.text,
                    }
                )
                if not is_chat:
                    chatbotai.insert_one(
                        {
                            "chat": chat.id,
                            "word": message.reply_to_message.text,
                            "text": message.text,
                            "check": "none",
                        }
                    )

# Add handlers to application
def add_chatbot_handlers(application):
    application.add_handler(CommandHandler("chatbot", toggle_chatbot))
    application.add_handler(MessageHandler(filters.ALL, log_user, block=False))
