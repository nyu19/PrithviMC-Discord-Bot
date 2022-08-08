from datetime import datetime
import discord
from discord.ext import commands

class userinfo(commands.Cog):
    def __init__(self,bot: discord.Bot):
        self.bot = bot

    @commands.user_command()
    async def info(self,ctx: discord.ApplicationContext, member: discord.Member):
        emb = discord.Embed(
            title=f"{member.name}#{member.discriminator}",
            description=member.mention,
            color=member.top_role.color,
            timestamp=datetime.now()
        )
        try: 
            emb.set_thumbnail(url=member.avatar.url)
        except AttributeError:
            emb.set_thumbnail(url=member.default_avatar.url)
        
        try:
            emb.set_image(url=member.banner.url)
        except Exception:
            pass

        emb.add_field(name=f"Verified",value=str(not member.pending))
        emb.add_field(name=f"Registered",value=member.created_at)
        emb.add_field(name=f"Joined Prithvi",value=member.joined_at)
        emb.add_field(name=f"Timed out",value=str(member.timed_out))
        emb.add_field(name=f"Roles [{len(member.roles)}]",value=str([i.mention for i in member.roles])[1:-1])
        emb.add_field(name=f"Guild Permissions",value=f"{'`Admin`' if member.guild_permissions.administrator else [i[0].capitalize() for i in member.guild_permissions if i[1]]}".replace("_"," ").replace("'","`")[1:-1])
        emb.add_field(name=f"ID",value=f"`{member.id}`")
        # emb.add_field(name=f"",value=f"{}")




        await ctx.respond(ephemeral=True,embed=emb)

def setup(bot):
    bot.add_cog(userinfo(bot))