from datetime import datetime
import discord,re
from discord.ext import commands,pages
from discord.commands import slash_command,message_command,user_command
from mctools import PINGClient,formattertools
import json
config = json.load(open('./config.json','r'))

def giveServerStatus():
    try:
        pinger = PINGClient(config['SERVER_IP'])
        data = pinger.get_stats()
        data.pop('favicon')

        ansi = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        motd = ansi.sub('', data['description']).replace("  ",'')
        players = f"{data['players']['online']}/{data['players']['max']}"

        embed = discord.Embed(title="**Prithvi MC Status**",color=discord.Color.green(),timestamp=datetime.now())
        embed.add_field(name="**IP**",value=f"`play.prithvimc.tk`")
        embed.add_field(name="**Version**",value=f"`{config['VERSION']}`")
        embed.add_field(name="**Player Online**",value=f"`{players}`")
        embed.add_field(name="**MOTD**",value=f"```{motd}```",inline=False)
        embed.add_field(name="**Ping**",value=f"`{int(data['time'])} ms`",inline=False)
        
    except Exception: 
        embed = discord.Embed(
            title="**Prithvi MC Status**",
            description="Server is **Offline!** Please Try again later.",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
    pinger.stop()
    return embed

class RefreshButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Refresh",style=discord.ButtonStyle.blurple,custom_id="kekw", emoji="🔄")
    async def button_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=giveServerStatus(),view=self)

class serverPinger(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RefreshButton())

    @commands.slash_command(description="Status!")
    @discord.default_permissions(administrator=True)
    async def status(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        await ctx.send(embed=giveServerStatus(),view=RefreshButton())
        await ctx.respond(content="Done!",delete_after=5)





def setup(bot):
    bot.add_cog(serverPinger(bot))