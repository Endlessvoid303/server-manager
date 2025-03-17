import logging

import discord
from discord import Message

import config
import enums
import exceptions
from classes.databaseconnection import DatabaseConnection
from classes.user import User
import bot.discord_commands
from bot import messages
from bot.messages import edit_original_message

class RegisterRequest(discord.ui.View):
    def __init__(self,user_id:int):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.allow_id = f"allow_signin_{user_id}"
        self.block_id = f"block_signin_{user_id}"
        self.allow_button = discord.ui.Button(label="Allow", style=discord.ButtonStyle.success,custom_id=self.allow_id)
        self.block_button = discord.ui.Button(label="Block", style=discord.ButtonStyle.danger,custom_id=self.block_id)
        self.allow_button.callback = self.allow_signin
        self.block_button.callback = self.block_signin
        self.add_item(self.allow_button)
        self.add_item(self.block_button)
        logging.info(f"Confirm Button ID: {self.allow_id}")
        logging.info(f"Cancel Button ID: {self.block_id}")

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Ensures only the correct user can interact with their buttons."""
        if not config.is_owner(interaction.user.id):
            await interaction.response.send_message("❌ you are not allowed to do this", ephemeral=True)
            return False
        return True

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item):
        """Catch errors in the view."""
        await interaction.response.send_message("An error occurred.", ephemeral=True)
        logging.error(f"Error: {error}")


    async def allow_signin(self, interaction: discord.Interaction):
        logging.info(f"Button Clicked: {interaction.data['custom_id']}")
        user = User.load_user(self.user_id)
        user.not_reviewed()
        user.allow_user()
        message:Message = interaction.message
        if message is None:
            raise exceptions.MessageNotFoundError
        succes_message = messages.Message(title="✅ user allowed",description=F"user {user.name} is now allowed", color=enums.BorderColor.color_green)
        await edit_original_message(message,succes_message)

    async def block_signin(self, interaction: discord.Interaction):
        logging.info(f"Button Clicked: {interaction.data['custom_id']}")
        user = User.load_user(self.user_id)
        user.not_reviewed()
        user.block_user()
        message: Message = interaction.message
        if message is None:
            raise exceptions.MessageNotFoundError
        succes_message = messages.Message(title="🛑 user blocked",description=F"user {user.name} is now blocked",color=enums.BorderColor.color_green)
        await edit_original_message(original_message=message,message=succes_message)

def reload_register_requests(client: discord.Client):
    db = DatabaseConnection()
    data = db.find("SELECT id FROM users WHERE isReviewed = False")
    db.complete()
    for row in data:
        client.add_view(RegisterRequest(row[0]))