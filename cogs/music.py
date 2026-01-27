from discord.ext import commands
import discord
from utils.ytdlp import YTDLSource
import asyncio


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}  # guild_id -> list

    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        return self.queues[guild_id]

    async def play_next(self, ctx):
        queue = self.get_queue(ctx.guild.id)

        if not queue:
            return

        vc = ctx.voice_client
        source = queue.pop(0)

        vc.play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx), self.bot.loop
            )
        )

        embed = discord.Embed(
            title="🎶 Tocando agora",
            description=source.title,
            color=discord.Color.green()
        )

        if source.thumbnail:
            embed.set_thumbnail(url=source.thumbnail)

        await ctx.send(embed=embed)

    @commands.command()
    async def play(self, ctx, *, busca: str):
        if not ctx.author.voice:
            return await ctx.send("❌ Entra numa call primeiro, campeão")

        channel = ctx.author.voice.channel

        if not ctx.voice_client:
            vc = await channel.connect()
        else:
            vc = ctx.voice_client

        await ctx.send(f"🔍 Buscando: `{busca}`"

        try:
            source = await YTDLSource.from_url(
                busca, loop=self.bot.loop, stream=True
            )
        except Exception as e:
            return await ctx.send(f"💥 Erro ao buscar áudio:\n```{e}```")

        queue = self.get_queue(ctx.guild.id)
        queue.append(source)

        if not vc.is_playing():
            await self.play_next(ctx)
        else:
            await ctx.send(
                f"✅ **Adicionada à fila:** `{source.title}`\n"
                f"📊 Posição: {len(queue)}"
            )

    @commands.command()
    async def leave(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("❌ Nem estou em call, chefia")

        self.queues.pop(ctx.guild.id, None)
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Saí da call e limpei a fila")


async def setup(bot):
    await bot.add_cog(Music(bot))
