from discord.ext import commands
import discord
import random


def setup(bot):
    bot.add_cog(utils(bot))


class utils(commands.Cog, name='Utilities'):
    def __init__(self, bot):
        self.bot = bot

    # Dice roll simulation.
    @commands.command(name='rl', help='Rolling dice(s). Example: .rl 2 6')
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        if number_of_dice != 0 and number_of_sides != 0:  # I don't want zeroes here. Zeroes do 50006 error.
            dice = [
                str(random.choice(range(1, number_of_sides + 1)))
                for _ in range(number_of_dice)
            ]
            await ctx.send(', '.join(dice))
        else:
            await ctx.send("No zeroes boyo")

    # Creating a teams out of list of given names and desired teams number.
    @commands.command(name='ts', help='Assemble teams - .ts / name,name,name... / number of teams')
    async def teams(self, ctx, buddies, number_of_teams: int):
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

    # Shows your unique discord id
    @commands.command(name='myid', help='Shows your unique discord id.')
    async def show_id(self, ctx):
        owner = ctx.author.id
        await ctx.send(f"Your id: {owner}")

    # Shows unique id of a mentioned person
    @commands.command(name="idof", help='Shows unique discord id of @someone')
    async def id_of(self, ctx, user: discord.Member):
        await ctx.send(f"ID of {user} is: {user.id}")
