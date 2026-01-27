from discord.ext import commands
import discord

class clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount: int):
        id1 = 756276938645176463
        id2 = 757402128502489218
        if ctx.author.id == id1 or ctx.author.id == id2:
            if amount < 5:
                await ctx.send("O número mínimo de mensagens para apagar é 5.")
                return
            await ctx.channel.purge(limit=amount + 1)
            embed = discord.Embed(
                title="🧹 Limpeza concluída!",
                description=f"🗑️ {amount} mensagens foram apagadas.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Por: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)


    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            param = error.param.name

            if param == "amount":
                await ctx.send(
                    "😅 Faltou o número de mensagens a serem apagadas.\n"
                    "👉 Usa assim: `?clear <número>`"
                )

        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "😅 Número inválido.\n"
                "👉 Usa assim: `?clear <número>`"
            )
async def setup(bot):
    await bot.add_cog(clear(bot))