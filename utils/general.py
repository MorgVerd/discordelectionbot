
import asyncio, aiohttp, discord, async_timeout, pytz, time
import os, sys, linecache, async_timeout, inspect, traceback
import re, math, random, uuid, time
from datetime import datetime
import os.path


class General():
    def __init__(self, bot, cursor):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.tz = pytz.timezone('UTC')

    # Add stuff