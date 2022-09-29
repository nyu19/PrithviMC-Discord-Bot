import discord, json
from datetime import datetime
from discord.ext import commands
from discord.commands import slash_command,message_command,user_command
config = json.load(open('./config.json','r'))


class Spy(commands.Cog):
    def __init__(self,bot: discord.Bot):
        self.bot = bot
        self.channel_Id = config["SPY"]["CONSOLE_ID"]
        self.spy_user = config["SPY"]["SPY_USER_ID"]

    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        if(message.author == self.bot.user or len(message.attachments)>0):
            return 
        
        if(message.channel.id==self.channel_Id):
            embed=discord.Embed(title="📟 Console Spy", description=f"`{message.content}`", color=discord.Color.yellow(), timestamp=datetime.now())
            embed.set_footer(text=message.author,icon_url=message.author.avatar)
            
            await self.bot.get_user(self.spy_user).send(embed=embed)

def setup(bot):
    bot.add_cog(Spy(bot))