#!/usr/bin/env python3.8

# Conclave Bot - Discord.py Bot used to create and administrate private RPG group channels+roles
# Copyright (C) 2020 Ethan Dunning and Gustave Michel III
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import string
import random
import asyncio

from discord import *
from discord import Game
from discord.ext.commands import Bot

# Local secret file
import secret

TOKEN = secret.DISCORD_TOKEN
#Get at discordapp.com/developers/applications/me

BOT_PREFIX = ("c?", "c!", "C!", "C?")
client = Bot(command_prefix=BOT_PREFIX)

GROUP_GM_ROLE = "group-%s-gm"
GROUP_PLAYER_ROLE = "group-%s-player"
GROUP_TEXT_CHANNEL = "group-%s-text"
GROUP_VOICE_CHANNEL = "group-%s-voice"
GROUP_CATEGORY = "GROUPS"
GROUP_BOT_ROLE = "group-bot"

@client.command(name="creategroup",
    descriptions="Creates a Private RPG Group with a Text+Voice Channel",
    brief="Create Group",
    aliases=["cgroup"])
async def creategroup(ctx):
    while True:
        # Recreate Key until we know it doesn't exist already
        key = str("".join(random.choice(str(string.ascii_lowercase)+str(string.digits)) for i in range(6)))
        if utils.get(ctx.guild.roles, name=GROUP_GM_ROLE%(key)) == None:
            break
    
    group_category = utils.get(ctx.guild.categories, name=GROUP_CATEGORY)
    if group_category == None:
        group_category = await ctx.guild.create_category(name=GROUP_CATEGORY)

    group_bot_role = utils.get(ctx.guild.roles, name=GROUP_BOT_ROLE)
    if group_bot_role == None:
        group_bot_role = await ctx.guild.create_role(name=GROUP_BOT_ROLE)

    group_gm_role = await ctx.guild.create_role(name=GROUP_GM_ROLE%(key))
    group_player_role = await ctx.guild.create_role(name=GROUP_PLAYER_ROLE%(key))

    group_overwrites = {
        ctx.guild.default_role: PermissionOverwrite(read_messages=False),
        group_gm_role: PermissionOverwrite(read_messages=True, mention_everyone=True),
        group_player_role: PermissionOverwrite(read_messages=True),
        group_bot_role: PermissionOverwrite(read_messages=True),
        client.user: PermissionOverwrite(read_messages=True)
    }

    group_text_channel = await ctx.guild.create_text_channel(
        name=GROUP_TEXT_CHANNEL%(key), 
        overwrites=group_overwrites, 
        category=group_category)
    group_voice_channel = await ctx.guild.create_voice_channel(
        name=GROUP_VOICE_CHANNEL%(key), 
        overwrites=group_overwrites, 
        category=group_category)
    
    await ctx.author.add_roles(group_gm_role)

    await ctx.send("%s Group Created!"%(key))


@client.command(name="deletegroup",
    descriptions="Deletes the RPG Group, and Accompanying Roles and Channels",
    brief="Delete Group",
    aliases=["delgroup"])
async def deletegroup(ctx, key: str):
    if utils.get(ctx.message.author.roles, name=GROUP_GM_ROLE%(key)) == None and ctx.message.author.guild_permissions.administrator == False:
        await ctx.send("You are not a GM for the %s Group. Only a Group's GM may Delete the Group."%(key))
        return

    group_gm_role = utils.get(ctx.guild.roles, name=GROUP_GM_ROLE%(key))
    group_player_role = utils.get(ctx.guild.roles, name=GROUP_PLAYER_ROLE%(key))
    group_text_channels = [channel for channel in ctx.guild.text_channels if key in channel.name]
    group_voice_channels = [channel for channel in ctx.guild.voice_channels if key in channel.name]

    await group_gm_role.delete()
    await group_player_role.delete()
    for channel in group_text_channels:
        await channel.delete()
    for channel in group_voice_channels:
        await channel.delete()

    await ctx.send("%s Group Deleted."%(key))


@client.command(name="addplayer",
    descriptions="Give a User the Player Role for an RPG Group",
    brief="Add Player to Group",
    aliases=["groupadd"])
async def addplayer(ctx, key: str, user: Member):
    if utils.get(ctx.message.author.roles, name=GROUP_GM_ROLE%(key)) == None and ctx.message.author.guild_permissions.administrator == False:
        await ctx.send("You are not a GM for the %s Group. Only a Group's GM may Add a Member to the Group."%(key))
        return

    group_player_role = utils.get(ctx.guild.roles, name=GROUP_PLAYER_ROLE%(key))
    await user.add_roles(group_player_role)

    await ctx.send("Player %s Added to %s Group!"%(user.name, key))


@client.command(name="removeplayer",
    descriptions="Remove the Player Role for an RPG Group from a User",
    brief="Remove Player from Group",
    aliases=["groupremove"])
async def removeplayer(ctx, key: str, user: Member):
    if utils.get(ctx.message.author.roles, name=GROUP_GM_ROLE%(key)) == None and ctx.message.author.guild_permissions.administrator == False:
        await ctx.send("You are not a GM for the %s Group. Only a Group's GM may Remove a Member from the Group."%(key))
        return

    group_player_role = utils.get(ctx.guild.roles, name=GROUP_PLAYER_ROLE%(key))
    await user.remove_roles(group_player_role)

    await ctx.send("Player %s Removed from %s Group."%(user.name, key))

