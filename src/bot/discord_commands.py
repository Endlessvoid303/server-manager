import logging
import re

import discord
from discord import app_commands

import enums
import exceptions
from bot.messages import Message, edit_message, send_message, send_to_channel
from bot.views import RegisterRequest
from classes.user import User

color_green = 65313
color_red = 16711680
color_orange = 11625728
OWNER_ID = 1079043553327583332


def load_commands(tree: app_commands.CommandTree, discordclient: discord.Client):
	client: discord.Client = discordclient

	@tree.error
	async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
		if isinstance(error, app_commands.CheckFailure):
			# Send a friendly message instead of a generic error
			# noinspection PyUnresolvedReferences
			permission_embed = discord.Embed(color=color_red, title="❌ No permission", description="You can not use this command")
			await interaction.response.send_message(embed=permission_embed, ephemeral=True)
		else:
			logging.error(error)
			if interaction.response.is_done():
				await interaction.edit_original_response(embed=discord.Embed(color=color_red, title="❌ error", description=F"something went wrong ¯\\_(ツ)_/¯\n{error}"))
			else:
				await interaction.response.send_message(embed=discord.Embed(color=color_red, title="❌ error", description=F"something went wrong ¯\\_(ツ)_/¯\n{error}"))

	@app_commands.describe(password="Password Required, 9 to 36 characters, must include uppercase and lowercase letters, and numbers")
	@tree.command(name="register", description="request a user account")
	async def register(interaction: discord.Interaction, password: str):
		pending_message = Message(title="⌛adding user account", description=F"adding user account for {interaction.user}", color=enums.BorderColor.color_orange)
		await send_message(pending_message, interaction)
		try:
			if not (re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d\W]{9,36}$", password) and (9 <= len(password) <= 36)):
				raise exceptions.PasswordRequirementError
			user = User.create_user(interaction.user.id, interaction.user.name, password)
			channel = client.get_channel(enums.Channels.ACCOUNT_REQUEST_CHANNEL.value)
			requestmessage = Message(title="Account request", description=F"{interaction.user.name} requested a account", color=enums.BorderColor.color_green, view=RegisterRequest(user.user_id))
			await send_to_channel(channel, requestmessage)
		except exceptions.PasswordRequirementError:
			error_message = Message(title="❌ password requirements not met", description="Password Requires 9 to 36 characters, must include uppercase and lowercase letters, and numbers",
			                        color=enums.BorderColor.color_red)
			await edit_message(error_message, interaction)
		except exceptions.UserExistsError:
			error_message = Message(title="❌ account already exists", description="you already have an account", color=enums.BorderColor.color_red)
			await edit_message(error_message, interaction)
		else:
			succes_message = Message(title="✅ User account requested", description=F"Account requested for {interaction.user}", color=enums.BorderColor.color_green)
			await edit_message(succes_message, interaction)

	@tree.command(name="delete_account", description="delete a user account")
	async def delete_account(interaction: discord.Interaction, discord_user: discord.Member):
		pending_message = Message(title="⌛deleting user account", description=F"user {discord_user} is being deleted", color=enums.BorderColor.color_orange)
		await send_message(pending_message, interaction)
		try:
			user = User.load_user_by_name(discord_user.name)
			user.delete()
		except exceptions.UserDoesNotExistError:
			error_message = Message(title="❌ account does not exist", description="user does not exist", color=enums.BorderColor.color_red)
			await edit_message(error_message, interaction)
		else:
			succes_messsage = Message(title="✅user account deleted", description=F"user {discord_user} has been deleted", color=enums.BorderColor.color_green)
			await edit_message(succes_messsage, interaction)
