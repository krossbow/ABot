import discord as D
import asyncio
import sys

__name__ = "ABot" # Program name.
prefix = __name__[0] + '!'
DB = "files" # An actual plaintext file named "./files".
"""
How to format you piracy database:
Path_to_file:Name_to_display [line break]
"""

HELP = {
	"help": ["shows this help message."],
	"search [str]": ["search for content",
		"searches the bot's database for [str]."],
	"dir": ["shows all content in database."],
	"get [int]": ["fetch a file.",
	"receives a file with the ID of [int]."]
}

CLIENT = D.Client()

@CLIENT.event
async def on_ready(): # Logged in.
	GAME = D.Game(name=prefix + "help")
	await CLIENT.change_presence(game=GAME)

	print("Logged in as", CLIENT.user.name)
	print("ID", CLIENT.user.id)
	print("Foi, ☭.")

@CLIENT.event
async def on_message(message):
	if message.content.startswith(prefix):
		print("Got from", message.author, ":", message.content) # Debugging.

	ARGS = message.content.split()[1:]

	def GET(CMD : str):
		return (message.content.startswith(prefix + CMD))

	if GET("help"):
		try:
			ARGS[0]
		except IndexError:
			MSG = """
Help for {0}:\n
Usage: {1}[COMMAND].
{1}help [COMMAND] for extended help.

COMMANDs:
""".format(__name__, prefix)

			for NAME in HELP:
				TO_APPEND = NAME + ": " + HELP[NAME][0] + "\n"
				MSG += TO_APPEND

			await CLIENT.send_message(message.author, MSG) # Split file into multiple parts.

		else:
			try:
				HELP[ARGS[0]][1]
			except IndexError:
				await CLIENT.send_message(message.author, "Extended help for \"{0}\" not found.".format(ARGS[0]))
			else:
				await CLIENT.send_message(message.author, ARGS[0] + ": " + HELP[ARGS[0]][1])

	def LIST_DEF():
		FILES = ""
		LIST = open(DB, "r")
		while True:
			LINE = LIST.readline()
			if LINE == '':
				break
			FILES += LINE
		return FILES

	if GET("dir"):
		ENTRY = LIST_DEF()
		for LINE in ENTRY.split('\n'):
			SPLIT = LINE.split(":")

			try:
				await CLIENT.send_message(
					message.author,
					"```{0} - ID: {1}```".format(
						SPLIT[-2],
						SPLIT[-1]
					)
				)
			except IndexError: # Don't know what causes; don't care.
				break

	elif GET("search"):
		# path:name:ID

		try:
			ARGS[0]
		except IndexError:
			await CLIENT.send_message(message.author, "Error: wrong usage, try {0}help".format(prefix))
		else: # It works.
			for LINE in LIST_DEF().split('\n'):
				SPLIT = LINE.split(":")

				try:
					if ARGS[0].lower() in SPLIT[1].lower():
						await CLIENT.send_message(
							message.author,
							"```{0} - ID: {1}```".format(SPLIT[-2], int(SPLIT[-1]))
					)
					else:
						await CLIENT.send_message(
							message.author,
							"Could not find what you were searching for - {}. :(".format(ARGS[0])
						)
				except IndexError:
					pass # It is 4 AM and I have stopped caring.

	elif GET("get"):
		for PARAM in ARGS:
			try:
				int(PARAM)
			except ValueError:
				await CLIENT.send_message(
					message.channel,
					"Error: argument \"{0}\" not an integer ID.".format(PARAM)
				)
			else: # It works.
				for LINE in LIST_DEF().split('\n'):
					if LINE.split(":")[-1] == PARAM:
						await CLIENT.send_file(
							destination=message.author,
							fp=LINE.split(":")[0],
							content=LINE.split(":")[1]
						)

		return

try:
	sys.argv[1]
except IndexError:
	print("Could not find token in command-line arguments, try {} [token]".format(sys.argv[0]))
	exit()
else:
	CLIENT.run(sys.argv[1])

