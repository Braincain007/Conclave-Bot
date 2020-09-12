from discord import *
import math
import random
import asyncio
from discord import Game
from discord.ext.commands import Bot

import numpy
import urllib
from decimal import *
import os
import keyboard as k
import datetime
import string

import secret

BOT_PREFIX = ("c?", "c!", "C!", "C?")

TOKEN = secret.DISCORD_TOKEN

#Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)


@client.command(name='cgroup',
                descriptions='creates a private voice channel and text channel',
                brief='Creates groups')
async def cgroup(ctx):
    string.ascii_letters
    key = "".join(random.choice(str(string.ascii_lowercase)+str(string.digits)) for i in range(6))
    gm_role = await ctx.guild.create_role(name=('group-'+str(key)+'-gm'))
    
    player_role = await ctx.guild.create_role(name=('group-'+str(key)+'-player'))
    text_channel = await ctx.guild.create_text_channel(name=('group-'+str(key)+'-text_channel'))
    await text_channel.set_permissions(ctx.guild.default_role,view_channel=False)
    await text_channel.set_permissions(gm_role,
                                    view_channel=True,
                                    read_messages=True,
                                    send_messages=True)
    await text_channel.set_permissions(player_role,
                                    view_channel=True,
                                    read_messages=True,
                                    send_messages=True)
    
    voice_channel = await ctx.guild.create_voice_channel(name=('group-'+str(key)+'-voice_channel'))
    await voice_channel.set_permissions(ctx.guild.default_role,view_channel=False)
    await voice_channel.set_permissions(gm_role,
                                    view_channel=True,
                                    read_messages=True,
                                    send_messages=True)
    await voice_channel.set_permissions(player_role,
                                    view_channel=True,
                                    read_messages=True,
                                    send_messages=True)
    group = utils.get(ctx.guild.categories, name='Groups')
    
    await text_channel.edit(category=group)
    await voice_channel.edit(category=group)
    await ctx.author.add_roles(gm_role)
    await ctx.send('Group created!')
    



@client.command(name='groupadd',
                descriptions='join a private voice channel and text channel',
                brief='join groups')
async def groupadd(ctx,key, *, user):
    if utils.get(ctx.message.author.roles, name='group-'+str(key)+'-gm')==('group-'+str(key)+'-gm'):
        player_role = utils.get(ctx.guild.roles, name=('group-'+str(key)+'-player'))
        await ctx.message.mentions[0].add_roles(player_role)

        await ctx.send('Player added!')


@client.command(name='delgroup',
                descriptions='deletes a private voice channel and text channel',
                brief='deletes groups')
async def delgroup(ctx, key):
   if str(utils.get(ctx.message.author.roles, name='group-'+str(key)+'-gm'))==('group-'+str(key)+'-gm'):
         text_channel = utils.get(ctx.guild.text_channels, name=('group-'+str(key)+'-text_channel'))
         voice_channel = utils.get(ctx.guild.voice_channels, name=('group-'+str(key)+'-voice_channel'))
         gm_role = utils.get(ctx.guild.roles, name=('group-'+str(key)+'-gm'))
         player_role = utils.get(ctx.guild.roles, name=('group-'+str(key)+'-player'))
         await text_channel.delete()
         await voice_channel.delete()
         await player_role.delete()
         await gm_role.delete()

    

@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="with c!"))
    print("Logged in as " + client.user.name)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed():
        print("Current servers:")
        for guild in client.guilds:
            print(guild.name)

        await asyncio.sleep(6000)


client.loop.create_task(list_servers())
client.run(TOKEN)
