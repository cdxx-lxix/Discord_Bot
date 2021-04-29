import json
import urllib.request
from youtube_search import YoutubeSearch
import discord
from discord.ext import commands


# Iterate over 500k of steam entries but return only the first match. Very strict and sensitive input.
def GetAppId(namequery):
    file = urllib.request.urlopen("http://api.steampowered.com/ISteamApps/GetAppList/v2")
    games = json.load(file)
    print(namequery)
    for tempdict in games['applist']['apps']:
        for _ in tempdict.items():
            if tempdict['name'].lower() == namequery.lower():
                print(tempdict['appid'], tempdict['name'])
                lookID = tempdict['appid']
                return lookID


#  Takes title and returns trailer of the game (hopefully)
def getTrailer(game):
    full_query = game + 'trailer'
    search = YoutubeSearch(full_query, max_results=1).to_json()
    json_object = json.loads(search)
    for item in json_object['videos']:
        postfix = item.get('url_suffix')
        return 'https://www.youtube.com' + postfix


#  Generates a list of data for embed message via Steam API detailed game info. Takes appid from GetAppId()
def GameInfo(appid):
    file = urllib.request.urlopen(f"https://store.steampowered.com/api/appdetails?appids={appid}")
    the_game = json.load(file)
    is_free_to_play = the_game[f'{appid}']['data']['is_free']
    if is_free_to_play:
        price = 'Free'
    else:
        price = the_game[f'{appid}']['data']['price_overview']['final_formatted']
    developers = the_game[f'{appid}']['data']['developers']
    publishers = the_game[f'{appid}']['data']['publishers']
    release = the_game[f'{appid}']['data']['release_date']['coming_soon']
    if not release:
        release_date = the_game[f'{appid}']['data']['release_date']['date']
    else:
        release_date = 'TBA'
    description = the_game[f'{appid}']['data']['short_description']
    title = the_game[f'{appid}']['data']['name']
    trailer = getTrailer(title)
    store_url = f'https://store.steampowered.com/app/{appid}'
    thumbnail = the_game[f'{appid}']['data']['background']

    # Return [0]    [1]       [2]         [3]         [4]          [5]         [6]       [7]         [8]
    return [title, price, description, developers, publishers, release_date, trailer, store_url, thumbnail]


class steam(commands.Cog, name='Steam'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='look', help='Search steam game by name')
    async def LookForGame(self, ctx, *, gamename: str):
        try:
            appid = GetAppId(gamename)
            print(appid)
            recieved_info = GameInfo(appid)
            print(recieved_info)
            message = discord.Embed(title=recieved_info[0],
                                    url=recieved_info[7],
                                    description=recieved_info[2],
                                    color=discord.Color.blue())

            message.add_field(name='Price: ', value=recieved_info[1])
            message.add_field(name='Devs: ', value=recieved_info[3])
            message.add_field(name='Pubs: ', value=recieved_info[4])
            message.set_thumbnail(url=recieved_info[8])
            message.set_footer(text=f'Release date: {recieved_info[5]}')
            message.set_author(name='Watch trailer', url=recieved_info[6])
            await ctx.send(embed=message)
        except Exception as e:
            await ctx.send(f'Nope. Error occured: {e}')


def setup(bot):
    bot.add_cog(steam(bot))
