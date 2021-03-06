import time
import json
import discord
from discord.ext import commands

with open('./config.json', 'r') as fichier:
    data = json.load(fichier)

start_time = time.time()
bot = commands.Bot(command_prefix='.')
token = data['token']
client = discord.Client

# Bot ready
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('----------')
    game = discord.Game("Look the user with .look")
    await bot.change_presence(status=discord.Status.idle, activity=game)

# Error gestion
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(ctx.message.channel, "It seems you are missing required argument(s). Try again if you have all the arguments needed.") 

def is_not_bot():
    async def predicate(ctx):
        if ctx.author.bot == True:
            return False
        else:
            return True
    return commands.check(predicate)


@bot.command()
@is_not_bot()
async def look(ctx, user: discord.Member):
    """ Launch a lookup """
    await ctx.send(':mag: Lookup in progress for: ' + str(user.id))
    await ctx.trigger_typing()
    embed = discord.Embed(title="ID: " + str(user.id), color=0x44b57c)
    embed.set_author(name="Lookup of " + user.name + "#" + str(user.discriminator), icon_url=user.avatar_url)
    embed.add_field(name="Created the:", value=user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"), inline=False)
    embed.add_field(name="Joined the guild the:", value=user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"), inline=False)
    role_names = [role.name for role in user.roles]
    embed.add_field(name="Roles:", value=role_names, inline=False)
    embed.add_field(name="Nickname on server:", value=user.display_name, inline=True)
    if user.bot is True:
        embed.add_field(name="Is BOT ?:", value="Yes", inline=True)
    else:
        embed.add_field(name="Is BOT ?:", value="No", inline=True)
    embed.set_footer(text="Superlookup version 1.0, by HeartsDo#0530")
    await ctx.send(":white_check_mark: Done:")
    await ctx.send(embed=embed)

@bot.command()
@is_not_bot()
async def info(ctx):
    """ Show Info of the bot """
    embed = discord.Embed(title="Version: 1", color=0x44b57c)
    embed.set_author(name="Bot created by HeartsDo#0530", icon_url="https://cdn.discordapp.com/avatars/140913931668553728/a993b5f3aa162d05927d8b3c88a98ef0.png")
    second = time.time() - start_time
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    embed.add_field(name="Uptime:", value=str(int(week)) + " weeks, " + str(int(day)) + " days, " + str(int(hour)) + " hours, " + str(int(minute)) + " minutes, " + str(int(second)) + " seconds")
    await ctx.send(embed=embed)

bot.remove_command("help")

@bot.command()
@is_not_bot()
async def help(ctx):
    embed = discord.Embed(name="Help", color=0x44b57c)
    embed.set_author(name="SuperLookup", icon_url="https://cdn.discordapp.com/avatars/451052111564767232/80479dce8b8091a66068946ac9100ba4.png")
    embed.add_field(name=".look <@mention or user id>", value="Lookup a user", inline=False)
    embed.add_field(name=".info", value="Gives a little info about the BOT", inline=False)
    embed.add_field(name=".help", value="Gives this message", inline=False)
    await ctx.send(embed=embed)


bot.run(token)
