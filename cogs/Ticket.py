import asyncio
from datetime import datetime, timedelta
import os
from time import sleep
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, slash_command,message_command,user_command, Option
import json

config = json.load(open("./config.json",'r'))

async def openTicket(user: discord.Member,guild: discord.Guild,msg=None,type=config["TICKET"]["TYPES"][0]):
    tmp = str(int(open(".tmp",'r').read())+1)
    open('.tmp','w').write(tmp)
    ticket_category = discord.utils.get(guild.categories, id=config["TICKET"]["CATEGORY_ID"])

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True,send_messages=True,attach_files=True),
        guild.get_role(config["TICKET"]["STAFF_ROLE_ID"]): discord.PermissionOverwrite(read_messages=True,send_messages=True,attach_files=True)
    }

    tkt_chnl = await guild.create_text_channel(name=f"{user.name}︱{type}︱{tmp}",category=ticket_category,overwrites=overwrites)
        
    if msg == None:
        msg = f"{user.mention} please elaborate your query here, So that our staff team can help you."
    else:
        msg = f"**Message:** ```{msg}```"

    em = discord.Embed(title="Prithvi Support",description=msg, color=discord.Color.from_rgb(91, 235, 192),timestamp=datetime.now())
    em.add_field(name="Type", value=type)

    await tkt_chnl.send(content=user.mention,embed=em)



class TicketOpenView(discord.ui.View):
    def __init__(self):    
        self.value = None
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Minecaft",style=discord.ButtonStyle.blurple,custom_id="minecraft", emoji="<:mccraft:677833864478982154>")
    async def mc_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await openTicket(user=interaction.user,guild=interaction.guild,type=butt.custom_id.capitalize())
        await interaction.response.send_message(f"{interaction.user.mention} Your Support request has been raised! Please wait while our Staff reviews your Query.",ephemeral=True)
    
    @discord.ui.button(label="Discord",style=discord.ButtonStyle.blurple,custom_id="discord", emoji="🤖")
    async def discord_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await openTicket(user=interaction.user,guild=interaction.guild,type=butt.custom_id.capitalize())
        await interaction.response.send_message(f"{interaction.user.mention} Your Support request has been raised! Please wait while our Staff reviews your Query.",ephemeral=True)

    @discord.ui.button(label="Rank/Donations",style=discord.ButtonStyle.success,custom_id="ranks", emoji="⭐")
    async def rank_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await openTicket(user=interaction.user,guild=interaction.guild,type=butt.custom_id.capitalize())
        await interaction.response.send_message(f"{interaction.user.mention} Your Support request has been raised! Please wait while our Staff reviews your Query.",ephemeral=True)

    @discord.ui.button(label="Other",style=discord.ButtonStyle.gray,custom_id="other")
    async def other_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} Your Support request has been raised! Please wait while our Staff reviews your Query.",ephemeral=True)
        await openTicket(user=interaction.user,guild=interaction.guild,type=butt.custom_id.capitalize())

waitforlog = []

class CloseView(discord.ui.View):
    def __init__(self):
        self.value = None
        super().__init__(timeout=60)
    

    async def sendLog(self,interaction: discord.Interaction):
        channel = interaction.channel
        
        open("./Ticket Logs/"+channel.name+".md", "x", encoding="utf-8").close()
        file = open("./Ticket Logs/"+channel.name+".md", "a", encoding="utf-8")
    
        async for msg in channel.history(oldest_first=True):
            
            if msg.content != "":
                file.write(f"""{msg.author.name}#{msg.author.discriminator} → {msg.content}\n\n""")
                
        file.close()

        sendfp = open("./Ticket Logs/"+channel.name+".md", "rb")
        await interaction.guild.get_channel(config['TICKET']['LOG_CHANNEL_ID']).send(file=discord.File(fp=sendfp,filename=channel.name + ".md"))
        sendfp.close()
        os.remove("./Ticket Logs/"+channel.name+".md")
        

    @discord.ui.button(label="Confirm",style=discord.ButtonStyle.green, emoji="✅")
    async def confirm_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.response.send_message(f"Support Ticket will be Closed <t:{int((datetime.now()+timedelta(seconds=5)).timestamp())}:R>")
        await self.sendLog(interaction)
        await asyncio.sleep(4)
        await interaction.channel.delete()
        self.stop()

    
    @discord.ui.button(label="Cancel",style=discord.ButtonStyle.danger, emoji="❎")
    async def cancel_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        self.stop()
        waitforlog.append({interaction.channel_id: False})
        

