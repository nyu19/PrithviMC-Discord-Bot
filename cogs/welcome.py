from datetime import datetime
import discord
from discord.ext import commands
from discord.commands import slash_command,message_command,user_command
import json
config = json.load(open('config.json', 'r'))

class welcome(commands.Cog):
    def __init__(self,bot :discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try: 
            avatar_url = member.avatar.url 
        except AttributeError:
            avatar_url = member.default_avatar.url
        
        em = discord.Embed(
            title=f"Welcome __**{member.name}**__ to Prithvi MC!!!",
            description=f"""Hi! {member.mention}, Welcome to Prithvi MC's Discord Server!

> **⟫** Visit <#972911505135796244> for more Info about the server!
> **⟫** Be sure to checkout <#747433678468022283>!
> **⟫** You can reach out to staff using <#972905726446039141>""",
            color=discord.Color.from_rgb(91, 235, 192),
            timestamp=datetime.now()
        )
        em.add_field(name="**IP**", value="`play.prithvimc.tk`")
        if (config["WELCOME"]["USE_WELCOME_AVATAR"] == True):
            em.set_thumbnail(url=avatar_url)
        em.set_image(url=config['WELCOME']['WELCOME_BANNER_URL'])


        await self.bot.get_channel(config['WELCOME']['CHANNEL_ID']).send(content=f"||{member.mention}||",embed=em)
        
def setup(bot):
    bot.add_cog(welcome(bot))