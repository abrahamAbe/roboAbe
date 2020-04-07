# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('discordToken')
discordGuild = os.getenv('discordGuild')
bot = commands.Bot(command_prefix='!')
#client = discord.Client()


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=discordGuild)
    print(
        f'{bot.user} is connected:'
    )
    if guild:
        print(f'Guild:')
        print(f'{guild.name}(id: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')


@bot.event
async def on_member_join(member):
    print(f'Joined!', member)
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, Do you like fish sticks?'
    )


@bot.command(name='99', help='Hold The Door')
async def nine_nine(ctx):
    gotQuotes = [
        'Winter is coming',
        'The Lannisters send their regards'
    ]

    response = random.choice(gotQuotes)
    await ctx.send(response)


@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

'''
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    quote = 'Hasta la vista, baby.'

    if message.content.lower() == 'terminator':
        await message.channel.send(quote)

    #elif message.content == 'raise-exception':
    #    raise discord.DiscordException
'''


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command... puny human.')

bot.run(token)