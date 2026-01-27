from discord.ext import commands
import discord
import aiohttp
import io


class AddFigurinha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def AddFigurinha(self, ctx, *, nome: str = None):

        # Verifica se há attachments (imagens)
        if not ctx.message.attachments:
            await ctx.send(
                "❌ Você precisa enviar uma imagem junto com o comando!\n"
                "👉 Usa assim: `?AddFigurinha <name>` (com a imagem anexada)"
            )
            return

        # Pega o primeiro attachment
        attachment = ctx.message.attachments[0]

        # Valida se é uma imagem
        if not attachment.content_type or not attachment.content_type.startswith('image/'):
            await ctx.send("❌ O arquivo precisa ser uma imagem!")
            return

        try:
            # Baixa a imagem
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    image_data = await resp.read()

            # Define o nome da figurinha
            if nome:
                sticker_name = nome[:50]
            else:
                sticker_name = attachment.filename.split('.')[0][:50]


            # Cria a figurinha no servidor
            sticker = await ctx.guild.create_sticker(
                name=sticker_name,
                description=f"Criada por {ctx.author.name}",
                emoji="👍",
                file=discord.File(
                    io.BytesIO(image_data),
                    filename=attachment.filename
                )
            )



            await ctx.send(f"✅ Figurinha criada com sucesso! {sticker.name}")

            await ctx.send("❌ Eu não tenho permissão para criar figurinhas neste servidor.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Erro ao criar figurinha: {e}")
        except Exception as e:
            await ctx.send(f"❌ Algo deu errado: {e}")


    @AddFigurinha.error
    async def addfigurinha_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("😅 Esse comando é só pra admin, foi mal.")

async def setup(bot):
    await bot.add_cog(AddFigurinha(bot))