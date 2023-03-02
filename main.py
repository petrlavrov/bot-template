import logging

from aiogram import Bot, Dispatcher
from fastapi import FastAPI

# compile translations
import subprocess
subprocess.call(['pybabel', 'compile', '-d', 'locales', '-D', 'messages'])

import api
import bot as botsource
import middlewares
import config as cnf
import setup

class App:
  def __init__(self):
    

    self.dp = Dispatcher()
    self.dp.include_router(botsource.router)

    self.logger = logging.getLogger(__name__)

    middlewares.db.setup(self.dp)
    middlewares.referer.setup(self.dp)
    middlewares.session.setup(self.dp)
    middlewares.i18n.setup(self.dp)

    # This function is called when bots are started (setup.start_bot)
    # Bots won't start until this function's execution is over
    self.dp.startup.register(setup.main_startup)

    self.dp.shutdown.register(setup.main_shutdown)

    self.app = FastAPI()
    self.app.include_router(self.api.router)

    # Initialize Bot instance with an default parse mode which will be passed to all API calls
    self.bot = Bot(cnf.TOKEN, parse_mode="HTML")
    setup.register_main_bot(self.dp, self.app, self.bot)
    
app = App()
