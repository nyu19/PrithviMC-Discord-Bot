from click import command
import discord
from discord.ext import commands
from discord.commands import slash_command,message_command,user_command

class welcome(commands.Cog):
    def __init__(self,bot :discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        self.bot.get_channel()

    

def setup(bot):
    bot.add_cog(welcome(bot))