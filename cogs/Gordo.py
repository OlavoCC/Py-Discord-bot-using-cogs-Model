from discord.ext import commands
import discord

class Gordo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "gordo" in message.content.lower():
            await message.channel.send("<@934192654491721768> <@756276938645176463> <@757402128502489218> <@525292825093472260> ")

async def setup(bot):
    await bot.add_cog(Gordo(bot))