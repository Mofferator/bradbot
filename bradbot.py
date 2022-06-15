import discord, os, json, random
from dotenv import load_dotenv
import messagedb

if os.path.exists('.env'):
	PATH_PREFIX = ""
else:
	PATH_PREFIX = "/home/Mofferator/BradBot/bradbot/"

load_dotenv('{}.env'.format(PATH_PREFIX))
TOKEN = os.getenv("TOKEN")


client = discord.Client()

with open("{}brad.txt".format(PATH_PREFIX)) as f:
	words = json.load(f)
	print("{} bradlines loaded".format(len(words)), flush=True)

with open("{}image_urls.json".format(PATH_PREFIX)) as urls:
	image_urls = json.load(urls)
	print("{} brad faces loaded".format(len(image_urls)), flush=True)

def hasPerms(member, perms):
  for role in reversed(member.roles):
    if not perms.is_subset(role.permissions):
        return False
  return True

@client.event
async def on_ready():
	print("Logged in as {0.user}".format(client), flush=True)

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith("$bradbot"):
		line = random.choice(words)
		author = message.author.name
		server = message.guild.name
		print("%-25s %-35s Brad said:'%s'" %(server, author, line[0]), flush=True)
		sent = await message.channel.send(line[0])
		messagedb.addMessage(sent.id, sent.guild.id, sent.guild.name, line[0], line[1], message.author.id, message.author.name)

	if message.content.startswith("$bradface"):
		url = random.choice(image_urls)
		await message.channel.send(url)

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