# Sync-Discord-bot
A Discord bot that sync multiple roles across two servers

- To use the bot you just have to add it to both server, make sure it has perms to give roles.
- The default prefix of the bot is `s.` you can use `s.help` for a list of commands.
- To set what roles get sync you need to edit the main server ID, sync server ID and role ID map in `app.py`.

## Comands:
- `ping` - Get the ping of the bot.
- `sync <@user or User ID>` - Sync roles for a specific user.
- `syncall` - Sync roles from main server for everyone in the sync server.
- `removeall` - Remove all sync roles from everyone in the sync server.
