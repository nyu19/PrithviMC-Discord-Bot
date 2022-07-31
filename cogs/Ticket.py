import asyncio
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, slash_command,message_command,user_command, Option
import json

config = json.load(open("./config.json",'r'))


class CloseView(discord.ui.View):
    def __init__(self):
        self.value = None
        super().__init__(timeout=60)
    

    @discord.ui.button(label="Confirm",style=discord.ButtonStyle.green, emoji="✅")
    async def confirm_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.response.send_message(f"Support Ticket will be Closed <t:{int((datetime.now()+timedelta(seconds=5)).timestamp())}:R>")
        await asyncio.sleep(4)
        await interaction.channel.delete()
        
        self.stop()
    
    @discord.ui.button(label="Cancel",style=discord.ButtonStyle.danger, emoji="❎")
    async def cancel_callback(self, butt: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        self.stop()

class Ticket(commands.Cog):
    def __init__(self,bot: discord.Bot):
        self.bot = bot

    tickets = SlashCommandGroup("ticket", "Contact staff using Tickets",guild_ids=config["DEBUG_GUILDS"])

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
        tmp = str(int(open(".tmp",'r').read())+1)
        open('.tmp','w').write(tmp)
        
        ticket_category = discord.utils.get(ctx.guild.categories, id=config["TICKET"]["CATEGORY_ID"])
        
        await ctx.respond(f"{ctx.author.mention} Your Support request has been raised! Please wait while our Staff reviews your Query.")
        
        tkt_chnl = await ctx.guild.create_text_channel(name=f"{ctx.author.name}︱{type}︱{tmp}",category=ticket_category)
        
        await tkt_chnl.set_permissions(ctx.author,read_messages=True,send_messages=True,attach_files=True)
        
        if msg == None:
            msg = f"{ctx.author.mention} please elaborate your query here, So that our staff team can help you."
        else:
            msg = f"**Message:** ```{msg}```"

        em = discord.Embed(title="Prithvi Support",description=msg, color=discord.Color.from_rgb(91, 235, 192),timestamp=datetime.now())
        em.add_field(name="Type", value=type)

        await tkt_chnl.send(content=ctx.author.mention,embed=em)

    
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
        await ctx.respond(embed=discord.Embed(title="Do you want to close this ticket?",color=discord.Color.red()),view=close_view)
        


def setup(bot):
    bot.add_cog(Ticket(bot))