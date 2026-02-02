from discord.ext import commands
import discord

class VoiceRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        canal_exilio = member.guild.get_channel(1251289842344792228)
        if canal_exilio is None:
            return

    # Se tentou sair do exílio
        if before.channel == canal_exilio and after.channel != canal_exilio:
            await member.move_to(canal_exilio)


    @commands.command()
    async def vr(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("Você não tem permissão para usar este comando.")
            return

        if not member.voice or not member.voice.channel:
            await ctx.send("Essa pessoa não está conectada em um canal de voz.")
            return

        canal = ctx.guild.get_channel(1251289842344792228)
        if canal is None:
            await ctx.send("Canal de exílio não encontrado.")
            return

        await member.move_to(canal)
        await ctx.send(f"{member.mention} foi exilado 😈")


    
    
async def setup(bot):
    await bot.add_cog(VoiceRoulette(bot))