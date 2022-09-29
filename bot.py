import discord,os
import json
import utils.consoleLogger as log
from discord.ext import commands


config = json.load(open('./config.json','r'))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guild_messages = True
intents.reactions = True


bot = discord.Bot(
    status=discord.Status.idle,
    debug_guilds=list(config["DEBUG_GUILDS"]),
    # debug_guilds=[925676737625464832],
    intents=intents
)


def loadAllCogs():
    # print(os.listdir('./cogs/'))
    for each in os.listdir('./cogs/'):
        if each.endswith('.py'):
            try:
                bot.load_extension("cogs." + each[:-3])
            except discord.ExtensionError as Ee:
                log.error(each[:-3] + " cog loading Failed!")
                print(Ee)
            else:
                log.success(each[:-3] + " cog loaded Successfully!")

@bot.event
async def on_ready():
    log.info(f"Logged on as : {bot.user.name}")
    names = []
    for i in config['DEBUG_GUILDS']:
        names.append(bot.get_guild(i).name)

    log.info(f"Debug Guilds : {names}")
    print("Bot Started!")

# bot.load_extension('')

loadAllCogs()
bot.run(config['BOT_TOKEN'])