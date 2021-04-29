# Discord_Bot
Basic discord bot 

In order to use you need to add a *.env* file in the root with your discord token. 
It looks like this:

```
# .env

DISCORD_TOKEN = ...your token...
```

All of the packages are included (discord.py, pythond-dotenv.py, youtube-search.py, urllib.py) along with venv.

What can this guy do?: 

```
Steam:
  look Search steam game by name
Utilities:
  idof Shows unique discord id of @someone
  myid Shows your unique discord id.
  rl   Rolling dice(s). Example: .rl 2 6
  ts   Assemble teams - .ts / name,name,name... / number of teams
Youtube:
  adv  Adds a video to the database. .vi name URL
  erv  Erases a video from our DB (if you are an owner) - .erv name
  mv   Shows all of your videos.
  show Shows all of the records. TESTING & OWNER ONLY.
  vi   Sends a message with your video - .vi name
  vof  Shows all of the mentioned user videos
No Category:
  help Shows this message
  ```
  
### Some previews:

#### .look
![alt text](https://cdn.discordapp.com/attachments/799824814709800962/837264334668693504/unknown.png "Preview of .look")

#### .vi 
![alt text](https://cdn.discordapp.com/attachments/799824814709800962/837264927990743070/unknown.png "Preview of .vi")

#### .myid and .idof 
![alt text](https://cdn.discordapp.com/attachments/799824814709800962/837265999144419338/unknown.png "Preview of .myid") ![alt text](https://cdn.discordapp.com/attachments/799824814709800962/837266127146057789/unknown.png "Preview of .idof")
