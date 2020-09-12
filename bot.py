#!/bin/env python3.8

#Co-created by Ethan and Gustave

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
    group_gm_role = await ctx.guild.create_role(name=GROUP_GM_ROLE%(key))
    group_player_role = await ctx.guild.create_role(name=GROUP_PLAYER_ROLE%(key))

    group_overwrites = {
        ctx.guild.default_role: PermissionOverwrite(read_messages=False),
        group_gm_role: PermissionOverwrite(read_messages=True),
        group_player_role: PermissionOverwrite(read_messages=True)
    }

    group_text_channel = await ctx.guild.create_text_channel(
        name=GROUP_TEXT_CHANNEL%(key), 
        overwrites=group_overwrites, 
        category=group_category)
    group_voice_channel = await ctx.guild.create_voice_channel(
        name=GROUP_VOICE_CHANNEL%(key), 
        overwrites=group_overwrites, 
        category=group_category)
    
    await ctx.self.add_roles(group_gm_role)
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
    group_text_channel = utils.get(ctx.guild.text_channels, name=GROUP_TEXT_CHANNEL%(key))
    group_voice_channel = utils.get(ctx.guild.voice_channels, name=GROUP_VOICE_CHANNEL%(key))

    await group_gm_role.delete()
    await group_player_role.delete()
    await group_text_channel.delete()
    await group_voice_channel.delete()

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
