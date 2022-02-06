import discord
import logging

class bot (discord.Client):
    def __init__(self, token, prefix, db, status, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token = token
        self._prefix = prefix
        self._db = db
        self._status = status
        status.add_callback(self.on_status_update)

    async def on_ready(self):
        logging.info('connected to discord')
    
    async def on_status_update(self, status, message):
        if status:
            for guild, channel in self._db.get_guilds():
                self.get_channel(channel).send(message)

    async def on_message(self, msg):
        if msg.content == self._prefix + "tuesday":
            await msg.channel.send(self._status.summary())
        elif msg.content == self._prefix + "setchannel" and msg.author.guild_permissions.administrator:
            self._db.set_channel(msg.guild.id, msg.channel.id)

    def run(self):
        super().run(self._token)
