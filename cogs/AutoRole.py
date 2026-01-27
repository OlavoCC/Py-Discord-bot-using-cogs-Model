from discord.ext import commands
import discord

class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role_id = 1277443066596294760
        role = member.guild.get_role(role_id)

        if not role:
            print("Role não encontrada")
            return
        try:
            await member.add_roles(role, reason="Autorole")
            print(f"Assigned role {role.name} to {member.name}")
        except discord.Forbidden:
            print("Sem permissão para adicionar a role")
        except Exception as e:
            print(f"Erro ao dar autorole: {e}")

            
async def setup(bot):
    await bot.add_cog(AutoRole(bot))