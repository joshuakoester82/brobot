import discord
from discord.ext import commands
import functions as f
from random import choice

"""
A simple discord bot for GameBros server.
See 'todo.txt' for potential features.
"""

# region init

flavor = False
token = "" # put your bot token here
client = commands.Bot(command_prefix = "!")
client.remove_command("help")

# load user presets
with open("../data/user_character_presets.txt","r+") as file:
    try:
        user_character_presets = eval(file.read())
        print(f"{file.name} loaded from file: {user_character_presets}")
    except:
        print(f"Unexpected error loading {file.name}. Reinitialized file.")
        file.truncate(0)
        file.seek(0)
        user_character_presets = {}
        file.write("{}")

# endregion


@client.event
async def on_member_update(member_a,member_b):
    global flavor
    if flavor == True:
        # on waking up
        status_a = str(member_a.status)
        status_b = str(member_b.status)
        if status_a == "idle" and status_b == "online":
            channel_general = client.get_channel(439603779298394124)
            # Josh
            if member_a.id == 124339909820547074:
                possible_messages = ["Welcome back creator!", "I missed you, Alimightyzentaco.", "Greetings creator!",
                                     "Ahh, he who gave me life is here. I am elated."]
                message = choice(possible_messages)
                await channel_general.send(message)

            # Ryan
            if member_a.id == 140294058663739394:
                possible_messages = ["Welcome back Ryan. How was your nap?",
                                     "Welcome Ryan, glad you finally woke up.",
                                     "It's good to see you again Ryan. Did you sleep well?",
                                     "Back amongst the living, eh Ryan?",
                                     "Ryan likes to party. And by party I mean take naps.",
                                     "Finally. Ryan is awake. Let the games begin.",
                                     "Do you guys think someone can nap too much? Let's ask Ryan, he'll probably know.",
                                     "Ryan is so good at sleeping he can do it with his eyes closed.",
                                     "Ryan spends so much time undercovers, he should be a detective."
                                     "Hey, Ryan's awake! About time."

                                     ]
                message = choice(possible_messages)
                await channel_general.send(message)


@client.event
async def on_message(message):
    if "https://www.youtube.com/watch?v=AmGti20smKo" in message.content:
        possible_messages = ["Nope, none of that.",
                             "Not on my watch.",
                             "No sir, not gonna happen",
                             "Maybe don't do that so much",
                             "Nobody is 'schemin' like a demon semen' while I'm here",
                             "Why would you try to subject us to that?",
                             "Please, don't do that."
                             ]
        to_send = choice(possible_messages)
        await message.channel.send(to_send)
        await message.delete()
    await client.process_commands(message)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def help(ctx):
    await ctx.send("List of commands. Some commands are not yet finished:\n"
                   "!help: help prompt\n"
                   "!ping: returns latency\n"
                   "!roll <times>d<sides> : roll some dice\n"
                   "!russianroulette: Play Russian Roulette. Always random. 1 in 6 chance of dying\n"
                   "!mythicplus: <character> <realm> Shows M+ score for character. Default realm=sargeras "
                   "(m+,mplus,mythic+,mp)\n"
                   "!bestruns <character> <realm>: show the best runs for the character. Default realm=sargeras "
                   "(br,bestr,bruns)\n"
                   "!raid <character> <realm>: show raid progression for selected character.(rp,progression,raid)\n"
                   "!raiderio <character> <realm> return a link with the raider.io character page (char, info, link)\n"
                   "!r (optional arguments:  -<character/realm/region>  d-x, m-x) [ex: !r sethur/sargeras/us d-4 m-dps] "
                   ": show rank info from warcraftlogs \n"
                   "!register <character> <realm> <region> : register a default character to your username.")

    f.log(ctx.message.author,ctx.message.content)


@client.command()
async def ping(ctx):
    await ctx.send(f"Parng! {round(client.latency*1000)}ms")
    f.log(ctx.message.author, ctx.message.content)


@client.command(aliases = ["dice","die","rolls"])
async def roll(ctx,roll="1d6"):
    roll_list = roll.strip().lower().split("d")
    f.log(ctx.message.author, ctx.message.content)
    try:
        roll,times = int(roll_list[0]), int(roll_list[1])
        result = f.roll(roll,times)
        await ctx.send(result)

    except:
        await ctx.send("You did something stupid. Cut that out.")


@client.command(aliases=["rr","russianr","roulette"])
async def russianroulette(ctx):
    await ctx.send(f.russian_roulette(ctx.author))
    f.log(ctx.message.author, ctx.message.content)


@client.command(aliases=["m+", "mplus", "mythic+", "mp"])
async def mythicplus(ctx,name=None,realm=None):
    author = str(ctx.message.author)
    if name is None:
        try:
            name = user_character_presets[author][0]
            print(f"name is {name}")
        except:
            print(f"exception! name: {name}")
            await ctx.send("Enter name or register a default character")

    if realm is None:
        try:
            realm = user_character_presets[author][1]
            print(f"realm is : {realm}")
        except:
            realm = "sargeras"
            print(f"realm is {realm}")

    raid_stats = f.get_mythic_plus(name,realm)
    name_caps = str(name).capitalize()
    message = f"{name_caps}'s mythic+ score is: {raid_stats}"
    await ctx.send(message)
    f.log(ctx.message.author, ctx.message.content)


