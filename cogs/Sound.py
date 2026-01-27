from discord.ext import commands
import discord
import os

class Sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def Baiacu(self, ctx):
        # 1️⃣ Verifica se o usuário tá numa call
        if not ctx.author.voice:
            await ctx.send("❌ Tu precisa estar numa call pra usar isso 😅")
            return

        channel = ctx.author.voice.channel

        # 2️⃣ Conecta (ou reutiliza)
        if ctx.voice_client:
            vc = ctx.voice_client
        else:
            vc = await channel.connect()

        # 3️⃣ Caminho do áudio
        audio_path = "sounds/teste.mp3"

        if not os.path.exists(audio_path):
            await ctx.send("❌ Áudio não encontrado.")
            return

        # 4️⃣ Cria a fonte de áudio (FFmpeg)
        source = discord.FFmpegPCMAudio(
            audio_path,
            executable="/usr/bin/ffmpeg"
        )

        # 5️⃣ Toca o áudio
        vc.play(source)

        await ctx.send("🎶 Tocando o som!")

async def setup(bot):
    await bot.add_cog(Sound(bot))
