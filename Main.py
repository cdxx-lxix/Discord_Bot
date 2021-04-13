# Discord bot v1 by Pizzaz
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import db_handler

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(command_prefix='.')


    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    # Dice roll simulation.
    @bot.command(name='rl', help='Rolling dice(s). Example: .rl 2 6')
    async def roll(ctx, number_of_dice: int, number_of_sides: int):
        if number_of_dice != 0 and number_of_sides != 0:  # I don't want zeroes here. Zeroes do 50006 error.
            dice = [
                str(random.choice(range(1, number_of_sides + 1)))
                for _ in range(number_of_dice)
            ]
            await ctx.send(', '.join(dice))
        else:
            await ctx.send("No zeroes boyo")

    # Creating a teams out of list of given names and desired teams number.
    @bot.command(name='ts', help='Assemble teams - .ts / name,name,name... / number of teams')
    async def teams(ctx, buddies, number_of_teams: int):
        players = list(buddies.split(','))  # Transforming strings into a beautiful LIST
        players_in_teams = int(len(players) / number_of_teams)  # Gotta cast it into INT (default FLOAT)
        if number_of_teams != 0:  # I don't want to divide by zero and I won't
            if len(players) % number_of_teams == 0:  # I want teams to be always equal
                for x in range(number_of_teams):  # Creating a team segment separation
                    temp_team = []  # Temp list for storing randomly picked names for a beautiful printing
                    for y in range(
                            players_in_teams):  # Iterating over given names to randomly assign players in the teams
                        current = players.index(random.choice(players))  # Currently picked name from a given list INDEX
                        temp_item = players[current]  # Currently picked name from a given list STRING
                        temp_team.append(temp_item)  # Filling temp list
                        players.pop(current)  # Removing picked name so it won't appear again

                    await ctx.send(f'Team {x}: {temp_team}')

            else:
                await ctx.send("Teams aren't equal. You need more players or less teams.")

    # Adding a new video to the DB. ID : NAME : URL : OWNER
    @bot.command(name='adv', help='Adds a video to the database. .vi name URL')
    async def add_video(ctx, name: str, url):
        owner = ctx.author.id  # Retrieving discord UNIQUE id
        output = db_handler.newRecord(name.lower(), url, owner)  # Passing values to db_handler then magic happens
        if output:
            await ctx.send(f"Your video *{name}* is now in our DB.")
        else:
            await ctx.send(f"Name must be UNIQUE or some unknown error occured.")

    # Sending a message with embeded video. Search query NAME or ID.
    @bot.command(name='vi', help='Sends a message with your video - .vi name')
    async def find_video(ctx, search_query: str):
        search_output = db_handler.sendRecord(search_query.lower())  # Passing values to db_handler then magic happens
        if search_output:
            await ctx.send(search_output)
        else:
            await ctx.send("Nothing found")

    # Erasing a record from the DB. Search query NAME or ID.
    @bot.command(name='erv', help='Erases a video from our DB (if you are an owner) - .erv name')
    async def del_video(ctx, erase_query):
        owner = int(ctx.author.id)  # Retrieving discord UNIQUE id
        action = db_handler.eraseRecord(erase_query.lower(), owner)  # Passing values to db_handler then magic happens
        if action:
            await ctx.send(f"Video {erase_query} annihilated.")
        else:
            await ctx.send(f"Can't do. It's either a bad name or you'r not an owner.")

    # Special command to show all of the records in the DB.
    @bot.command(name='show', help='Shows all of the records. TESTING & OWNER ONLY.')
    @commands.is_owner()
    async def test_video(ctx):
        result = db_handler.adminShowAll()
        await ctx.send(sendFormatted("DB consists of: ", result))

    # Shows all of the videos added by message author
    @bot.command(name='mv', help='Shows all of your videos.')
    async def show_records(ctx):
        owner = ctx.author.id  # Retrieving discord UNIQUE id
        output = db_handler.showUserRecords(owner)
        if len(output) != 0:
            await ctx.send(sendFormatted("Your videos: ", output))
        else:
            await ctx.send(f"You have no videos :( Want to add some? Type .adv + name + URL")

    # Shows all of the videos added by mentioned user
    @bot.command(name='vof', help='Shows all of the mentioned user videos')
    async def videosOf(ctx, user: discord.Member):
        owner_id = user.id
        output = db_handler.showUserRecords(owner_id)
        if len(output) != 0:
            await ctx.send(sendFormatted(f"{user} videos: ", output))
        else:
            await ctx.send(f"This user got no videos")

    # Shows your unique discord id
    @bot.command(name='myid', help='Shows your unique discord id.')
    async def show_id(ctx):
        owner = ctx.author.id
        await ctx.send(f"Your id: {owner}")

    # Shows unique id of a mentioned person
    @bot.command(name="idof", help='Shows unique discord id of @someone')
    async def id_of(ctx, user: discord.Member):
        await ctx.send(f"ID of {user} is: {user.id}")

    def sendFormatted(message: str, array):
        return '{0} {1}'.format(message, array)


    bot.run(TOKEN)
