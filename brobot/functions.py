import discord
import random
import requests
import datetime


def recolor(str):
    c_str = f"```md\n" \
            f"{str}\n" \
            f"```"
    return c_str


def average(list):
    return round(sum(list)/len(list),2)


def log(author,message):
    date_time = datetime.datetime.now()
    print(f"{author} {message} : {date_time}")


def roll(times=0,sides=0):
    """simulate a die roll with arguments times,sides and return a list with roll results"""
    try:
        if times <= 100 and sides <= 100_000:
            result_list = []
            for i in range(times):
                result_list.append(random.randint(1,sides))
            return f"You rolled: {result_list}"
        else:
            return "Your roll request hurt my feelings."
    except:
        return "You did something stupid. Please stop that."


def russian_roulette(name):
    """a crude russian roulette simulation. Takes the name of the player and returns a string
    with result of simulation"""
    outcome_list = [0,0,0,0,0,1]
    result = random.choice(outcome_list)
    if result == 1:
        return f"KABLAMO! {name} blew their brains out. Play stupid games win stupid prizes."
    else :
        return f"CLICK. {name} lives to play again"


def get_mythic_plus(name,realm="sargeras"):
    """Queries the Raider.io server api with a character name and realm and retrieves a json file. The data is parsed
    and returns a string to be displayed or sent to the server"""
    url = f"https://raider.io/api/v1/characters/profile?" \
          f"region=us&realm={realm}&name={name}&fields=mythic_plus_scores_by_season%3Acurrent"
    response = requests.get(url).json()
    mythic_plus_data = response["mythic_plus_scores_by_season"][0]["scores"]["all"]
    return mythic_plus_data


def get_best_runs(name,realm="sargeras"):
    """queries the raider.io server api with a request for the best runs. The resulting json is parsed and
    returned as a string."""
    url = f"https://raider.io/api/v1/characters/profile?region=us&realm={realm}" \
          f"&name={name}&fields=mythic_plus_best_runs%3A10"
    response = requests.get(url).json()
    best_runs = response["mythic_plus_best_runs"]
    run_list = []
    # put the runs into a list
    for item in best_runs:
        run_list.append(item)
    # create message string
    message = ""
    for i in range(len(run_list)):
        message += f"{run_list[i]['dungeon']} (+{run_list[i]['mythic_level']}) - {run_list[i]['score']}\n"
    return message


def get_best_runs_as_embed(name,realm="sargeras"):
    """get best runs data and return embed object"""
    url = f"https://raider.io/api/v1/characters/profile?region=us&realm={realm}" \
          f"&name={name}&fields=mythic_plus_best_runs%3A10"
    r = requests.get(url).json()
    best_runs = r["mythic_plus_best_runs"]
    run_list = []
    mplus_score = get_mythic_plus(name,realm)

    # create and prep embed
    embed_author_title = "------------------- M+ Best Runs -------------------"
    embed_author_name = f"{r['name']}'s M+ Score : {mplus_score}"
    embed_author_profile = r['profile_url']
    embed_color = 0xFF0000
    embed_thumbnail = r['thumbnail_url']
    embed = discord.Embed(title=embed_author_title, color=embed_color)
    embed.set_author(name=embed_author_name, url=embed_author_profile)
    embed.set_thumbnail(url=embed_thumbnail)

    # put the runs into a list
    for item in best_runs:
        run_list.append(item)
    # create message string
    message = ""
    for i in range(len(run_list)):
        message_name = f"{run_list[i]['dungeon']}"
        message_value = f"(+{run_list[i]['mythic_level']}) - {run_list[i]['score']}"
        embed.add_field(name=message_name, value=message_value,inline=True)
    return embed


def get_raid_progression(name,realm="sargeras"):
    """Get the raid progression info as json from Raider.io api, format and return as a string"""
    raid_list = ["the-eternal-palace","crucible-of-storms","battle-of-dazaralor","uldir"]
    formatted_raidnames = ["Eternal Palace","Crucible of Storms","Battle of Dazaralor","Uldir"]
    url = f"https://raider.io/api/v1/characters/profile?region=us&realm={realm}&name={name}&fields=raid_progression"
    response = requests.get(url).json()
    category = response['raid_progression']
    message = f"{str(name).capitalize()}'s Raid Progression\n" \
              f"---------------------------------------\n"
    for i in range(len(raid_list)):
        total_bosses = category[raid_list[i]]['total_bosses']
        message += f"{formatted_raidnames[i]}: {category[raid_list[i]]['mythic_bosses_killed']}/{total_bosses}M, "
        message += f"{category[raid_list[i]]['heroic_bosses_killed']}/{total_bosses}H, "
        message += f"{category[raid_list[i]]['normal_bosses_killed']}/{total_bosses}N\n"
    message += f"---------------------------------------\n"
    return message


