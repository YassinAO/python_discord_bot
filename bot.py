import discord
from discord.ext import commands
from decouple import config

intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.event
async def on_member_join(member):
    print(f'{member} has joined the guild, say hello!')


@bot.event
async def on_member_remove(member):
    print(f'{member} has left the guild, bye bye!')

bot.run(config('DISCORD_TOKEN'))
