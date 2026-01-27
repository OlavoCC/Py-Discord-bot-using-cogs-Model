from discord.ext import commands
import discord

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """Mostra o avatar de um usuário mencionado."""
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title="🖼️ Avatar",
            description=f"Usuário: {member.mention} <:PepeUlala:1465419624907538524>",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Pedido por {ctx.author}", icon_url=ctx.author.display_avatar.url)
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Avatar(bot))