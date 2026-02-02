from discord.ext import commands
import discord
from utils.ytdlp import YTDLSource
import asyncio
from async_timeout import timeout

class VoiceState:
    def __init__(self, bot):
        self.bot = bot
        self.current = None
        self.next = asyncio.Event()
        self.songs = []
        self.volume = 0.25
        self.channel = None  # Para embeds
        self.audio_player = None

    def set_channel(self, channel):
        self.channel = channel

    async def start_audio_player(self, ctx):
        self.channel = ctx.channel
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    async def audio_player_task(self):
        while True:
            self.next.clear()
            if not self.songs:
                try:
                    async with timeout(180):
                        await self.next.wait()
                except asyncio.TimeoutError:
                    await self.stop()
                    return
            self.current = self.songs.pop(0)
            self.current.volume = self.volume
            self.voice.play(self.current, after=self.play_next_song)
            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            print(f'Erro no player: {error}')
        self.next.set()

    def skip(self):
        self.voice.stop()
        self.play_next_song()  # Trigger manual pro next

    async def stop(self):
        """Stop corrigido"""
        self.songs.clear()
        if self.audio_player:
            self.audio_player.cancel()
        if hasattr(self, 'voice') and self.voice:
            try:
                await self.voice.disconnect()
            except:
                pass  # Ignora erro de disconnect

    def _create_embed(self, title, desc, color=discord.Color.green()):
        embed = discord.Embed(title=title, description=desc, color=color)
        if hasattr(self.current, 'thumbnail') and self.current.thumbnail:
            embed.set_thumbnail(url=self.current.thumbnail)
        embed.set_footer(text="Botzin do Contessotto")
        return embed
    
    def set_volume(self, volume):
        """Aplica volume IMEDIATO na música atual + futuras"""
        self.volume = volume
        if self.current:
            self.current.volume = volume
        print(f"Volume setado: {volume}")  # Debug

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx):
        gid = ctx.guild.id
        if gid not in self.voice_states:
            self.voice_states[gid] = VoiceState(self.bot)
        return self.voice_states[gid]

    async def ensure_voice(self, ctx):
        if not ctx.author.voice:
            return await ctx.send("❌ Entra na call!")
        if not ctx.voice_client:
            vc = await ctx.author.voice.channel.connect()
            state = self.get_voice_state(ctx)
            state.voice = vc
            await state.start_audio_player(ctx)

    @commands.command()
    async def join(self, ctx):
        await self.ensure_voice(ctx)

    @commands.command()
    async def play(self, ctx, *, busca: str):
        state = self.get_voice_state(ctx)
        await self.ensure_voice(ctx)

        try:
            source = await YTDLSource.from_url(busca, loop=self.bot.loop, stream=True)
        except Exception as e:
            return await ctx.send(f"💥 Erro: ```{str(e)[:100]}```")

    # ✅ CORREÇÃO: Verifica SE JÁ TÁ TOCANDO antes de calcular posição
        is_playing = state.voice and state.voice.is_playing()
        pos = len(state.songs) + 1 if not is_playing else len(state.songs) + 1

        state.songs.append(source)

        if not is_playing:  # Se NÃO tava tocando
            embed = discord.Embed(
                title="<a:Virus:1466534011873661070> **TOCANDO AGORA**", 
                description=f"**{source.title}**",
                color=0x1db954
            )
            if hasattr(source, 'thumbnail') and source.thumbnail:
                embed.set_thumbnail(url=source.thumbnail)
            embed.set_footer(text="Botzin do Contessotto • Sexy Music 🔥")
            await ctx.send(embed=embed)
            state.next.set()
        else:  # Se JÁ tava tocando → fila
            embed = discord.Embed(
                title="➕ **ADICIONADO À FILA**",
                description=f"**{source.title}**\n`{pos}º na fila`",
                color=0x5865f2
            )
            if hasattr(source, 'thumbnail') and source.thumbnail:
                embed.set_thumbnail(url=source.thumbnail)
            embed.set_footer(text=f"Botzin do Contessotto • {len(state.songs)} na fila")
            await ctx.send(embed=embed)



    @commands.command()
    async def np(self, ctx):
        state = self.get_voice_state(ctx)
        if state.current and state.current.title:
            embed = state._create_embed("🎵 Tocando agora", state.current.title)
        else:
            embed = discord.Embed(title="⏹️ Nada tocando", color=discord.Color.red())
            embed.set_footer(text="Botzin do Contessotto")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        state = self.get_voice_state(ctx)
        if state.voice and state.voice.is_playing():
            state.skip()
            await ctx.send("⏭️ Skipado!")
        else:
            await ctx.send("❌ Nada tocando!")

    @commands.command()
    async def queue(self, ctx):
        state = self.get_voice_state(ctx)
        if not state.songs:
            return await ctx.send("📭 Fila vazia!")
        qlist = "\n".join([f"{i+1}. {s.title[:40]}..." for i, s in enumerate(state.songs[:10])])
        embed = discord.Embed(title="📋 Fila (Próximas 10)", description=qlist, color=discord.Color.blue())
        embed.set_footer(text=f"Total: {len(state.songs)} | Botzin do Contessotto")
        await ctx.send(embed=embed)

    @commands.command()
    async def pause(self, ctx):
        state = self.get_voice_state(ctx)
        if state.voice and state.voice.is_playing():
            state.voice.pause()
            await ctx.send("⏸️ Pausado!")

    @commands.command()
    async def resume(self, ctx):
        state = self.get_voice_state(ctx)
        if state.voice and state.voice.is_paused():
            state.voice.resume()
            await ctx.send("▶️ Resumido!")

    @commands.command()
    async def volume(self, ctx, vol: int = None):
        state = self.get_voice_state(ctx)
        if vol is not None and 0 <= vol <= 100:
            volume = vol / 100.0
            state.set_volume(volume)  # Usa novo método
            embed = discord.Embed(title="🔊 Volume alterado", 
                                description=f"**{vol}%** (aplicado agora!)", 
                                color=discord.Color.gold())
            await ctx.send(embed=embed)
        else:
            atual = int(state.volume * 100)
            embed = discord.Embed(title="📢 Volume atual", 
                                description=f"**{atual}%**", 
                                color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name='dc')
    async def leave(self, ctx):
        gid = ctx.guild.id
        if gid in self.voice_states:
            state = self.voice_states[gid]
            state.channel = ctx.channel  # Para mensagens finais
            await state.stop()
            del self.voice_states[gid]
        
        if ctx.voice_client:
            await ctx.voice_client.cleanup()
            await ctx.send("👋 Saí da call e limpei tudo!")
        else:
            await ctx.send("❌ Não estava em call!")
async def setup(bot):
    await bot.add_cog(Music(bot))