@client.command(aliases = ["items"])
async def gear(ctx,name=None,realm=None):
    author = str(ctx.message.author)
    if name is None:
        try:
            name = user_character_presets[author][0]
        except:
            await ctx.send("Enter name or register a default character")
    if realm is None:
        try:
            realm = user_character_presets[author][1]
        except:
            realm = "sargeras"
    message = f.get_gear(name,realm)
    await ctx.send(message)
    f.log(ctx.message.author, ctx.message.content)


@client.command(aliases=["char","info","link","character"])
async def raiderio(ctx,name=None,realm=None):
    author = str(ctx.message.author)
    if name is None:
        try:
            name = user_character_presets[author][0]
        except:
            await ctx.send("Enter name or register a default character")
    if realm is None:
        try:
            realm = user_character_presets[author][1]
        except:
            realm = "sargeras"

    message = f.get_raideriopage(name,realm)
    await ctx.send(message)
    f.log(ctx.message.author, ctx.message.content)


@client.command(aliases=["rp","raidprogression","proggression"])
async def raid(ctx,name=None,realm=None):
    author = str(ctx.message.author)
    if name is None:
        try:
            name = user_character_presets[author][0]
        except:
            await ctx.send("Enter name or register a default character")
    if realm is None:
        try:
            realm = user_character_presets[author][1]
        except:
            realm = "sargeras"

    message = f.get_raid_progression_as_embed(name,realm)
    await ctx.send(embed=message)
    f.log(ctx.message.author, ctx.message.content)


@client.command(aliases = ["br","bruns","best","runs"])
async def bestruns(ctx,name=None,realm=None):
    author = str(ctx.message.author)
    if name is None:
        try:
            name = user_character_presets[author][0]
        except:
            await ctx.send("Enter name or register a default character")
    if realm is None:
        try:
            realm = user_character_presets[author][1]
        except:
            realm = "sargeras"

    message = f.get_best_runs_as_embed(name,realm)
    await ctx.send(embed=message)
    f.log(ctx.message.author, ctx.message.content)


@client.command(aliases=["rankings","getrank","r","logs","parse"])
async def rank(ctx):
    print(f"{ctx.message.author} requested rank information from warcraftlogs.com ")
    author = str(ctx.message.author)
    commands = str(ctx.message.content).split(" ")
    commands.remove(commands[0])
    # set default values
    name, realm, difficulty, region, metric = None, "sargeras", 4, "us", "dps"

    for item in commands:
        if item.startswith("d-") or item.startswith("difficulty-"):
            item_list = item.split("-")
            if len(item_list) > 1:
                difficulty = int(item_list[1])
        if item.startswith("m-") or item.startswith("metric-"):
            item_list = item.split("-")
            if len(item_list) > 1:
                metric = item_list[1]
        if item.startswith("-"):
            item_list = item.split("-")
            if len(item_list) > 1:
                name_realm_region = item_list[1]
                if "/" in name_realm_region:
                    nrr_list = name_realm_region.split("/")
                    name = nrr_list[0]
                    if len(nrr_list) > 1:
                        realm = nrr_list[1]
                    if len(nrr_list) > 2:
                        region = nrr_list[2]
                else:
                    name = name_realm_region

    if name is None:
        try:
            name = user_character_presets[author][0]
        except:
            print("No name preset for user")
            await ctx.send("Enter a character name or register a character with !register")
        try:
            realm = user_character_presets[author][1]
        except:
            print("No region preset for user")
        try:
            region = user_character_presets[author][2]
        except:
            print("No realm preset for user")

    message = f.get_rankings(name,realm,difficulty,metric,region)
    await ctx.send(embed=message)


@client.command()
async def register(ctx,name=None,realm="sargeras",region="us"):
    user = str(ctx.message.author)
    user_character_presets[user] = [name, realm, region]
    with open("user_character_presets.txt","w") as file:
        file.write(str(user_character_presets))
    await ctx.send(f"Character registered as : {name}, {realm}, {region}")
    await ctx.send(f"https://raider.io/characters/{region}/{realm}/{name}")


@client.command()
async def idiot(ctx):
    author = str(ctx.message.author)
    if author == "Horizen#1881":
        await ctx.send("That's you, @Horizen#1881.")
    else:
        await ctx.send("The current idiot around here is @Horizen#1881")


@client.command()
async def pic(ctx):
   file = discord.File("yousuck.jpg")
   await ctx.channel.send(file=file)


@client.command()
async def personality(ctx):
    global flavor
    flavor = not flavor
    if flavor == True:
        await ctx.send("I'll spice it up a bit.")
    else:
        await ctx.send("Okay, It's all business from here on out.")


client.run(token)












