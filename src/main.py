import os
import logging

import argparse
import discord
from discord import app_commands

from logging_config import setup_logging
import config
import bot.discord_commands
from bot.views import reload_register_requests

setup_logging()

logger = logging.getLogger()

parser = argparse.ArgumentParser()

parser.add_argument("--test", action="store_true", default=False)

args = parser.parse_args()

if args.test:
    discordBotToken = os.getenv("TEST_TOKEN")
    account_request_channel = 1350509785316982815
    logging.info("bot running in TEST mode")
else:
    discordBotToken = os.getenv("TOKEN")
    account_request_channel = 1350509157538730024
    logging.info("bot running in GLOBAL mode")

# Discord bot setup
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot.discord_commands.load_commands(tree,client)


@client.event
async def on_ready():
    await tree.sync()
    reload_register_requests(client=client)
    print(f"Logged in as {client.user}")
# Run the bot
client.run(discordBotToken)  # Replace with your Discord bot token
