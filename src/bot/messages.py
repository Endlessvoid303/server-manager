import discord
import logging
import enums


class Message:
    def __init__(self, title: str, description: str, color: enums.BorderColor, personal: bool = False,
                 view: discord.ui.View = None):
        self.title = title
        self.description = description
        self.color = color
        self.personal = personal
        self.view = view

async def edit_original_message(original_message: discord.Message, message: Message):
    logging.info(f"Editing original message")
    embed = discord.Embed(title=message.title, description=message.description, color=message.color.value)
    await original_message.edit(embed=embed, view=message.view)


async def send_to_channel(channel: discord.TextChannel, message: Message):
    await channel.send(
        embed=discord.Embed(
            color=message.color.value,
            title=message.title,
            description=message.description
        )
        ,view=message.view
    )
    logging.debug("message sent to channel")


async def edit_message(message: Message, interaction: discord.Interaction):
    logging.info(f"Editing message")
    embed = discord.Embed(title=message.title, description=message.description, color=message.color.value)
    return await interaction.edit_original_response(embed=embed, view=message.view)


async def send_message(message: Message, interaction: discord.Interaction):
    logging.info(f"Sending message")
    embed = discord.Embed(title=message.title, description=message.description, color=message.color.value)
    if message.view is not None:
        return await interaction.response.send_message(embed=embed, view=message.view)
    else:
        return await interaction.response.send_message(embed=embed)