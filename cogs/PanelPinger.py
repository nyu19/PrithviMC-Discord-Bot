from datetime import datetime
import discord,requests
from discord.ext import commands,pages
from discord.commands import slash_command,message_command,user_command
import json
import utils.sizeUtils as szu
config = json.load(open('./config.json','r'))

def parseStatus(st:str):
    st = st.lower()
    if st == 'running':
        return '`🟢`'
    elif st == 'starting':
        return '`🟡`'
    else :
        return '`🔴`'


def giveServerStatus() -> discord.Embed:
    embed = discord.Embed(
        title="**Panel Server Status**",
        color=discord.Color.from_rgb(59, 130, 246),
        timestamp=datetime.now(),
    )
    fp = open('PanelCache.json','r')
    list_of_servers = list(json.load(fp))
    fp.close()
    header = {
        "Accept" : "application/json",
        "Content-Type":"application/json",
        "Authorization":f"Bearer {config['PANEL']['API_TOKEN']}"
    }
    for i in list_of_servers:
        i = dict(i)

        data = requests.get(f'{config["PANEL"]["URL"]}/api/client/servers/{i["id"]}/resources',headers=header).json()['attributes']
        # print(data)

        embed.add_field(name=f"**{i['name']}**",value=f"""**Status:** {parseStatus(str(data['current_state']))}
**Memory:** `{szu.converter(data['resources']['memory_bytes'])} / {i['limits']['memory']}`
**Disk:** `{szu.converter(data['resources']['disk_bytes'])} / {i['limits']['disk']}` 
**CPU:** `{data['resources']['cpu_absolute']} / {i['limits']['cpu']} %`
""")


    
    return embed

class RefreshButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Refresh",style=discord.ButtonStyle.blurple,custom_id="panelstats", emoji="🔄")
    async def button_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=giveServerStatus(),view=self)

class PanelPinger(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RefreshButton())

    @commands.slash_command(description="Status!")
    @discord.default_permissions(administrator=True)
    async def panelstatus(self, ctx: discord.ApplicationContext):
        dumpdict = []
        header = {
            "Accept" : "application/json",
            "Content-Type":"application/json",
            "Authorization":f"Bearer {config['PANEL']['API_TOKEN']}"
        }
        data = requests.get(config["PANEL"]["URL"] + "/api/application/servers",headers=header).json()
        # print(data)
        for i in data["data"]:
            o = i['attributes']
            dumpdict.append({
                "id": str(o['identifier']),
                "name": str(o['name']),
                "limits": {
                    "memory": szu.mbconverter(o['limits']['memory']),
                    "disk": szu.mbconverter(o['limits']['disk']),
                    "cpu": o['limits']['cpu'] 
                }
            })

        json.dump(dumpdict,open("PanelCache.json",'w'))
            

        await ctx.respond(content="Done!",ephemeral=True)
        await ctx.send(embed=giveServerStatus(),view=RefreshButton())





def setup(bot):
    bot.add_cog(PanelPinger(bot))