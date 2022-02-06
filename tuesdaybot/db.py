import sqlite3

class db (object):
    def __init__(self, filename):
        self._ctx = sqlite3.connect(filename)
        self._ctx.cursor().execute('''
            create table if not exists guild (
                guildid integer primary key,
                channel integer null
            )
        ''')
        self._ctx.commit()
    
    def set_channel(self, guildid, channelid):
        self._ctx.cursor().execute('''
            insert into guild (guildid, channel) values (?, ?)
            on conflict (guildid) do update set channel = ?
        ''', [guildid, channelid, channelid])
        self._ctx.commit()

    def get_guilds(self):
        cur = self._ctx.cursor()
        cur.execute('''
            select guildid, channel from guild
        ''')
        return cur.fetchall()
