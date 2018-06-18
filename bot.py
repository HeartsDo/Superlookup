import time
import json
import discord
from discord.ext import commands

with open('./config.json', 'r') as fichier:
    DATA = json.load(fichier)
START_TIME = time.time()
BOT = commands.Bot(command_prefix='.')
TOKEN = DATA['token']


@BOT.event
async def on_ready():
    print('Logged in as')
    print(BOT.user.name)
    print(BOT.user.id)
    print('------')
    game = discord.Game(name="Look the user with .look")
    await BOT.change_presence(status=discord.Status.idle, game=game)

@BOT.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await BOT.send_message(ctx.message.channel, "It seems you are missing required argument(s). Try again if you have all the arguments needed.")


@BOT.command(pass_context=True)
async def look(ctx, user: discord.Member):
    """ Launch a lookup """
    edit = await BOT.say(':mag: Lookup in progress for: ' + str(user.id))
    await BOT.send_typing(ctx.message.author)
    embed = discord.Embed(title="ID: " + str(user.id), color=0x44b57c)
    embed.set_author(name="Lookup of " + user.name + "#" + str(user.discriminator), icon_url=user.avatar_url)
    embed.add_field(name="Created the:", value=user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"), inline=False)
    embed.add_field(name="Joined the guild the:", value=user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"), inline=False)
    role_names = [role.name for role in user.roles]
    embed.add_field(name="Roles:", value=role_names, inline=False)
    embed.add_field(name="Nickname on server:", value=user.display_name, inline=True)
    if user.BOT is True:
        embed.add_field(name="Is BOT ?:", value="Yes", inline=True)
    else:
        embed.add_field(name="Is BOT ?:", value="No", inline=True)
    embed.set_footer(text="Superlookup version 1.0, by HeartsDo#0530")
    await BOT.edit_message(edit, ":white_check_mark: Done:")
    await BOT.say(embed=embed)

@BOT.command()
async def info():
    """ Show Info of the BOT """
    embed = discord.Embed(title="Version: 1", color=0x44b57c)
    embed.set_author(name="BOT created by HeartsDo#0530", icon_url="https://cdn.discordapp.com/avatars/140913931668553728/a993b5f3aa162d05927d8b3c88a98ef0.png")
    second = time.time() - START_TIME
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    embed.add_field(name="Uptime:", value=str(int(week)) + " weeks, " + str(int(day)) + " days, " + str(int(hour)) + " hours, " + str(int(minute)) + " minutes, " + str(int(second)) + " seconds")
    await BOT.say(embed=embed)

BOT.remove_command("help")

@BOT.command()
async def help():
    embed = discord.Embed(name="Help", color=0x44b57c)
    embed.set_author(name="SuperLookup", icon_url="https://cdn.discordapp.com/avatars/451052111564767232/80479dce8b8091a66068946ac9100ba4.png")
    embed.add_field(name=".look <@mention or user id>", value="Lookup a user", inline=False)
    embed.add_field(name=".info", value="Gives a little info about the BOT", inline=False)
    embed.add_field(name=".help", value="Gives this message", inline=False)
    await BOT.say(embed=embed)

BOT.run(TOKEN)