@client.command(name="addtextchannel",
    descriptions="Add a Text Channel to an RPG Group",
    brief="Add Text Channel",
    aliases=["addtext"])
async def addtextchannel(ctx, key: str, name: str):
    group_text_channel = "group-%s-%s"%(key, name)

    if utils.get(ctx.message.author.roles, name=GROUP_GM_ROLE%(key)) == None and ctx.message.author.guild_permissions.administrator == False:
        await ctx.send("You are not a GM for the %s Group. Only a Group's GM may add Channels to the Group."%(key))
        return

    if utils.get(ctx.guild.text_channels, name=group_text_channel) != None:
        await ctx.send("Text Channel %s Already Exists for %s Group."%(group_text_channel, key))
        return

    group_category = utils.get(ctx.guild.categories, name=GROUP_CATEGORY)
    group_bot_role = utils.get(ctx.guild.roles, name=GROUP_BOT_ROLE)
    group_gm_role = utils.get(ctx.guild.roles, name=GROUP_GM_ROLE%(key))
    group_player_role = utils.get(ctx.guild.roles, name=GROUP_PLAYER_ROLE%(key))

    group_overwrites = {
        ctx.guild.default_role: PermissionOverwrite(read_messages=False),
        group_gm_role: PermissionOverwrite(read_messages=True, mention_everyone=True),
        group_player_role: PermissionOverwrite(read_messages=True),
        group_bot_role: PermissionOverwrite(read_messages=True),
        client.user: PermissionOverwrite(read_messages=True)
    }

    await ctx.guild.create_text_channel(
        name=group_text_channel, 
        overwrites=group_overwrites, 
        category=group_category)
    
    await ctx.send("Text Channel %s Added to %s Group."%(group_text_channel, key))

@client.command(name="removetextchannel",
    descriptions="Remove a Text Channel from an RPG Group",
    brief="Remove Text Channel",
    aliases=["deltext"])
async def removetextchannel(ctx, key: str, channel: TextChannel):
    if utils.get(ctx.message.author.roles, name=GROUP_GM_ROLE%(key)) == None and ctx.message.author.guild_permissions.administrator == False:
        await ctx.send("You are not a GM for the %s Group. Only a Group's GM may remove Channels from the Group."%(key))
        return

    await channel.delete()
    
    await ctx.send("Text Channel %s Removed from %s Group."%(channel.name, key))

@client.command(name="addvoicechannel",
    descriptions="Add a Voice Channel to an RPG Group",
    brief="Add Voice Channel to Group",
    aliases=["groupaddvoice"])
async def addvoicechannel(ctx, key: str, name: str):
    group_voice_channel = "group-%s-%s"%(key, name)

    if utils.get(ctx.message.author.roles, name=GROUP_GM_ROLE%(key)) == None and ctx.message.author.guild_permissions.administrator == False:
        await ctx.send("You are not a GM for the %s Group. Only a Group's GM may add Channels to the Group."%(key))
        return

    if utils.get(ctx.guild.voice_channels, name=group_voice_channel) != None:
        await ctx.send("Voice Channel %s Already Exists for %s Group."%(group_voice_channel, key))
        return

    group_category = utils.get(ctx.guild.categories, name=GROUP_CATEGORY)
    group_bot_role = utils.get(ctx.guild.roles, name=GROUP_BOT_ROLE)
    group_gm_role = utils.get(ctx.guild.roles, name=GROUP_GM_ROLE%(key))
    group_player_role = utils.get(ctx.guild.roles, name=GROUP_PLAYER_ROLE%(key))

    group_overwrites = {
        ctx.guild.default_role: PermissionOverwrite(read_messages=False),
        group_gm_role: PermissionOverwrite(read_messages=True, mention_everyone=True),
        group_player_role: PermissionOverwrite(read_messages=True),
        group_bot_role: PermissionOverwrite(read_messages=True),
        client.user: PermissionOverwrite(read_messages=True)
    }

    group_voice_channel = await ctx.guild.create_voice_channel(
        name=group_voice_channel, 
        overwrites=group_overwrites, 
        category=group_category)
    
    await ctx.send("Voice Channel %s Added to %s Group."%(group_voice_channel, key))

@client.command(name="removevoicechannel",
    descriptions="Remove a Voice Channel from an RPG Group",
    brief="Remove Voice Channel",
    aliases=["delvoice"])
async def removevoicechannel(ctx, key: str, channel: VoiceChannel):
    if utils.get(ctx.message.author.roles, name=GROUP_GM_ROLE%(key)) == None and ctx.message.author.guild_permissions.administrator == False:
        await ctx.send("You are not a GM for the %s Group. Only a Group's GM may remove Channels from the Group."%(key))
        return

    await channel.delete()
    
    await ctx.send("Voice Channel %s Removed from %s Group."%(channel.name, key))

@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="with c!"))
    print("Logged in as %s"%client.user.name)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed():
        print("Current servers:")
        for guild in client.guilds:
            print(guild.name)

        await asyncio.sleep(6000)


client.loop.create_task(list_servers())
client.run(TOKEN)
