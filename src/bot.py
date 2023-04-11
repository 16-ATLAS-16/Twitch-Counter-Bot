from twitchio.ext import commands
import time
from threading import Thread


class Bot(commands.Bot):
  suspectedUsers = []
  THRESHOLD = 10
  TIMEOUT_SECONDS = 5 * 60
  THREAD = None

  def __init__(self, token: str, channels: list[str]):
    self.client_id = ""
    self.token = token

    if not Bot.THREAD:
      Bot.THREAD = Thread(target=Bot.tickUsers)
      Bot.THREAD.start()

    Bot.join_channels(channels)

  def trackUser(self, username: str, channel):
    Bot.suspectedUsers.append({
      "username": username,
      "channel": channel,
      "addTime": time.time()
    })
    if len(Bot.suspectedUsers) > Bot.THRESHOLD:
      Bot.banAllSuspects()

  def tickUsers(self):
    while True:
      time.sleep(1)
      for user in Bot.suspectedUsers:
        if time.time() - user["time"] > Bot.TIMEOUT_SECONDS:
          Bot.untrackUser(user)

  def untrackUser(self, user: dict):
    Bot.suspectedUsers.remove(user)

  def banAllSuspects(self):
    for user in Bot.suspectedUsers:
      # TODO: use chromedriver to mass ban users
      pass
    Bot.suspectedUsers = []
