import discord
from discord.ext import commands
import re
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="§", intents=intents)

ALLOWED_PATTERNS = [
    "tenor.com",
    "youtube.com",
    "youtu.be",
    "spotify.com",
    "soundcloud.com",
    "deezer.com"
]

url_regex = re.compile(r'https?://[^\s]+')

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    urls = url_regex.findall(message.content)
    if urls:
        for url in urls:
            if not any(pattern in url for pattern in ALLOWED_PATTERNS):
                try:
                    await message.delete()
                    print(f"❌ Message supprimé de {message.author} contenant un lien interdit.")
                except discord.Forbidden:
                    print("🚫 Permissions insuffisantes pour supprimer le message.")
                break
            elif "tenor.com" in url:
                try:
                    await message.delete()
                    embed = discord.Embed(color=discord.Color.purple())
                    embed.set_image(url=url)
                    embed.set_footer(text=f"GIF partagé par {message.author.display_name}")
                    await message.channel.send(embed=embed)
                except discord.Forbidden:
                    print("🚫 Permissions insuffisantes pour envoyer un embed.")
                break

    await bot.process_commands(message)

bot.run(TOKEN)

