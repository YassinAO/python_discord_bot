import discord
from discord.ext import commands
from decouple import config


class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def lvl_up(self, user):
        cur_xp = user['xp']
        cur_lvl = user['lvl']

        if cur_xp >= round((4 * (cur_lvl ** 3)) / 5):
            await self.bot.pg_con.execute('UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id = $3', cur_lvl + 1, user['user_id'], user['guild_id'])
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_ready(self):
        print('Level cog is ready')

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = await self.bot.pg_con.fetch('SELECT * FROM users WHERE user_id = $1 AND guild_id = $2', author_id, guild_id)

        if not user:
            await self.bot.pg_con.execute('INSERT INTO users (user_id, guild_id, lvl, xp) VALUES ($1, $2, 1, 0)', author_id, guild_id)

        user = await self.bot.pg_con.fetchrow('SELECT * FROM users WHERE user_id = $1 AND guild_id = $2', author_id, guild_id)

        await self.bot.pg_con.execute('UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3', user['xp'] + 1, author_id, guild_id)

        if self.lvl_up(user):
            await message.channel.send(f"{message.author.mention} has reached level {user['lvl'] + 1}")

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.bot.pg_con.fetch('SELECT * FROM users WHERE user_id = $1 AND guild_id = $2', member_id, guild_id)

        if not user:
            await ctx.send('Member doesn\'t have a level')
        else:
            embed = discord.Embed(color=member.color,
                                  timestamp=ctx.message.created_at)

            embed.set_author(
                name=f'Level - {member}', icon_url=self.bot.user.avatar_url)

            embed.add_field(name='Level', value=user[0]['lvl'])
            embed.add_field(name='XP', value=user[0]['xp'])

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Level(bot))
