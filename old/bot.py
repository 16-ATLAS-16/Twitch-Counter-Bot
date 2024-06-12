import time, queue, configparser, requests, re
from twitchio.ext import commands
from datetime import datetime, timezone
from threading import Thread
from decapi import getUserAge
from token_manager import TokenManager
from typing import *
from logging import *
import logging
logging.basicConfig(level=logging.DEBUG)
  
class Bot(commands.Bot):
  # -- Data Tracking Variables -- #
  suspectedUsers = []
  recentAccounts = {}  # FORMAT: {channel: [lastUser1, lastUser2, lastUser3]}

  # -- Default Required Variables -- #
  THRESHOLD = 10
  TIMEOUT_SECONDS = 5 * 60

  # -- Thread Variables -- #
  THREAD = None  # Thread for updating suspicious users
  UPDATER = None  #Thread for updating token

  # -- Config Overrides -- #
  LOG_SETTINGS = None
  CHANNEL_OVERRIDES = None
  USE_UI = False

  # -- Tracking Variables -- #
  BANNING = False
  BAN_CHANNEL = None

  def __init__(self,
               token: str = None,
               channels: list[str] = [None],
               flags: Optional[list[str]] = None):
    
    # -- Basic Variable Setup, Auto Obtain a Functional Token -- #
    self.client_id = "7583ak4tqsqbnpbdoypfpg2h0ie4tu"
    self.tokenQueue = queue.Queue()
    self.tokenManager = TokenManager(out=self.tokenQueue,
                                     refreshToken=open('refreshtoken',
                                                       'r').read(),
                                     token=token)
    self.tokenManager.auto()
    self.token = self.tokenQueue.get(block=True)

    # -- Set Up Supporting Threads (Keeps from blocking console) -- #
    # -- One For Suspicious Users -- #
    if not Bot.THREAD:
      Bot.THREAD = Thread(target=Bot.tickUsers, args=[
        self,
      ])
      Bot.THREAD.start()

    # -- One For Updating The Token During Runtime -- #
    if not Bot.UPDATER:
      Bot.UPDATER = Thread(target=Bot.updateToken, args=[
        self,
      ])
      Bot.UPDATER.start()

    ## TODO - implement webhook event and thread for new followers

    # -- Parse Flags -- #
    if flags:
      with configparser.ConfigParser() as conf:
        try:
          conf.read('config.ini')
          sections = conf.sections()
        except FileNotFoundError:
          print("Config file not found. \nContinuing on default settings.")

    super().__init__(token=self.token,
                     client_id=self.client_id,
                     nick='nickhere',
                     prefix='prefix',
                     initial_channels=channels)
    print("INIT PASS")

  def trackUser(self, user, channel):
    Bot.suspectedUsers.append({
      "user": user,
      "channel": channel,
      "addTime": time.time()
    })
    if len(Bot.suspectedUsers) > Bot.THRESHOLD:
      Bot.banAllSuspects()

  def tickUsers(self):
    while True:
      time.sleep(1)
      for user in Bot.suspectedUsers:
        print(user)
        if time.time() - user["time"] > Bot.TIMEOUT_SECONDS:
          Bot.untrackUser(user)

  def updateToken(self):
    while True:
      self.token = self.tokenQueue.get(block=True)

  def untrackUser(self, user: dict):
    Bot.suspectedUsers.remove(user)

  def banAllSuspects(self):
    for user in Bot.suspectedUsers:
      # TODO: use chromedriver to mass ban users
      pass
    Bot.suspectedUsers = []

  async def event_ready(self):
    print(f'Logged in as {self.nick}')
  
  async def event_join(self, channel, user):
    newUserAge = getUserAge(user.name)
    try:
      recentUsers = Bot.recentAccounts[channel.name]
      if newUserAge == recentUsers[0] == recentUsers[1] == recentUsers[2]:
        self.trackUser(user, channel)
      Bot.recentAccounts.update(
        {channel.name: [newUserAge, recentUsers[0], recentUsers[1]]})
    except KeyError:
      Bot.recentAccounts.update({channel.name: [None, None, None]})

  async def process_git_sync(self, url: str, channel: str):
    CHANNEL = channel
    await CHANNEL.send('Processing Sync...')
    url = url.replace('github.com', 'raw.githubusercontent.com').replace('blob/', '')
    names = requests.get(url).content.decode().split('\n')
    print(f"Processed and got {len(names)} names.")
    listed_names = []

    # == Split it into smaller loads for API ==

    l=[]
    for x in names:
      l.append(x)
      if len(l) == 100:
        listed_names.append(l)
        l=[]
    listed_names.append(l)

    for N in listed_names:
      try:
        users = await self.fetch_users(N)
        print(f'Fetched {len(users)} users')
        for user in users:
          Bot.suspectedUsers.append({
            "user": user,
            "channel": channel,
            "addTime": time.time()+9000000
          })
      except Exception as e:
        if '400' in str(e): # retry recursive
          try:
            L = []
            LL = []
            for x in N:
              L.append(x)
              if len(L) == 10:
                LL.append(L)
                L = []
            LL.append(L)
            for NN in LL:
              users = await self.fetch_users(NN)
              print(f'Fetched {len(users)} users')
              for user in users:
                Bot.suspectedUsers.append({
                  "user": user,
                  "channel": channel,
                  "addTime": time.time()+9000000
                })
          except Exception as e:
            #FIX ME
            pass
        else:
          raise e
        #print(f"DEBUG: ADDED {user}")
    print("Added all users.")
    await CHANNEL.send(f"Processed all {len(names)} users.")

  async def ban_all(self, initiator, mod_id, reason, chn=None):
    USR = await chn.user()
    for suspectedUser in Bot.suspectedUsers:
      
      user = suspectedUser['user']
      try:
        
        await USR.ban_user(token=self.token, moderator_id=int(mod_id), user_id=int(user.id), reason=reason)
        Bot.suspectedUsers.remove(suspectedUser)
        print(f"banned {user}")

        
      except Exception as e:
        if '400' in str(e):
          print("User is already banned.")
          pass
          
        else:
          raise e
      
    if chn:
      await chn.send("Done.")

  async def event_message(self, message):
    if message.echo:
      pass

    else:
      try:
        made = await message.author.user()
      except twitchio.Unauthorized:
        pass
      age = datetime.now(timezone.utc) - made.created_at
      print(f"Account is {age.total_seconds()} seconds old")
      print(message.channel.name, message.content)

      if message.content.startswith("ab!sync"):
        await self.process_git_sync(message.content.split(' ')[1], message.channel)

      if message.content.startswith("ab!banall"):
        await self.ban_all(made, message.author.id, ' '.join(message.content.split(' ')[1:]), message.channel)

      matches = 0

      for x in open('banned_words', 'r').readlines():
        if x in message.content:
          matches += 1
      if matches >= 3:
        CHN = await message.channel.user()
        usr = await message.author.user()
        await CHN.ban_user(token=self.token, moderator_id=int(CHN.id), user_id=int(usr.id), reason='Doxxing.')
        #actionUser = message.author
        #for target in res:
        #  try:
        #    await made.ban_user(token=self.token, moderator_id=int(actionUser.id), user_id=int(target.id), reason='test')
        #  except Exception as e:
        #    if '400' in str(e):
        #      print("User is already banned.")
        #    else:
        #      raise e
