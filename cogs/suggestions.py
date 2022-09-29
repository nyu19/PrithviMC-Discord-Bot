from datetime import datetime
import discord
from discord.ext import commands
from discord.commands import slash_command,message_command,user_command
import json
config = json.load(open('./config.json','r'))

class suggestions(commands.Cog):
    def __init__(self,bot: discord.Bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction: discord.Reaction, user:discord.Member):
        if reaction.message.channel.id == config['SUGGESTION']['CHANNEL_ID'] and user.guild_permissions.administrator and reaction.message.author.id == self.bot.user.id and user != self.bot.user:
            if reaction.emoji == '✅':
                em = reaction.message.embeds[0]
                em.clear_fields()
                em.add_field(name="Verdict", value='✅ Suggestion **Accepted** by ' + user.name)
                em.colour = discord.Color.green()
                
            elif reaction.emoji == '❎':
                em = reaction.message.embeds[0]
                em.clear_fields()
                em.add_field(name="Verdict", value='❎ Suggestion **Rejected** by ' + user.name)
                em.colour = discord.Color.red()
            
            else:           # remove if any error regrading this
                return      #

            await reaction.message.edit(embed=em)
            await reaction.message.clear_reactions()

    @commands.slash_command(description="Suggestions")
    async def suggest(self, ctx: discord.ApplicationContext, suggestion: str):
        user = ctx.author
        try: 
            avatar_url = user.avatar.url 
        except AttributeError:
            avatar_url = user.default_avatar.url

        em = discord.Embed(
            title = f"New Suggestion!",
            description = suggestion,
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )  
        em.set_author(name=user.name,icon_url=avatar_url)

        msg = await self.bot.get_channel(config['SUGGESTION']['CHANNEL_ID']).send(embed=em)
        await msg.add_reaction('👍🏻')
        await msg.add_reaction('👎🏻')
        await ctx.respond("New Suggestion has been submitted! Please wait while admins review it.",ephemeral=True)
        
    

def setup(bot):
    bot.add_cog(suggestions(bot))