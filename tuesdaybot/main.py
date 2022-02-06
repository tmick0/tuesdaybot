import argparse
import configparser
import logging

from .db import db
from .bot import bot
from .status import status as statusclient

def main():
    logging.basicConfig(level=logging.INFO)

    config = configparser.ConfigParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', default='config.ini')

    args = parser.parse_args()
    config.read(args.config)
    config = config['tuesday']

    database = db(config['database'])
    status = statusclient(config['valveapikey'], int(config['interval']), config['regions'].split(','), config['services'].split(','))
    client = bot(config['discordtoken'], config['prefix'], database, status)

    client.run()
