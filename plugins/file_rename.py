from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db

from asyncio import sleep
from PIL import Image
import os, time

# ==================================== Gestion du canal dump ====================================

@Client.on_message(filters.private & filters.command('dump'))
async def set_dump_channel(client, message):
    if len(message.command) < 2:
        current_dump = await db.get_dump_channel(message.from_user.id)
        if current_dump:
            try:
                chat = await client.get_chat(current_dump)
                return await message.reply_text(
                    f"**📌 Canal dump actuel :** {chat.title}\n\n"
                    "Pour changer : `/dump @nom_du_canal`\n"
                    "Pour désactiver : `/dump off`")
            except:
                await db.set_dump_channel(message.from_user.id, None)
        
        return await message.reply_text(
            "**🔧 Configuration du canal dump**\n\n"
            "Pour envoyer les fichiers renommés vers un canal :\n"
            "`/dump @nom_du_canal`\n\n"
            "Pour désactiver : `/dump off`")

    channel = message.command[1]
    if channel.lower() == 'off':
        await db.set_dump_channel(message.from_user.id, None)
        return await message.reply_text("**✅ Canal dump désactivé - Les fichiers seront envoyés en privé**")

    try:
        chat = await client.get_chat(channel)
        if chat.type not in ["channel", "supergroup"]:
            return await message.reply_text("**❌ Vous devez spécifier un canal/supergroupe valide**")

        member = await chat.get_member(client.me.id)
        if not member or not member.can_post_messages:
            return await message.reply_text(
                "**⚠️ Je dois être administrateur avec permission de poster dans ce canal**")

        await db.set_dump_channel(message.from_user.id, chat.id)
        await message.reply_text(
            f"**✅ Canal dump configuré :** {chat.title}\n\n"
            f"Tous les fichiers renommés seront envoyés ici.")
    except Exception as e:
        await message.reply_text(
            f"**Erreur :** {str(e)}\n\n"
            "Assurez-vous que :\n"
            "1. Le bot est ajouté au canal\n"
            "2. Le bot a les permissions d'envoyer des messages")

# ==================================== Fonction de renommage ====================================

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_handler(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name  
    if file.file_size > 2000 * 1024 * 1024:
        return await message.reply_text("Dᴇ́ꜱᴏʟᴇ́ ᴄᴇ ʙᴏᴛ ɴᴇ ᴘʀᴇɴᴅ ᴘᴀꜱ ᴇɴ ᴄʜᴀʀɢᴇ ʟᴇꜱ ꜰɪᴄʜɪᴇʀꜱ ᴅᴇ ᴘʟᴜꜱ ᴅᴇ 2ɢᴏ")

    try:
        await message.reply_text(
            text=f"**__Vᴇᴜɪʟʟᴇᴢ ᴇɴᴛʀᴇʀ ᴜɴ ɴᴏᴜᴠᴇᴀᴜ ɴᴏᴍ ᴅᴇ ꜰɪᴄʜɪᴇʀ...__**\n\n**Aɴᴄɪᴇɴ ɴᴏᴍ** :- `{filename}`",
            reply_to_message_id=message.id,  
            reply_markup=ForceReply(True))
        )       
    except FloodWait as e:
        await sleep(e.value)
        await message.reply_text(
            text=f"**__Vᴇᴜɪʟʟᴇᴢ ᴇɴᴛʀᴇʀ ᴜɴ ɴᴏᴜᴠᴇᴀᴜ ɴᴏᴍ ᴅᴇ ꜰɪᴄʜɪᴇʀ...__**\n\n**Aɴᴄɪᴇɴ ɴᴏᴍ** :- `{filename}`",
            reply_to_message_id=message.id,  
            reply_markup=ForceReply(True))
    except:
        pass

async def force_reply_filter(_, client, message):
    return bool(message.reply_to_message and isinstance(message.reply_to_message.reply_markup, ForceReply))
 
