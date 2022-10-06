import datetime
import discord,requests
from discord.ext import commands,pages,tasks
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
        title="**Panel Status**",
        color=discord.Color.from_rgb(59, 130, 246),
        timestamp=datetime.datetime.now(),
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
**CPU:** `{data['resources']['cpu_absolute']} / {i['limits']['cpu']} %`""",inline=False)


    embed.set_thumbnail(url=config['SERVER_ICON_URL'])
    return embed

class RefreshButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Refresh",style=discord.ButtonStyle.blurple,custom_id="panelstats", emoji="🔄")
    async def button_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=giveServerStatus(),view=self)



class PanelPinger(commands.Cog):
    def __init__(self,bot:discord.Bot):
        self.bot = bot
        self.daily_update.start()
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RefreshButton())
        
    @tasks.loop(time=datetime.time(hour=int(str(config["PANEL"]["DAILY_UPDATE_TIME"]).split(":")[0]),minute=int(str(config["PANEL"]["DAILY_UPDATE_TIME"]).split(":")[1]),tzinfo=datetime.datetime.now().astimezone().tzinfo))
    async def daily_update(self):
        # print("In Loop!")
        em = giveServerStatus().fields
        tempList = []
        for each in em:
            if each.value.count("🟢") < 1:
                tempList.append(each.name)
        
        if len(tempList) != 0:
            updateUser = await self.bot.get_or_fetch_user(config["PANEL"]["DAILY_UPDATE_USER_ID"])
            await updateUser.send(f"**{updateUser.mention} The Following server is facing issue!**\n`{str(tempList).replace('*','')}` \nPlease visit: {config['PANEL']['URL']}")
            
        else:
            return

        

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