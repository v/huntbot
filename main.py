import discord
import os
import shlex
from collections import namedtuple
from tabulate import tabulate
import re
from models import Puzzle
from datetime import datetime
from gdrive import create_spreadsheet, sheet_link

client = discord.Client()

huntbot_usage = """Huntbot

Usage:
  huntbot start <name>...
  huntbot finish <name>...
  huntbot list
  huntbot show <name>...
  huntbot (-h | --help)

Options:
  -h --help     Show help
"""

def alnum(s):
    return re.sub(r'[^a-zA-Z0-9 \-]','', s)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.content.startswith('huntbot'):
        return

    text = message.content.strip()
    parts = [alnum(s) for s in shlex.split(alnum(text))]

    if len(parts) < 2:
        await message.channel.send(huntbot_usage)
        return

    command = parts[1]

    if command == 'help':
        await message.channel.send(huntbot_usage)
        return

    if command == 'start':
        if len(parts) < 3:
            await message.channel.send(huntbot_usage)
            return

        name = ' '.join(parts[2:])
        channel = '-'.join(parts[2:]).lower()

        puz = Puzzle.get_or_none(Puzzle.name == channel)


        if not puz:
            sheet = create_spreadsheet(name)

            link = sheet_link(sheet['id'])

            topic = """Discuss the puzzle **{}**. Sheet: {}""".format(name, link)

            text_category = discord.utils.get(message.guild.categories, name='Puzzles')
            voice_category = discord.utils.get(message.guild.categories, name='Voice Channels')

            # create channel and get id
            discord_chan = await message.guild.create_text_channel(channel, topic=topic, category=text_category)
            voice_chan = await message.guild.create_voice_channel(channel, category=voice_category)

            puz = Puzzle(
                name=name,
                channel=channel,
                channel_id=discord_chan.id,
                sheet=link,
                creator=message.author,
                created_at=datetime.now(),
            )

            puz.save()
        await message.channel.send("""Puzzle **{}** started
Visit channel <#{}>
Solve using spreadsheet: {}""".format(puz.name, puz.channel_id, puz.sheet))
        return

    if command == 'finish':
        if len(parts) < 3:
            await message.channel.send(huntbot_usage)
            return

        name = ' '.join(parts[2:])
        channel = '-'.join(parts[2:]).lower()

        puz = Puzzle.get_or_none(Puzzle.name == name)

        if not puz:
            await message.channel.send("""Puzzle **{}** not found""".format(name))
            return

        finished_category = discord.utils.get(message.guild.categories, name='Finished')

        text_chan = discord.utils.get(message.guild.text_channels, name=puz.channel)
        await text_chan.edit(category=finished_category)

        voice_chan = discord.utils.get(message.guild.voice_channels, name=puz.channel)
        if voice_chan is not None:
            await voice_chan.delete()

        await message.channel.send("""Puzzle **{}** marked finished""".format(puz.name))
        return

    if command == 'list':
        items = []
        puzzles = Puzzle.select().where(Puzzle.completed_at == None)
        for puz in puzzles:
            items.append([puz.name, puz.channel, puz.sheet])

        s = "```{}```".format(tabulate(items, headers=["Name", "Channel", "Sheet"]))
        await message.channel.send(s)
        return

    await message.channel.send(huntbot_usage)
    return




client.run(os.getenv('DISCORD_TOKEN'))
