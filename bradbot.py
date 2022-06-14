import discord, os, json, random
from dotenv import load_dotenv
import messagedb

load_dotenv('.env')
TOKEN = os.getenv("TESTTOKEN")

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
		print("%-25s %-35s Brad said:'%s'" %(server, author, line[0]))
		sent = await message.channel.send(line[0])
		messagedb.addMessage(sent.id, sent.guild.id, sent.guild.name, line[0], line[1], message.author.id, message.author.name)

@client.event
async def on_guild_join(guild):
	print("BradBot joined server: '{}'".format(guild.name))

@client.event
async def on_reaction_add(reaction, user):
	if reaction.message.author == client.user:
		message_id = reaction.message.id
		msg_info = messagedb.getMessageInfo(message_id)
		if msg_info != [] and len(reaction.message.reactions) == 1:
			embed=discord.Embed(title="Match {}".format(msg_info[0][4]), url="https://opendota.com/matches/{}/chat".format(msg_info[0][4]), color=0xff0000)
			embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/940421411024011275/986373541601640518/unknown.png")
			print("%-25s %-35s Match ID fetched:'%s'" %(reaction.message.guild.name, "N/A", msg_info[0][4]))
			await reaction.message.reply(embed=embed)

client.run(TOKEN)