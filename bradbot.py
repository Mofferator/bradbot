import discord, os, json, random
from dotenv import load_dotenv
import messagedb

if os.path.exists('.env'):
	PATH_PREFIX = ""
else:
	PATH_PREFIX = "/home/Mofferator/BradBot/bradbot/"

load_dotenv('{}.env'.format(PATH_PREFIX))
TOKEN = os.getenv("TESTTOKEN")


client = discord.Client()

with open("{}brad.txt".format(PATH_PREFIX)) as f:
	words = json.load(f)
	print("{} bradlines loaded".format(len(words)), flush=True)

with open("{}image_urls.json".format(PATH_PREFIX)) as urls:
	image_urls = json.load(urls)
	print("{} brad faces loaded".format(len(image_urls)), flush=True)

def bradbot(message):
	line = random.choice(words)
	author = message.author.name
	server = message.guild.name
	print("%-25s %-35s Brad said:'%s'" %(server, author, line[0]), flush=True)
	return line

def bradface(message):
	return random.choice(image_urls)

def bradhelp(message):
	embed=discord.Embed(title="Brad Bot Help", url="https://github.com/Mofferator/bradbot", color=0xff0000)
	embed.set_thumbnail(url=random.choice(image_urls))
	embed.add_field(name="Brad Bot", value="Type `bradbot` to make Brad Bot say one of his {} all chat lines at random".format(len(words)), inline=False)
	embed.add_field(name="Brad Bot React", value="React to any of Brad Bot's all chat lines to get a link to the match", inline=False)
	embed.add_field(name="Brad Face", value="Type `$bradface` to see a random picture of Bradley Dragon", inline=False)
	return embed

def listServers():
	print("{} is in {} servers:".format(client.user, len(client.guilds)), flush=True)
	for guild in client.guilds:
		print("\t{}".format(guild.name), flush=True)

@client.event
async def on_ready():
	print("Logged in as {0.user}".format(client), flush=True)

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith("$bradbot"):
		msg = bradbot(message)
		sent = await message.channel.send(msg[0])
		messagedb.addMessage(sent.id, sent.guild.id, sent.guild.name, msg[0], msg[1], message.author.id, message.author.name)

	if message.content.startswith("$bradface"):
		msg = bradface(message)
		await message.channel.send(msg)
		print("%-25s %-35s Bradface:'%s'" %(message.guild.name, message.author, ":)"), flush=True)

	if message.content.startswith("$bradhelp"):
		await message.reply(embed=bradhelp(message))
		print("%-25s %-35s Requested help" %(message.guild.name, message.author), flush=True)

	if message.content.startswith("$listservers"):
		listServers()

@client.event
async def on_guild_join(guild):
	print("BradBot joined server: '{}'".format(guild.name), flush=True)

@client.event
async def on_reaction_add(reaction, user):
	if reaction.message.author == client.user:
		if(reaction.message.channel.guild.me.guild_permissions.embed_links):
			message_id = reaction.message.id
			msg_info = messagedb.getMessageInfo(message_id)
			if msg_info != [] and len(reaction.message.reactions) == 1 and reaction.message.reactions[0].count == 1:
				embed=discord.Embed(title="Match {}".format(msg_info[0][4]), url="https://opendota.com/matches/{}/chat".format(msg_info[0][4]), color=0xff0000)
				embed.set_thumbnail(url=random.choice(image_urls))
				print("%-25s %-35s Match ID fetched:'%s'" %(reaction.message.guild.name, "N/A", msg_info[0][4]), flush=True)
				await reaction.message.reply(embed=embed)
		else:
			await reaction.message.reply(msg_info[0][4])

client.run(TOKEN)