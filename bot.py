import discord
from pathlib import Path
from itertools import cycle
from decouple import config
from discord.ext import commands, tasks

intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)

bot = commands.Bot(command_prefix='!', intents=intents)
bot_status = cycle(['Programming', 'Debugging'])


@bot.event
async def on_ready():
    change_status.start()
    print('Bot is ready.')


@tasks.loop(seconds=120)
async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next(bot_status)))


@bot.event
async def on_member_join(member):
    print(f'{member} has joined the guild, say hello!')


@bot.event
async def on_member_remove(member):
    print(f'{member} has left the guild, bye bye!')


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

paths = list(Path('cogs').rglob('*.py'))
for filename in paths:
    bot.load_extension(f'cogs.{filename.stem}')

bot.run(config('DISCORD_TOKEN'))
