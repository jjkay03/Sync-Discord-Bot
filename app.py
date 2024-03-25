# Sync Bot by jjkay03

import discord
from discord.ext import commands

intents = discord.Intents.default(); intents.message_content=True; intents.members=True
client = commands.Bot(command_prefix = "s.", intents=intents)
TOKEN = open("TOKEN.txt", "r").read()
version = "1.0.4"

# The sync server will copy the roles from the main server
main_server_id = 302087475385539007 # The ID of the main server
sync_server_id = 302087475385539007 # The ID of the sync server

# This is the role map, ID of a role on the main server and its equivalent on the sync server
# Main server role ID : Sync server role ID
role_id_map = {
    302087475385539007 : 302087475385539007, # Role 1
    302087475385539007 : 302087475385539007, # Role 2
    302087475385539007 : 302087475385539007 # Role 3
}

# -- EVENTS ---------------------------------------------------------------------

# On ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print(">> BOT IS RUNNING")
    print(">> Name: {}".format(client.user.name))
    print(">> ID: {}".format(client.user.id))
    print(f">> Version: {version}")

# Member update
@client.event
async def on_member_update(before, after):
    if before.roles != after.roles and before.guild.id == main_server_id:
        print(f"[>] Synchronized roles for {before.name} as they updated in the Main Server.")
        await sync_roles(before.guild, client.get_guild(sync_server_id), before.id)

# On member join
@client.event
async def on_member_join(member):
    if member.guild.id == sync_server_id:
        print(f"[>] Synchronized roles for {member.name} as they joined the Sync Server.")
        await sync_roles(client.get_guild(main_server_id), member.guild, member.id)


# -- FUNCTIONS ------------------------------------------------------------------

async def sync_roles(main_server, sync_server, user_id):
    main_member = main_server.get_member(user_id)
    sync_member = sync_server.get_member(user_id)

    if main_member is None:
        print(f"[D] User with ID {user_id} not found in Main Server.")
    if sync_member is None:
        print(f"[D] User with ID {user_id} not found in Sync Server."); return

    sync_roles_to_remove = [role for role in sync_member.roles if role.id in role_id_map.values()]

    # Remove sync roles from the user on the sync server
    if sync_roles_to_remove:
        await sync_member.remove_roles(*sync_roles_to_remove, reason="Removing sync roles.")
        print(f"[-] Cleared sync roles the role for {sync_member.name} in the Sync Server.")

    # Return after role clear if not on main server
    if main_member is None:
        return
    
    main_user_roles = [role.id for role in main_member.roles]
    sync_user_roles = [role.id for role in sync_member.roles]

    # Add roles on the sync server that the user has on the main server
    for role_id in main_user_roles:
        sync_role_id = role_id_map.get(role_id)
        if sync_role_id:
            sync_role = sync_server.get_role(sync_role_id)
            if sync_role:
                await sync_member.add_roles(sync_role, reason="Syncing roles from the main server.")
                print(f"[+] Gave {sync_member.name} the role {sync_role.name} in the Sync Server.")


# -- COMMANDS -------------------------------------------------------------------

# COMMAND: ping
@client.command(aliases=["Ping","PING", "p", "P"], help="Shows you the ping of the Bot")
async def ping(ctx):
    ping = round(client.latency * 1000)
    await ctx.send(f"**{ping}ms**")

# COMMAND: sync
@client.command()
async def sync(ctx, user_id: int = None):
    if ctx.author.guild_permissions.manage_roles:
        main_server = client.get_guild(main_server_id)
        sync_server = client.get_guild(sync_server_id)
        if main_server is None or sync_server is None:
            await ctx.send("One or both of the servers could not be found.")
            return

        await sync_roles(main_server, sync_server, user_id)
        await ctx.send(":ballot_box_with_check: Roles have been synced successfully!")

    else:
        await ctx.message.delete()
        await ctx.send(":x: You do not have the required permissions to use this command.", delete_after=5)

# COMMAND: syncall
@client.command()
async def syncall(ctx):
    if ctx.author.guild_permissions.manage_roles:
        main_server = client.get_guild(main_server_id)
        sync_server = client.get_guild(sync_server_id)
        if sync_server is None:
            await ctx.send("Sync server not found.")
            return

        for member in sync_server.members:
            await sync_roles(main_server, sync_server, member.id)
            print(f"[!] Synchronized roles for {member.name} in the Sync Server.")

        await ctx.send(":ballot_box_with_check: Roles have been synced for all members on the sync server!")

    else:
        await ctx.message.delete()
        await ctx.send(":x: You do not have the required permissions to use this command.", delete_after=5)

# COMMAND: removeall
@client.command()
async def removeall(ctx):
    if ctx.author.guild_permissions.manage_roles:
        sync_server = client.get_guild(sync_server_id)

        if sync_server is None:
            await ctx.send("Sync server not found.")
            return

        # Iterate through all members on the sync server
        for member in sync_server.members:
            sync_roles = [role for role in member.roles if role.id in role_id_map.values()]
            if sync_roles:
                await member.remove_roles(*sync_roles, reason="Removing all sync roles.")
                print(f"[-] Removed sync roles from {member.name} in the Sync Server.")

        await ctx.send(":ballot_box_with_check: Removed all sync roles from everyone on the sync server!")

    else:
        await ctx.message.delete()
        await ctx.send(":x: You do not have the required permissions to use this command.", delete_after=5)


# -- CLIENT RUN -----------------------------------------------------------------

# Client Run
client.run(TOKEN)
