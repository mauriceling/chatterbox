"""!
ChatterBox - Generic Scipt for ChatterBot Corpus Development and Testing

Date created: 9th October 2022

License: GNU General Public License version 3 for academic or 
not-for-profit use only

SiPy package is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import datetime
import os
import shutil

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import fire

def environment_build(environment):
    os.system("conda create --name %s --file conda_chatterbox_environment.txt" % environment)
    try:
        os.system("activate %s" % environment)
    except:
        os.system("source activate %s" % environment)
    pip_packages = open("pip_chatterbox_environment.txt").readlines()
    pip_packages = [x[:-1] for x in pip_packages]
    for package in pip_packages:
        trusted_hosts = "--trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org"
        os.system("pip install %s %s" % (trusted_hosts, package))

def environment_freeze():
    os.system("conda list --explicit > conda_chatterbox_environment.txt")
    os.system("pip list --format=freeze > pip_chatterbox_environment.txt")

def chat(database=None):
    if not database:
        now = datetime.datetime.now()
        database = now.strftime("%Y-%m-%d-%H-%M-%S") + ".db"
    else:
        now = datetime.datetime.now()
        new_database = database + "_" + now.strftime("%Y-%m-%d-%H-%M-%S") + ".db"
        shutil.copyfile("./" + database, "./" + new_database)
        database = new_database
    bot = ChatBot(
        'ChatBot',
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        logic_adapters=["chatterbot.logic.BestMatch"],
        database_uri="sqlite:///" + database 
        )
    while True:
        user_input = input("Talk to ChatBot > ")
        if user_input.lower().strip() == ".exit":
            return None
        else:
            bot_response = bot.get_response(user_input)
            print("ChatBot: " + str(bot_response))

def train(corpus, database=None):
    if not database:
        now = datetime.datetime.now()
        database = now.strftime("%Y-%m-%d-%H-%M-%S") + ".db"
    bot = ChatBot(
        'ChatBot',
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        logic_adapters=["chatterbot.logic.BestMatch"],
        database_uri='sqlite:///' + database
    )
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("./" + str(corpus))

if __name__ == "__main__":
    exposed_functions = {
        "env_build": environment_build,
        "env_freeze": environment_freeze,
        "chat": chat,
        "train": train
        }
    fire.Fire(exposed_functions)
