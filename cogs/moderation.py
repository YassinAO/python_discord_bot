import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation cog is ready')

    @commands.command()
    @commands.has_role('Moderator')
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

    @commands.command()
    @commands.has_role('Moderator')
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command()
    @commands.has_role('Moderator')
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} was kicked from server, bye bye!')

    @commands.command()
    @commands.has_role('Moderator')
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} was banned from server, bye bye!')

    @commands.command()
    @commands.has_role('Moderator')
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for banned_user in banned_users:
            user = banned_user.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} was unbanned from the server, welcome back!')
                return


def setup(bot):
    bot.add_cog(Moderation(bot))
