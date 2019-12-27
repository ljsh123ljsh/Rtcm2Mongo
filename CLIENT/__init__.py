import asyncio
from random import random, choice
import time
from base64 import b64encode
from DB import RABBITMQ
from configparser import ConfigParser
from binascii import b2a_hex

from os.path import abspath, join, dirname