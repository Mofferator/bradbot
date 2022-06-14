import sqlite3

conn = sqlite3.connect('messages.db')

c = conn.cursor()

def init():
	c.execute("""CREATE TABLE IF NOT EXISTS messages 
		(
		message_id integer, 
		guild_id integer,
		guild_name text,
		message_content text, 
		match_id integer,
		requester_id integer,
		requester_name text
		)""")
	conn.commit()

def main():
	init()

def addMessage(message_id, guild_id, guild_name, message_content, match_id, requester_id, requester_name):
	c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)", (message_id, guild_id, guild_name, message_content, match_id, requester_id, requester_name))
	conn.commit()

def getMessageInfo(message_id):
	c.execute("SELECT * FROM messages WHERE message_id = ?", (message_id,))
	return c.fetchall()

if __name__ == '__main__':
	main()