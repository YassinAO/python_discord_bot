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


@bot.command()
@commands.has_role('Moderator')
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')


@bot.command()
@commands.has_role('Moderator')
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)


@bot.command()
@commands.has_role('Moderator')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} was kicked from server, bye bye!')


@bot.command()
@commands.has_role('Moderator')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} was banned from server, bye bye!')


@bot.command()
@commands.has_role('Moderator')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for banned_user in banned_users:
        user = banned_user.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} was unbanned from the server, welcome back!')
            return

bot.run(config('DISCORD_TOKEN'))
