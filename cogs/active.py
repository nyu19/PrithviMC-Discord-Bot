import discord
from discord.ext import commands,tasks
from discord.commands import slash_command,message_command,user_command
import json
config = json.load(open("./config.json",'r'))


class Active_Dev(commands.Cog):
    def __init__(self,bot: discord.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.active_reminder.start()


    @tasks.loop(hours=14*24)
    async def active_reminder(self):
        owner = await self.bot.get_or_fetch_user(config['BOT_OWNER_ID'])
        
        await owner.send(embed=discord.Embed(title="**Ayo, Active Developer Cheeeeckkk!!**",description=f"</active:{self.bot.get_application_command(name='active').id}>"))


    @commands.slash_command(description="Worship the Owner 🛐")
    @commands.is_owner()
    async def active(self,ctx: discord.ApplicationContext):
        await ctx.respond(embed=discord.Embed(title="**Ayo, Active Developer Cheeeeckkk!!**",description=f"</active:{self.bot.get_application_command(name='active').id}>"))
        
    


    

def setup(bot):
    bot.add_cog(Active_Dev(bot))