import os
import discord
from discord.ext import commands
import mss
from PIL import Image
import asyncio

# Lit le token depuis token.txt dans le même dossier
def load_token():
    token_path = os.path.join(os.path.dirname(__file__), "token.txt")
    if not os.path.isfile(token_path):
        raise FileNotFoundError(f"Le fichier token.txt est introuvable dans {token_path}.")
    with open(token_path, "r", encoding="utf-8") as f:
        token = f.read().strip()
    if not token:
        raise ValueError("token.txt est vide — colle le token de ton bot dedans.")
    return token

TOKEN = load_token()

intents = discord.Intents.default()
# si tu veux que le bot lise le contenu des messages (commande texte), active ceci dans le dev portal
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def take_screenshot(path="screenshot.png"):
    with mss.mss() as sct:
        # sct.monitors[1] = écran principal
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        # conversion correcte BGRA -> RGB
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save(path)
        return path

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user} (id: {bot.user.id})")

@bot.command(name="screenshot")
async def screenshot(ctx):
    try:
        await ctx.send("📸 Capture de l'écran en cours...")
        path = take_screenshot("screenshot.png")
        # envoyer le fichier
        await ctx.send(file=discord.File(path))
        # optionnel : supprimer le screenshot local après envoi
        try:
            os.remove(path)
        except OSError:
            pass
    except Exception as e:
        await ctx.send(f"❌ Erreur lors de la capture : {e}")
        raise

if __name__ == "__main__":
    # run blocking
    bot.run(TOKEN)