class Ticket(commands.Cog):
    def __init__(self,bot: discord.Bot):
        self.bot = bot

    

    tickets = SlashCommandGroup("ticket", "Contact staff using Tickets",guild_ids=config["DEBUG_GUILDS"])

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TicketOpenView())

    @tickets.command(description="Initiate")
    @discord.default_permissions(administrator=True)
    async def init(self,ctx:discord.ApplicationContext):
        await ctx.respond("Done!",ephemeral=True)
        await ctx.send(embed=discord.Embed(title="Prithvi MC Support Ticket!",
        description="You raise a support request by opening a ticket! To open a ticket you can either use the **Buttons** provided below or user `/ticket open <type> <message/query>`",
        color=discord.Color.from_rgb(91, 235, 192)).set_footer(text="Prithvi Staff"),view=TicketOpenView())
               

    @tickets.command(description="Raise support ticket")
    async def open(
        self, 
        ctx: discord.ApplicationContext, 
        type: Option(str, description="Enter the type of Query.",required=False,default=config["TICKET"]["TYPES"][0],choices=config["TICKET"]["TYPES"]),
        msg: Option(str,name="message", description="Elaborate your Problem/Query here.", required=False,default=None)
    ):  
        if ctx.channel.category_id == config["TICKET"]["CATEGORY_ID"]:
            await ctx.respond(content="Sorry You can't use this command in Ticket! Please use it in Bot Channel.",ephemeral=True)
            return
        
        await openTicket(user=ctx.author,guild=ctx.guild,msg=msg,type=type)
        
        await ctx.respond(f"{ctx.author.mention} Your Support request has been raised! Please wait while our Staff reviews your Query.")
        
        # await tkt_chnl.set_permissions(ctx.author,read_messages=True,send_messages=True,attach_files=True)
        
        

    @tickets.command(description="Add Member to This/a ticket.")
    async def add(self,ctx: discord.ApplicationContext, member: Option(discord.Member,description="User you want to add to ticket.",required=True),
    ticket: Option(discord.TextChannel,description="Select Ticket Channel", required=False, default=None)):
        if ctx.channel.category_id != config["TICKET"]["CATEGORY_ID"]:
            await ctx.respond(content="You can only use this command in Ticket Channels.",ephemeral=True)
            return

        if ctx.author.guild_permissions.administrator or ctx.guild.get_role(config["TICKET"]["STAFF_ROLE_ID"]) in ctx.author.roles:
            if ticket == None:
                await ctx.channel.set_permissions(member,read_messages=True,send_messages=True,attach_files=True)
                await ctx.respond(embed=discord.Embed(title=f"New User added!",description=f"{member.mention} has been added to {ctx.channel.mention}",timestamp=datetime.now(),color=discord.Color.from_rgb(74, 157, 240)))
            else:
                await ticket.set_permissions(member,read_messages=True,send_messages=True,attach_files=True)
                await ctx.respond(embed=discord.Embed(title=f"New User added!",description=f"{member.mention} has been added to {ticket.mention}",timestamp=datetime.now(),color=discord.Color.from_rgb(74, 157, 240)))
            
        else:
            await ctx.respond(embed=discord.Embed(title=f"You **Do not** have permission to execute this command."),timestamp=datetime.now(),color=discord.Color.red())
    
    @tickets.command(description="Remove Member from This/a ticket.")
    async def remove(self,ctx: discord.ApplicationContext, member: Option(discord.Member,description="User you want to add to ticket.",required=True),
    ticket: Option(discord.TextChannel,description="Select Ticket Channel", required=False, default=None)):
        if ctx.channel.category_id != config["TICKET"]["CATEGORY_ID"]:
            await ctx.respond(content="You can only use this command in Ticket Channels.",ephemeral=True)
            return
        if ctx.author.guild_permissions.administrator or ctx.guild.get_role(config["TICKET"]["STAFF_ROLE_ID"]) in ctx.author.roles:
            if ticket == None:
                await ctx.channel.set_permissions(member,read_messages=False,send_messages=False,attach_files=False)
                await ctx.respond(embed=discord.Embed(title=f"User removed!",description=f"{member.mention} has been removed from {ctx.channel.mention}",timestamp=datetime.now(),color=discord.Color.orange()))
            else:
                await ticket.set_permissions(member,read_messages=False,send_messages=False,attach_files=False)
                await ctx.respond(embed=discord.Embed(title=f"User removed!",description=f"{member.mention} has been removed from {ticket.mention}",timestamp=datetime.now(),color=discord.Color.orange()))
            
        else:
            await ctx.respond(embed=discord.Embed(title=f"You **Do not** have permission to execute this command."),timestamp=datetime.now(),color=discord.Color.red())
    
    @tickets.command(description="Close This ticket.")
    async def close(self,ctx: discord.ApplicationContext):
        if ctx.channel.category_id != config["TICKET"]["CATEGORY_ID"]:
            await ctx.respond(content="You can only use this command in Ticket Channels.",ephemeral=True)
            return
        
        close_view = CloseView()
        await ctx.respond(embed=discord.Embed(title="Do you want to close this ticket?",color=discord.Color.red()),view=close_view,delete_after=60)
        
        

        


def setup(bot):
    bot.add_cog(Ticket(bot))