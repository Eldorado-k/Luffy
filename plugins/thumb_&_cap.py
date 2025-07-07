from pyrogram import Client, filters 
from helper.database import db

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    if len(message.command) == 1:
       return await message.reply_text("**__Donne une nouvelle histoire (legende)__\n\nExemple:- `/set_caption {filename}\n💾 Taille: {filesize}\n⏰ Durée: {duration}`**")
    caption = message.text.split(" ", 1)[1]
    try:
        caption.format(filename='', filesize='', duration='')
    except KeyError as e:
        await message.edit(f"**Mauvaise clé : {e} \nEssayez à nouveau**")
    await db.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("__**✅ Légende enregistrée**__")
   
@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if not caption:
       return await message.reply_text("__**😔 Vous n'avez aucune légende**__")
    await db.set_caption(message.from_user.id, caption=None)
    await message.reply_text("__**❌️ Légende supprimée**__")
                                       
@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if caption:
       await message.reply_text(f"**Votre légende:-**\n\n`{caption}`")
    else:
       await message.reply_text("__**😔 Vous n'avez aucune légende**__")


@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):    
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(chat_id=message.chat.id, photo=thumb)
    else:
        await message.reply_text("😔 __**Vous n'avez aucune miniature**__") 
		
@Client.on_message(filters.private & filters.command(['del_thumb', 'delthumb']))
async def removethumb(client, message):
    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("❌️ __**Miniature supprimée**__")
	
@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    mkn = await message.reply_text("Veuillez patienter...")
    await db.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await mkn.edit("✅️ __**Miniature enregistrée**__")