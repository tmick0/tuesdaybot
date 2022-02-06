import requests
import asyncio
import logging


class status (object):

    ENDPOINT="https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key={:s}"

    def __init__(self, apikey, interval, regions, services):
        self._key = apikey
        self._interval = interval
        self._regions = regions
        self._services = services
        self._cache = None
        self._bad = False
        self._message = "I haven't retrieved the status yet"
        self._callbacks = []
        asyncio.ensure_future(self.update())
    
    async def update(self):
        logging.info("updating status...")
        r = requests.get(self.ENDPOINT.format(self._key))
        if r.status_code == 200:
            logging.info("successfully updated")
            self._cache = r.json()
            self._process_update()
            for c in self._callbacks:
                await c(self.status(), self.summary())
        else:
            logging.warning("failed to update, code {:d}".format(r.status_code))
        await asyncio.sleep(self._interval)
        asyncio.ensure_future(self.update())

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def data(self):
        return self._cache

    def status(self):
        return self._bad

    def summary(self):
        return self._message

    def _process_update(self):
        bad_svcs = {}
        bad_regions = {}

        for svc in self._services:
            if self._cache['result']['services'][svc] != "normal":
                bad_svcs[svc] = self._cache['result']['services'][svc]

        for reg in self._regions:
            dc = self._cache['result']['datacenters'][reg]
            if dc['capacity'] not in ('full', 'high'):
                bad_regions[reg] = 'degraded'
            elif dc['load'] == 'high':
                bad_regions[reg] = 'high load'
        
        if len(bad_svcs) > 0 or len(bad_regions) > 0:
            msg = ""
            self._bad = True
            if len(bad_svcs):
                msg += "The following services are degraded: " + ", ".join("{} ({})".format(k, v) for k, v in bad_svcs.items()) + ".\n"
            if len(bad_regions):
                msg += "The following server regions are degraded: " + ", ".join("{} ({})".format(k, v) for k, v in bad_regions.items()) + ".\n"
            self._message = msg
        else:
            self._bad = False
            self._message = "Everything looks okay"