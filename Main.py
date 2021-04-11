# Discord bot v1 by Pizzaz
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
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))

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
    @bot.command(name='show', help='Shows all of the records. TESTING & ADMIN ONLY.')
    async def test_video(ctx):
        result = db_handler.adminShowAll()
        await ctx.send(result)


    bot.run(TOKEN)
