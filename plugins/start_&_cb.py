import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from helper.database import db
from config import Config, Txt

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await db.add_user(client, message)
    
    # Liste des stickers et messages intermédiaires
    sequence = [
        {"type": "message", "text": "✨ Salut. Je suis Luffy. Le chef de l'équipage au chapeau de paille😁...."},
        {"type": "sticker", "id": "CAACAgQAAxkBAAI3VWhpJkh1GJkxjq7ciOKcTHlAQ28BAALkFQACfqTJUVt-EzCZ0Ol6HgQ"},  # ID du 1er sticker
        {"type": "message", "text": " Moi mon rêve à moi, c'est de trouver le One piece qu'elle qu'en soit le Prix💥 ..."},
        {"type": "sticker", "id": "CAACAgQAAxkBAAI3VWhpJkh1GJkxjq7ciOKcTHlAQ28BAALkFQACfqTJUVt-EzCZ0Ol6HgQ"},  # ID du 2ème sticker
        {"type": "message", "text": " Et je  deviendrai le Roi des Pirates ..."},
        {"type": "sticker", "id": "CAACAgQAAxkBAAI3VWhpJkh1GJkxjq7ciOKcTHlAQ28BAALkFQACfqTJUVt-EzCZ0Ol6HgQ"}   # ID du 3ème sticker
    ]
    
    # Envoyer et supprimer les éléments un par un
    for item in sequence:
        if item["type"] == "message":
            sent_item = await message.reply_text(item["text"])
        else:
            sent_item = await message.reply_sticker(item["id"])
        
        await asyncio.sleep(2)  # Attendre 2 secondes
        await sent_item.delete()
        await asyncio.sleep(0.3)  # Petit délai entre les éléments
    
    # Envoyer le vrai message de démarrage après la séquence
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton("Cᴏɴᴛᴀᴄᴛ Dᴇᴠ", callback_data='dev')
        ],[
        InlineKeyboardButton('Mɪsᴇ à ᴊᴏᴜʀ', url='https://t.me/BotZFlix'),
        InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ', url='https://t.me/BTZF_CHAT')
        ],[
        InlineKeyboardButton('À Pʀᴏᴘᴏs', callback_data='about'),
        InlineKeyboardButton('Aɪᴅᴇ', callback_data='help')
    ]])
    
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)
   

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cᴏɴᴛᴀᴄᴛ Dᴇᴠ", callback_data='dev')
                ],[
                InlineKeyboardButton('Mɪsᴇ à ᴊᴏᴜʀ', url='https://t.me/BotZFlix'),
                InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ', url='https://t.me/BZFT_CHAT')
                ],[
                InlineKeyboardButton('À Pʀᴏᴘᴏs', callback_data='about'),
                InlineKeyboardButton('Aɪᴅᴇ', callback_data='help')
            ]])
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("❣️ Code Source", url="https://github.com/TEAM-PYRO-BOTZ/PYRO-RENAME-BOT")
                ],[
                InlineKeyboardButton("❤️‍🔥 Tutoriel", url='https://youtu.be/4ZfvMSDXBVg')
                ],[
                InlineKeyboardButton("🔒 Fermer", callback_data="close"),
                InlineKeyboardButton("◀️ Retour", callback_data="start")
            ]])            
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("❣️ Code Source", callback_data="dev")
                ],[
                InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/BTFZ_CHAT")
                ],[
                InlineKeyboardButton("񑠠 ZFʟɪx-Tᴇᴀᴍ", callback_data="zft"),
                InlineKeyboardButton("◀️ Retour", callback_data="start")
            ]])            
        )
    elif data == "zft":
        await query.message.edit_text(
            text=Txt.ZFT_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("❣️ Rejoindre ", url="https://t.me/ZFlixTeam")
                ],[
                InlineKeyboardButton("🎌 Contact", url="https://t.me/ZFlixTeamBot")
                ],[
                InlineKeyboardButton("🔒 Fermer", callback_data="close"),
                InlineKeyboardButton("◀️ Retour", callback_data="start")
            ]])          
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()