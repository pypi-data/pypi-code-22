import discord
import os
import pkg_resources
from discord.ext import commands
import asyncio
import aiml
import requests


STARTUP_FILE = "std-startup.xml"
BOT_PREFIX = '?'


class ChattyCathy:
    def __init__(self, channel_name, bot_token):
        self.channel_name = channel_name
        self.token = bot_token

        # Load AIML kernel
        self.aiml_kernel = aiml.Kernel()
        initial_dir = os.getcwd()
        os.chdir(pkg_resources.resource_filename(__name__, '')) # Change directories to load AIML files properly
        startup_filename = pkg_resources.resource_filename(__name__, STARTUP_FILE)
        self.aiml_kernel.learn(startup_filename)
        self.aiml_kernel.respond("LOAD AIML B")
        os.chdir(initial_dir)

        # Set up Discord client
        self.discord_client = discord.Client()
        self.discord_client = commands.Bot(command_prefix=BOT_PREFIX)
        self.setup()

    def setup(self):

        @self.discord_client.event
        @asyncio.coroutine
        def on_ready():
            print("Bot Online!")
            print("Name: {}".format(self.discord_client.user.name))
            print("ID: {}".format(self.discord_client.user.id))
            yield from self.discord_client.change_presence(game=discord.Game(name='Chatting with Humans'))

        @self.discord_client.event
        @asyncio.coroutine
        def on_message(message):
            if message.author.bot or str(message.channel) != self.channel_name:
                return

            print("Message: " + str(message.content))

            if message.content.startswith(BOT_PREFIX):
                # Pass on to rest of the client commands
                yield from self.discord_client.process_commands(message)
            else:
                aiml_response = self.aiml_kernel.respond(message.content)
                yield from self.discord_client.send_message(message.channel, aiml_response)

        @self.discord_client.command(pass_context=True)
        @asyncio.coroutine
        def bitcoin(context):
            """Get the current Bitcoin price"""
            # Get the BTC price from CoinDesk
            bitcoin_price_url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
            data = requests.get(bitcoin_price_url).json()
            price_in_usd = data['bpi']['USD']['rate']
            yield from self.discord_client.say("Bitcoin is currently worth $" + price_in_usd + " USD.")

    def run(self):
        self.discord_client.run(self.token)
