# Conclave-Bot
A Discord.py Bot created for the Louisiana Tech Chapter of the Conclave of Science Fiction and Fantasy

## Purpose
Manage the Creation and Administration of Private RPG Groups within the Conclave Discord. 
These Groups will consist of a Game Master (GM) and Player role which will be used to grant access to Text and Voice Channels created specifically for the group. 
The GM of a given group (as well as Server Admins) can then add the Player role to other Members of the Server.

## Goals
Allow RPG Groups within Conclave to have a private space to run their RPG Sessions without dealing with potential trolls/outside intrustion from the rest of the Server.

## Development Setup

### Prerequisite
* Python3.8
* pip
* virtualenv (optional)
* Discord Application with Bot

### Install Dependancies
Install the Library Dependancies from the `requirements.txt` file in the Repo. Preferably inside a Python Virtual Environemnt.
```
pip install -r requirements.txt
```

### Environment
Create a `secret.py` file in the root of the Repo, and place the Discord Bot Token in a `DISCORD_TOKEN` variable.
```
DISCORD_TOKEN=abCdef.3456.IJklM
```