@Client.on_message(filters.private & filters.reply & filters.create(force_reply_filter))
async def rename_selection(client, message):
    reply_message = message.reply_to_message
    new_name = message.text
    await message.delete() 
    msg = await client.get_messages(message.chat.id, reply_message.id)
    file = msg.reply_to_message
    media = getattr(file, file.media.value)
    
    if not "." in new_name:
        extn = media.file_name.rsplit('.', 1)[-1] if "." in media.file_name else "mkv"
        new_name = f"{new_name}.{extn}"
    
    await reply_message.delete()

    buttons = [
        [InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ", callback_data="upload_document")]
    ]
    if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
        buttons.append([InlineKeyboardButton("🎥 Vɪᴅᴇ́ᴏ", callback_data="upload_video")])
    elif file.media == MessageMediaType.AUDIO:
        buttons.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data="upload_audio")])
    
    await message.reply(
        text=f"**Sᴇ́ʟᴇᴄᴛɪᴏɴɴᴇᴢ ʟᴇ ᴛʏᴘᴇ ᴅᴇ ꜰɪᴄʜɪᴇʀ ᴅᴇ ꜱᴏʀᴛɪᴇ**\n**• Nᴏᴍ ᴅᴜ ꜰɪᴄʜɪᴇʀ :-**```{new_name}```",
        reply_to_message_id=file.id,
        reply_markup=InlineKeyboardMarkup(buttons))

# ==================================== Upload et envoi au dump ====================================

@Client.on_callback_query(filters.regex("^upload_"))
async def rename_callback(bot, query): 
    user_id = query.from_user.id
    file_name = query.message.text.split(":-")[1].strip('` ')
    file_path = f"downloads/{user_id}_{time.time()}/{file_name}"
    file = query.message.reply_to_message
    dump_channel = await db.get_dump_channel(user_id)

    sts = await query.message.edit("Tᴇ́ʟᴇ́ᴄʜᴀʀɢᴇᴍᴇɴᴛ ᴇɴ ᴄᴏᴜʀꜱ...")    
    try:
        path = await file.download(
            file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=("Dᴇ́ʙᴜᴛ ᴅᴜ ᴛᴇ́ʟᴇ́ᴄʜᴀʀɢᴇᴍᴇɴᴛ...", sts, time.time()))
    except Exception as e:
        return await sts.edit(f"**Erreur de téléchargement :** {e}")
    
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass
    
    # Préparation de la miniature et caption
    ph_path = None
    media = getattr(file, file.media.value)
    db_caption = await db.get_caption(user_id)
    db_thumb = await db.get_thumbnail(user_id)

    caption = f"**{file_name}**"
    if db_caption:
        try:
            caption = db_caption.format(
                filename=file_name,
                filesize=humanbytes(media.file_size),
                duration=convert(duration))
        except KeyError as e:
            pass  # On garde la caption par défaut

    if db_thumb or (hasattr(media, 'thumbs') and media.thumbs):
        try:
            ph_path = await bot.download_media(db_thumb or media.thumbs[0].file_id)
            with Image.open(ph_path) as img:
                img.convert("RGB").resize((320, 320)).save(ph_path, "JPEG")
        except Exception as e:
            print(f"Erreur miniature : {e}")
            ph_path = None

    # Envoi du fichier
    await sts.edit("Eɴᴠᴏɪ ᴇɴ ᴄᴏᴜʀꜱ...")
    upload_type = query.data.split("_")[1]
    
    try:
        send_method = {
            "document": bot.send_document,
            "video": bot.send_video,
            "audio": bot.send_audio
        }.get(upload_type)
        
        if not send_method:
            return await sts.edit("**❌ Type de fichier non supporté**")

        kwargs = {
            "chat_id": user_id,
            "caption": caption,
            "thumb": ph_path,
            "progress": progress_for_pyrogram,
            "progress_args": ("Uᴘʟᴏᴀᴅ ᴇɴ ᴄᴏᴜʀꜱ...", sts, time.time())
        }
        
        if upload_type == "video":
            kwargs["duration"] = duration
        elif upload_type == "audio":
            kwargs["duration"] = duration
            kwargs["title"] = os.path.splitext(file_name)[0]
            
        msg = await send_method(file_path, **kwargs)
        
        # Envoi au canal dump si configuré
        if dump_channel:
            try:
                await msg.copy(dump_channel)
                await query.message.reply("**✅ Fichier envoyé au canal dump**")
            except Exception as e:
                await query.message.reply(f"**⚠️ Échec d'envoi au canal dump :** {e}")
                
    except Exception as e:
        await sts.edit(f"**❌ Erreur d'envoi :** {e}")
    finally:
        # Nettoyage des fichiers temporaires
        for path in [file_path, ph_path]:
            try:
                if path and os.path.exists(path):
                    os.remove(path)
                    dir_path = os.path.dirname(path)
                    if os.path.exists(dir_path):
                        os.rmdir(dir_path)
            except:
                pass