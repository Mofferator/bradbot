import discord, os, json, random
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv("TOKEN")

client = discord.Client()

f = open("brad.txt")

words = json.load(f)

print("{} bradlines loaded".format(len(words)))

@client.event
async def on_ready():
	print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith("$bradbot"):
		line = random.choice(words)
		author = message.author.name
		server = message.guild.name
		print("%-25s %-25s Brad said:'%s'" %(server, author, line))
		await message.channel.send(line)

@client.event
async def on_guild_join(guild):
	print("BradBot joined server: '{}'".format(guild.name))

client.run(TOKEN)