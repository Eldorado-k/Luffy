import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # Configuration client Pyro
    API_ID = os.environ.get("API_ID", "24817837")
    API_HASH = os.environ.get("API_HASH", "acd9f0cc6beb08ce59383cf250052686")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8183564006:AAFuWtGxfO_zpU7DGLetb_218Mu10Dr1gVQ") 
   
    # Configuration base de données
    DB_NAME = os.environ.get("DB_NAME", "Aniflix")     
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://Aniflix:Lipun123@aniflix.q2wina5.mongodb.net/?retryWrites=true&w=majority&appName=Aniflix")
 
    # Autres configurations
    BOT_UPTIME = time.time()
    START_PIC  = os.environ.get
      ("START_PIC", "https://iili.io/Fc0oBrF.md.jpg")
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '7428552084').split()]
    FORCE_SUB = os.environ.get("FORCE_SUB", "otakukingcey1") 
    LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1002757788052")
    MAX_CONCURRENT_TRANSMISSIONS = int(os.environ.get("MAX_CONCURRENT_TRANSMISSIONS", "2"))
    
    # Configuration support web
    WEB_SUPPORT = bool(os.environ.get("WEB_SUPPORT", "True"))


class Txt(object):
    # Messages texte
    START_TXT = """<b>Salut {} 👋,</b>
<b>Jᴇ sᴜɪs ʟᴇ ʀᴇɴᴀᴍᴇʀ ʙᴏᴛ 🦜 ᴄᴀᴘᴀʙʟᴇ ᴅ'ᴀʟʟᴇʀ à ᴜɴᴇ ᴠɪᴛᴇssᴇ ᴅᴇ 𝟷𝟹Mᴏ/s 🚀

Lᴀ ғᴀçᴏɴ ᴅᴏɴᴛ ᴊᴇ ᴍᴇ sᴀᴄʀɪғɪᴇ ᴘᴏᴜʀ ᴍᴏɴ éǫᴜɪᴘᴀɢᴇ ⚓, Jᴇ ғᴇʀᴀɪ ᴅᴇ ᴍêᴍᴇ ᴘᴏᴜʀ ᴛᴇs ғɪᴄʜɪᴇʀs 📂. Sᴏɪᴛ ᴇɴ sûʀ. Mêᴍᴇ sɪ ᴍᴏɴ ᴇsᴛᴏᴍᴀᴄ ғᴀɪᴛ ᴅᴇs ʙʀᴜɪᴛs ᴅᴇ ᴍᴏᴛᴇᴜʀ, sᴀᴄʜᴇᴢ Qᴜᴇ, 

Jᴇ ᴛʀᴏᴜᴠᴇʀᴀɪ ʟᴇ Oɴᴇ ᴘɪᴇᴄᴇ 🏴‍☠️ ᴅᴇ ᴠᴏs ғɪᴄʜɪᴇʀs, ᴇᴛ Lᴇ ᴘʀᴏᴄʜᴀɪɴ ʀᴏɪ ᴅᴇs Pɪʀᴀᴛᴇs 🏆, ᴄᴇ sᴇʀᴀ Mᴏɪ 🍖.</b>


<blockquote><b>Créé par :</b> <a href="https://t.me/BotZFlix">BotZFlix</a></blockquote> 💞"""

    ABOUT_TXT = """<b>╔════❰ Lᴜғғʏ Rᴇɴᴀᴍᴇʀ Bᴏᴛ ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼📃Mᴏɴ Nᴏᴍ : {}
║┣⪼👼Cʀᴇᴀᴛᴇᴜʀ : <a href='t.me/ZFlixteamBot>—‌‌‌‌◡‌⃝ㅤ🇰ιηg¢єу</a>
║┣⪼🤖Mɪsᴇ à Jᴏᴜʀ : <a href='t.me/BotZFlix'>BᴏᴛZFʟɪx</a>
║┣⪼📡 Héʙᴇʀɢᴇʀ Sᴜʀ: Sᴜᴘᴇʀ Fᴀsᴛ
║┣⪼🗣️Lᴀɴɢᴜᴀɢᴇ : <a href='python.org'>Pʏᴛʜᴏɴ𝟹</a>
║┣⪼📚 Lɪʙʀᴀɪʀɪᴇ : <a href='pyrogram.org'>Pʏʀᴏɢʀᴀᴍ</a>
║┣⪼🗒️Vᴇʀsɪᴏɴ : 𝟶.𝟷𝟾.𝟹
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪<b>"""

    HELP_TXT = """

✏️ <b><u>Renommage de fichiers</u></b>
<b>•»</b> Envoyez un fichier et spécifiez le nouveau nom
<b>•»</b> Sélectionnez le format [document, video, audio]

🔧 <b>Support :</b> <a href="https://t.me/BotZFlixSupport">Groupe d'aide</a>"""

    LEG_TXT = """📝 <b><u>Configuration des légendes</u></b>
<b>•»</b> /set_caption - Définir une légende personnalisée
<b>•»</b> /see_caption - Voir votre légende actuelle
<b>•»</b> /del_caption - Supprimer votre légende"""

    THUMB_TXT = """🌟 <b><u>Configuration de la miniature</u></b>
  
<b>•»</b> /start - Démarrez le bot et envoyez une photo pour définir la miniature
<b>•»</b> /del_thumb - Supprimer votre miniature actuelle
<b>•»</b> /view_thumb - Voir votre miniature actuelle"""

    ZFT_TXT = """<b><u>⛔️⛔️⛔️MESSAGE URGENT‼️‼️‼️ </u>

Rejoignez Notre Groupe de film & de séries. Dans ce groupe, il faut juste écrire le nom du film ou de la série, pour le recevoir

<u>EXEMPLE:</u>

<code>Loki 
Warrior
Hulk
Squid Game</code>

En écrivant le nom, Un bot va vous l'envoyé. il faut et seulement écrire le nom du film.


<a href='t.me/ZFlixTeam'>Rejoindre le groupe</a>
<a href='t.me/ZFlixTeam'>Rejoindre le groupe</a>
<a href='t.me/ZFlixTeam'>Rejoindre le groupe</a>


pour tout Problème contactez moi : <a href='t.me/ZFlixTeamBot'>◡̈⃝ㅤ🇰ιηg¢єу</a></b>"""

    PROGRESS_BAR = """<b>
╔━━━━❰ Gᴏᴍᴜ Gᴏᴍᴜ Nᴏ🔥 ❱━╗ 
 ➜ 🗃️ Tᴀɪʟʟᴇ : {1} | {2}
 ➜ ⏳ Tᴇʀᴍɪɴé : {0}%
 ➜ 🚀 Vɪᴛᴇssᴇ : {3}/s
 ➜ ⏰ Rᴇsᴛᴀɴᴛ : {4}
╚━━━━━━━━━━━━━━━╝
<blockquote><a href='t.me/ZFlixTeam'>𒄆  ZFʟɪx-Tᴇᴀᴍ</a></blockquote></b>"""