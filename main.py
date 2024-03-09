import discord
import toml
import requests

api_url = "https://valorant-api.com/v1/agents?isPlayableCharacter=true"


class ValorantAgents:
    def __init__(self):
        data = requests.get(api_url)

        self.parsed_json = data.json()
        # for i in range(len(parsed_json['data'])):
        #     print(parsed_json['data'][i]['displayName'])

    async def names_agents(self):
        agents_list = []
        for i in range(len(self.parsed_json['data'])):
            agents_list.append(self.parsed_json['data'][i]['displayName'])

        return agents_list

        # return self.parsed_json


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


def load_config(config_name="config.toml"):
    with open(config_name, "r") as f:
        data = toml.load(f)

        token = data['token']['token']
    return token


def main():

    token = load_config()

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(token)


if __name__ == "__main__":
    main()

