import time, queue, configparser, requests, re, twitchio, json, wsclient
from twitchio.ext import commands, eventsub
from datetime import datetime, timezone
from threading import Thread
from decapi import getUserAge
from token_manager import TokenManager
from typing import *
from logging import *
from api.WSEventSub import classes as WSSubClasses
import logging, asyncio
logging.basicConfig(level=logging.INFO)
  
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

  SEEN_USER: list = []

  PREFIX: str = 'ab!'
  token: str = ''

  initch = []
  ESClient = None

  subcounter: int = 0

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
    
    self.initch = channels
    self.token = self.tokenManager.auto()

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
        if time.time() - user["addTime"] > Bot.TIMEOUT_SECONDS:
          print("UNTRACKED ", user)
          Bot.untrackUser(user)

  def updateToken(self):
    while True:
      self.token = self.tokenQueue.get(block=True)

  def untrackUser(self, user: dict):
    Bot.suspectedUsers.remove(user)
  
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
        
        await USR.ban_user(token=self.token, moderator_id=int(mod_id or str(self.user_id)), user_id=int(user.id), reason=reason)
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

  async def check_user(self, user, channel):
    if user.name not in [u.name for u in Bot.SEEN_USER]:
        newUserAge = getUserAge(user.name)

        try:
          print("CHANN ", channel, channel.name)
          print("CHECK! ", channel.name, user)
          recentUsers = Bot.recentAccounts[channel.name]

          if newUserAge == recentUsers[0] == recentUsers[1] == recentUsers[2]:
            self.trackUser(user, channel)

          Bot.recentAccounts.update(
            {channel.name: [newUserAge, recentUsers[0], recentUsers[1]]})
          
        except KeyError:
          Bot.recentAccounts.update({channel.name: [None, None, None]})
          
        Bot.SEEN_USER.append(user)

  async def event_ready(self):
    #await self.sub_all()
    self.initch = [ch.id for ch in await self.fetch_users(self.initch)]
    self.ESClient = wsclient.WSEvents(self, self.initch, [WSSubClasses.Follow]) #, WSSubClasses.Subscribe, WSSubClasses.Resubscribe])
    await self.ESClient.start()
    pass

  async def sub_all(self):
    for channel in self.connected_channels:
      print("subscribing!")
      await self.ESClient.subscribe_channel_follows_v2(channel.name, self.user_id, self.token)

  async def event_eventsub_notification_followV2(self, payload: eventsub.ChannelFollowData):
    print(payload.user.name, "follwed", payload.broadcaster, "!")
    user = await payload.user.fetch()
    channel = payload.broadcaster.channel
    await self.check_user(user, channel)

  async def event_eventsub_keepalive(self, event):
    print("KEEPALIVE!")

  async def event_message(self, message):
    
    if message.echo:
      pass

    else:

      try:
        author = await message.author.user()
        chusr = await message.channel.user()

      except twitchio.Unauthorized:
        pass

      age = datetime.now(timezone.utc) - author.created_at

      print(f"Account is {age.total_seconds()} seconds old.\nUID IS {author.id}")
      print("Channel ID is ", chusr.id)
      print(message.channel.name, message.content)

      user = message.author
      channel = message.channel

      await self.check_user(user, channel)

      f = open('commands.json', 'r')
      cmds = json.loads(f.read())
      f.close()

      if message.content.split(' ')[0].replace(self.PREFIX, '') in cmds:
        exec(f'async def {message.content.split(' ')[0].replace(self.PREFIX, '')}(): {cmds[message.content.split(' ')[0].replace(self.PREFIX, '')]}', locals(), locals())
        await locals()[message.content.split(' ')[0].replace(self.PREFIX, '')]()

      matches = 0

      for x in open('banned_words', 'r').readlines():

        if x in message.content:
          matches += 1

      if matches >= 3:

        CHN = await message.channel.user()
        usr = await message.author.user()

        await usr.ban_user(token=self.token, moderator_id=int(str(self.user_id)), user_id=int(user.id), reason='Spoke what shan\'t be spoken')

  async def event_token_expired(self):
    print("Token expired!")
    
    try:
      self.tokenManager.verifyToken(self.token)
      
    except TokenManager.Exceptions.InvalidToken:
      self.token = self.tokenManager.auto()
      
    return self.token
