import discord
from discord.ext import commands
from discord.ui import Button,View
from discord.commands import slash_command,message_command,user_command
import json
config = json.load(open('./config.json','r'))

# class pinger(commands.Cog):
#     def __init__(self,bot: discord.Bot):
#         self.bot = bot
    
#     @commands.Cog.listener()    
    
    
#     async def on_message(self,msg: discord.Message):
#         if(msg.author==self.bot.user):
#             return
        
#         async def button_callback(interation:discord.Interaction):
#             print(interation.user)
#             role= interation.guild.get_role(1002794393771716728)
#             roles = interation.user.roles
            
#             print(role in roles)
            
#             if role in roles:
#                 await interation.user.remove_roles(role)
#                 return
#             else:
#                 await interation.user.add_roles(role)
                
#             await interation.response.send_message("oki")
            
        
#         button = Button(label="Click", style=discord.ButtonStyle.green, emoji="⛔")
#         button.callback=button_callback
#         view = View()
        
#         print(msg.author.roles)
    
#         view.add_item(button)
#         await msg.channel.send("Hi", view=view) 
        
#     async def on_button_click(self,interaction:discord.Interaction):
#         print(interaction)
        
def embeder():
    embed=discord.Embed(
        title="**Get Your Roles By Clicking The Respective Buttons**",
        description="description",
        color=discord.Color.blue()
    )
    
    return embed        

class announcementRole(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Announcement",style=discord.ButtonStyle.blurple,custom_id="Annoucment",emoji="📢")
    async def button_callback(self,button:discord.ui.Button,interaction:discord.Interaction):
        role= interaction.guild.get_role(1002794393771716728)
        roles = interaction.user.roles
        if role in roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(content=f"{role.mention} Role was removed", ephemeral=True)
            return
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(content=f"{role.mention} Role was added", ephemeral=True)
            
    @discord.ui.button(label="Development",style=discord.ButtonStyle.blurple,custom_id="Develpoment",emoji="📢")
    async def button_callback(self,button:discord.ui.Button,interaction:discord.Interaction):
        role= interaction.guild.get_role(1002794393771716728)
        roles = interaction.user.roles
        if role in roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(content=f"{role.mention} Role was removed", ephemeral=True)
            return
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(content=f"{role.mention} Role was added", ephemeral=True)
            
    @discord.ui.button(label="Announcement",style=discord.ButtonStyle.blurple,custom_id="Annoucment",emoji="📢")
    async def button_callback(self,button:discord.ui.Button,interaction:discord.Interaction):
        role= interaction.guild.get_role(1002794393771716728)
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
        self.bot.add_view(announcementRole())
    
    @commands.slash_command(description="buttonRole")
    @discord.default_permissions(administrator=True)
    async def getrole(self,ctx: discord.ApplicationContext):
        await ctx.defer()
        await ctx.send(embed=embeder(),view=announcementRole())
        await ctx.respond(content="Done!",delete_after=3)
        

        
def setup(bot):
    bot.add_cog(buttonRole(bot))