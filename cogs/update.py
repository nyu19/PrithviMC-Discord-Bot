import discord
from discord.ext import commands
from discord.ui import Button,View
from discord.commands import slash_command,message_command,user_command
import json
from datetime import datetime
config = json.load(open('./config.json','r'))

#1009758166818508832 channel Bot 2

class serverUpdates(commands.Cog):
    def __init__(self,bot:discord.Bot):
        self.channel_Id=config["UPDATE"]["CHANNEL_ID"]
        self.tag=config["ROLES"]["DEVELOPMENT"]
        self.bot = bot
    
    
    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        
        if(message.author == self.bot.user or len(message.attachments)>0):
            return 
        
        if(message.channel.id==self.channel_Id):
            
            embed=discord.Embed(title="📑 Updates", description=message.content, color=0x36a0e2, timestamp=datetime.now())
            embed.set_footer(text=message.author,icon_url=message.author.avatar)
            await message.delete()
            await message.channel.send(content=f"||<@&{self.tag}>||",embed=embed)
        
            
            
        
def setup(bot):
    bot.add_cog(serverUpdates(bot))