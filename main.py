import os
import sys
import discord
from discord.client import _ClientEventTask
from dotenv import load_dotenv
import re

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, '.env'))

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

server_id = int(os.getenv('SERVER_ID'))
print(server_id)
bot_test = int(os.getenv('CHANNEL_ID'))

logString = sys.argv[1]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    server = discord.utils.find(lambda g: g.id == server_id, client.guilds)
    # for guild in client.guilds:
    #     print(
    #         f'{client.user} is connected to the following guild:\n'
    #         f'{guild.name}(id: {guild.id})'
    #     )
    #     if guild.id == server_id:
    #         server = guild

    print(server.id)
    print(server.channels)

    channel = discord.utils.find(lambda x: x.id == bot_test, server.channels)
    print(channel)
    print(server.roles)
    role = discord.utils.find(lambda x : "factory" in x.name.lower(), server.roles)
    print(role)
    print(logString)
    if match := re.search(r"Join succeeded: (.*)", logString):
        print(match.groups()[0])
        await channel.send(f"{role.mention} {match.groups()[0]} just logged in!")

    exit(0)


if __name__ == "__main__":

    client.run(TOKEN)