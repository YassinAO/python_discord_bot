import discord
from discord.ext import commands
from decouple import config

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot is ready.')

client.run(config('DISCORD_TOKEN'))
