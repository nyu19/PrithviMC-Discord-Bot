import discord
from discord.ext import commands
from discord.ui import Button,View
from discord.commands import slash_command,message_command,user_command
import json
config = json.load(open('./config.json','r'))

        
def embeder():
    embed=discord.Embed(
        title="**Get Your Roles By Clicking The Respective Buttons**",
        description=f"""The corresponding role will be pinged whenever anything is posted in specific channels. If you like to be notified when one of these things occur, please react with the following emojis to get the corresponding roles:

<@{config["ROLES"]["ANNOUNCEMENT"]}>
<@{config["ROLES"]["DEVELOPMENT"]}>
<@{config["ROLES"]["EVENT"]}>
""",
        color=discord.Color.blue()
    )
    
    return embed        

class buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Announcement",style=discord.ButtonStyle.blurple,custom_id="Annoucment",emoji="📢")
    async def button1_callback(self,button:discord.ui.Button,interaction:discord.Interaction):
        role= interaction.guild.get_role(config["ROLES"]["ANNOUNCEMENT"])
        roles = interaction.user.roles
        if role in roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(content=f"{role.mention} Role was removed", ephemeral=True)
            return
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(content=f"{role.mention} Role was added", ephemeral=True)
            
    @discord.ui.button(label="Development",style=discord.ButtonStyle.blurple,custom_id="Develpoment",emoji="👨‍💻")
    async def button2_callback(self,button:discord.ui.Button,interaction:discord.Interaction):
        role= interaction.guild.get_role(config["ROLES"]["DEVELOPMENT"])
        roles = interaction.user.roles
        if role in roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(content=f"{role.mention} Role was removed", ephemeral=True)
            return
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(content=f"{role.mention} Role was added", ephemeral=True)
            
    @discord.ui.button(label="Event",style=discord.ButtonStyle.blurple,custom_id="Event",emoji="📆")
    async def button3_callback(self,button:discord.ui.Button,interaction:discord.Interaction):
        role= interaction.guild.get_role(config["ROLES"]["EVENT"])
        roles = interaction.user.roles
        if role in roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(content=f"{role.mention} Role was removed", ephemeral=True)
            return
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(content=f"{role.mention} Role was added", ephemeral=True)
        
        
class buttonRole(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(buttons())
    
    @commands.slash_command(description="buttonRole")
    @discord.default_permissions(administrator=True)
    async def getrole(self,ctx: discord.ApplicationContext):
        await ctx.send(embed=embeder(),view=buttons())
        await ctx.respond(content="Get Ya Roles!",delete_after=3)
        

        
def setup(bot):
    bot.add_cog(buttonRole(bot))