def get_raid_progression_as_embed(name,realm="sargeras"):
    """Query raider.io for raid progression and return an embed object"""
    raid_list = ["the-eternal-palace", "crucible-of-storms", "battle-of-dazaralor", "uldir"]
    formatted_raidnames = ["Eternal Palace", "Crucible of Storms", "Battle of Dazaralor", "Uldir"]
    url = f"https://raider.io/api/v1/characters/profile?region=us&realm={realm}&name={name}&fields=raid_progression"
    r = requests.get(url).json()
    category = r['raid_progression']

    embed_author_title = "------------------- Raid Progression -------------------"
    embed_author_name = f"{r['name']} : {r['active_spec_name']} {r['class']}"
    embed_author_profile = r['profile_url']
    embed_color = 0xFF0000
    embed_thumbnail = r['thumbnail_url']

    embed = discord.Embed(title=embed_author_title, color=embed_color)
    embed.set_author(name=embed_author_name,url=embed_author_profile)
    embed.set_thumbnail(url=embed_thumbnail)

    for i in range(len(raid_list)):
        message = ""
        total_bosses = category[raid_list[i]]['total_bosses']
        message += f"{category[raid_list[i]]['mythic_bosses_killed']}/{total_bosses}M, "
        message += f"{category[raid_list[i]]['heroic_bosses_killed']}/{total_bosses}H, "
        message += f"{category[raid_list[i]]['normal_bosses_killed']}/{total_bosses}N\n"
        embed.add_field(name=f"{formatted_raidnames[i]}", value=message, inline=False)

    return embed


def get_gear(name,realm="sargeras"):
    """Query the raider.io server for gear information on a character and return as a formatted string"""
    url = f"https://raider.io/api/v1/characters/profile?region=us&realm={realm}&name={name}&fields=gear"
    response = requests.get(url).json()
    gear = response["gear"]
    message = f"{name}'s Gear:\n" \
              f"--------------------\n" \
              f"Equipped Item Level: {gear['item_level_equipped']}\n" \
              f"Total Item Level: {gear['item_level_total']}\n" \
              f"Artifact Traits: {gear['artifact_traits']}\n" \
              f"-------------------\n"
    return message


def get_raideriopage(name,realm="sargeras"):
    """Query the raider.io server for a link to the character and return as a string."""
    url = f"https://raider.io/api/v1/characters/profile?region=us&realm={realm}&name={name}"
    response = requests.get(url).json()
    link = response['profile_url']
    return link


def get_rankings(name,realm="sargeras",target_difficulty=3,metric="dps",region="us"):
    """Query the warcraftlogs api for character rankings, embed, and return as embed object"""
    difficulty_dict = {5:"Mythic", 4:"Heroic", 3:"Normal"}
    r = requests.get(f"https://www.warcraftlogs.com:443/v1/rankings/character/{name}/{realm}/{region}?metric={metric}"
                     f"&timeframe=historical&api_key=9850a2e6d1fb8032c841cd17f4afb60b").json()
    # create embed
    ilvl = r[0]["ilvlKeyOrPatch"]
    embed_author_title = f"-------------------{difficulty_dict.get(target_difficulty)} {metric} Rankings -------------------"
    embed_author_name = f"{r[0]['characterName']}({r[0]['spec']} {r[0]['class']}) ilvl: {ilvl}"
    embed_color = 0xFF0000
    embed_author_url = f"https://www.warcraftlogs.com/character/{region}/{realm}/{name}?mode=detailed&zone=23" \
              f"#difficulty={target_difficulty}"
    embed = discord.Embed(title=embed_author_title, color=embed_color)
    embed.set_author(name=embed_author_name,url=embed_author_url,icon_url="https://dmszsuqyoe6y6.cloudfront.net/img/warcraft/favicon.png")


    # construct ordered list of raids
    raid_order = ["Abyssal Commander Sivara", "Blackwater Behemoth", "Radiance of Azshara", "Lady Ashvane", "Orgozoa",
                  "The Queen's Court", "Za'qul", "Queen Azshara"]
    raid_list_ordered = []
    percentile_list = []
    for raid in raid_order:
        for item in r:
            difficulty = item["difficulty"]
            if difficulty == target_difficulty:
                if item["encounterName"] == raid:
                    raid_list_ordered.append(item)
                    percentile_list.append(item["percentile"])

    # check raid_list_ordered for duplicates, remove the duplicate with lowest percentile
    for raid in raid_list_ordered:
        for worse in raid_list_ordered:
            if raid["encounterName"] == worse["encounterName"]:
                if worse["percentile"] < raid["percentile"]:
                    raid_list_ordered.remove(worse)

    # create fields
    for item in raid_list_ordered:
        encounter = item["encounterName"]
        percentile = item["percentile"]
        duration = item["duration"]
        duration_minutes = round(((duration / 1000) // 60))
        duration_seconds = round((((duration / 1000) / 60) % 1) * 60)
        if duration_seconds < 10:
            duration_seconds = "0" + str(duration_seconds)
        message = f"{percentile}%  ({duration_minutes}:{duration_seconds})"
        embed.add_field(name=f"-{encounter}-", value=message, inline=True)

    # calculate averages, put in field
    p_average = average(percentile_list)
    embed.insert_field_at(0, name=f"Average Percentile", value=p_average, inline=False)

    return embed










