# Discord bot v1.1 by Pizzaz
from discord.ext import commands
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(command_prefix='.')
    bot.load_extension("Cogs.UtilitiesCog")
    bot.load_extension("Cogs.SteamCog")
    bot.load_extension("Cogs.YoutubeCog")


    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')


    bot.run(TOKEN)
