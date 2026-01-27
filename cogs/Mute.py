from discord.ext import commands
import discord
import asyncio

class Mute(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot


    @commands.command()
    async def mute(self, ctx, member: discord.Member, duration: str):
        muterole = 1465423902938235056
        if not duration.isdigit():
            await ctx.send("Por favor, insira o tempo em segundos.")
            return
        seconds = int(duration)
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("Você não tem permissão para usar este comando.")
            return
        mute_role_id = 1465423902938235056
        mute_role = ctx.guild.get_role(mute_role_id)
        await member.add_roles(mute_role)
        embed = discord.Embed(
            title="🔇 Usuário Mutado!",
            description=f"{member.mention} foi mutado por {seconds} segundos.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Por: {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        await asyncio.sleep(seconds)
        await member.remove_roles(mute_role)
        embed = discord.Embed(
            title="🔊 Usuário Desmutado!",
            description=f"{member.mention} foi desmutado.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        muterole = 1465423902938235056
        if ctx.author.guild_permissions.administrator:
            await member.remove_roles(ctx.guild.get_role(muterole))
            embed = discord.Embed(
                title="🔊 Usuário Desmutado!",
                description=f"{member.mention} foi desmutado.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Por: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            param = error.param.name

            if param == "member":
                await ctx.send(
                    "😅 Faltou marcar o usuário.\n"
                    "👉 Usa assim: `?mute @usuario <segundos>`"
                )
            elif param == "duration":
                await ctx.send(
                    "😅 Faltou o tempo do mute.\n"
                    "👉 Usa assim: `?mute @usuario <segundos>`"
                )

        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "😅 Usuário inválido.\n"
                "👉 Usa assim: `?mute @usuario <segundos>`"
            )


    
async def setup(bot):
    await bot.add_cog(Mute(bot))