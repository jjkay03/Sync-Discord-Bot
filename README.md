# <img alt="Static Badge" src="https://slackmojis.com/emojis/61723-usagyuuun-loading/download" width="35"> Sync-Discord-bot
A Discord bot that sync multiple roles across two servers

- To use the bot you just have to add it to both server, make sure it has perms to give roles.
- The default prefix of the bot is `s.` you can use `s.help` for a list of commands.
- To set what roles get sync you need to edit the main server ID, sync server ID and role ID map in `app.py`.

## Comands:
- `ping` - Get the ping of the bot.
- `sync <@user or User ID>` - Sync roles for a specific user.
- `syncall` - Sync roles from main server for everyone in the sync server.
- `removeall` - Remove all sync roles from everyone in the sync server.

## Cofiguration:
To configure the bot you just have to change the values at the top of `app,py`.
```py
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
```
