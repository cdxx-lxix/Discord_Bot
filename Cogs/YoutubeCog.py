from discord.ext import commands
import discord
import db_handler


def sendFormatted(message: str, array):
    return '{0} {1}'.format(message, array)


def setup(bot):
    bot.add_cog(youtube(bot))


class youtube(commands.Cog, name='Youtube'):
    def __init__(self, bot):
        self.bot = bot

    # Adding a new video to the DB. ID : NAME : URL : OWNER
    @commands.command(name='adv', help='Adds a video to the database. .vi name URL')
    async def add_video(self, ctx, name: str, url):
        owner = ctx.author.id  # Retrieving discord UNIQUE id
        output = db_handler.newRecord(name.lower(), url, owner)  # Passing values to db_handler then magic happens
        if output:
            await ctx.send(f"Your video *{name}* is now in our DB.")
        else:
            await ctx.send(f"Name must be UNIQUE or some unknown error occured.")

    # Sending a message with embeded video. Search query NAME or ID.
    @commands.command(name='vi', help='Sends a message with your video - .vi name')
    async def find_video(self, ctx, search_query: str):
        search_output = db_handler.sendRecord(search_query.lower())  # Passing values to db_handler then magic happens
        if search_output:
            await ctx.send(search_output)
        else:
            await ctx.send("Nothing found")

    # Erasing a record from the DB. Search query NAME or ID.
    @commands.command(name='erv', help='Erases a video from our DB (if you are an owner) - .erv name')
    async def del_video(self, ctx, erase_query):
        owner = int(ctx.author.id)  # Retrieving discord UNIQUE id
        action = db_handler.eraseRecord(erase_query.lower(), owner)  # Passing values to db_handler then magic happens
        if action:
            await ctx.send(f"Video {erase_query} annihilated.")
        else:
            await ctx.send(f"Can't do. It's either a bad name or you'r not an owner.")

    # Special command to show all of the records in the DB.
    @commands.command(name='show', help='Shows all of the records. TESTING & OWNER ONLY.')
    @commands.is_owner()
    async def test_video(self, ctx):
        result = db_handler.adminShowAll()
        await ctx.send(sendFormatted("DB consists of: ", result))

    # Shows all of the videos added by message author
    @commands.command(name='mv', help='Shows all of your videos.')
    async def show_records(self, ctx):
        owner = ctx.author.id  # Retrieving discord UNIQUE id
        output = db_handler.showUserRecords(owner)
        if len(output) != 0:
            await ctx.send(sendFormatted("Your videos: ", output))
        else:
            await ctx.send(f"You have no videos :( Want to add some? Type .adv + name + URL")

    # Shows all of the videos added by mentioned user
    @commands.command(name='vof', help='Shows all of the mentioned user videos')
    async def videosOf(self, ctx, user: discord.Member):
        owner_id = user.id
        output = db_handler.showUserRecords(owner_id)
        if len(output) != 0:
            await ctx.send(sendFormatted(f"{user} videos: ", output))
        else:
            await ctx.send(f"This user got no videos")
