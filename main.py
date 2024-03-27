import discord
import asyncio
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  
intents.guilds = True  

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    print(message.content)

    print("OK")

    if message.content.startswith('!transfer'):
        # Acknowledge command receipt
        await message.channel.send("Transfer command received. Processing...")
        await transfer_messages(message.channel, message.content)


async def transfer_messages(current_channel, command):
    try:
        # Command format: !transfer source_channel_id dest_channel_id
        _, source_id, dest_id = command.split()
        source_channel = client.get_channel(int(source_id))
        dest_channel = client.get_channel(int(dest_id))
    except ValueError:
        await current_channel.send("Invalid command format. Use `!transfer <source_channel_id> <dest_channel_id>`.")
        return
    except TypeError:
        await current_channel.send("One or both of the provided channel IDs are invalid.")
        return

    if not source_channel or not dest_channel:
        await current_channel.send("One or both of the channels could not be found.")
        return

    try:
        start_date = datetime.datetime(2019, 1, 1)
        # Fetch up to 2369 messages from the source channel.
        messages = [msg async for msg in source_channel.history(limit=2369, after=start_date)]
        # Reversed to maintain the original order when reposting (newest first)
        for msg in reversed(messages):

            for reaction in msg.reactions:

                if isinstance(reaction.emoji, str):
                    if reaction.emoji=='🐐':
                        for attachment in msg.attachments:
                            await dest_channel.send(f"{msg.author.name}: {attachment.url}")
                        

                else:
                    # For custom Discord emojis (object), access the 'name' attribute
                    emoji_name = reaction.emoji.name
                    print(emoji_name)
                    if emoji_name == "CapraRaku" or emoji_name=="goat":
                        for attachment in msg.attachments:
                            await dest_channel.send(f"{msg.author.name}: {attachment.url}")

    except discord.errors.Forbidden:
        await current_channel.send("I don't have the necessary permissions to perform this task.")

client.run('NOT-LEAKING-IT-THIS-TIME')
