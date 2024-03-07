import discord
import toml


def load_config(config_name = "config.toml"):
	with open(config_name, "r") as f:
		data = toml.load(f)

		token = data['token']['token']
	return token

def main():
	token = load_config()

	class MyClient(discord.Client):
		async def on_ready(self):
			print(f'Logged on as {self.user}!')

		async def on_message(self, message):
			if str(message.author) == "1llya":
				print("HAHAHAHA")
			else:
				print(f'{message.author}: {message.content}')
				print(type(message.author))

	intents = discord.Intents.default()
	intents.message_content = True

	client = MyClient(intents=intents)
	client.run(token)

if __name__ == "__main__":
	main()