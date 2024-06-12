from WSEventSub import wshandler, classes, subscription
from requests import get
from typing import *
import twitchio

class WSEvents(wshandler.WSHandler):

    bot = None

    def __init__(self, Client, initial_channels: list[str] = [], initial_types: classes.SubscriptionType = None):
        fields = initial_types.Fields
        initCh = [(channel, initial_types.Type) for channel in initial_channels]
        self.bot = Client

        requirements = []
        print("INIT")
        for channel in initial_channels:
            print(channel)
            requirements.append({fields['target']: channel,
                                 fields['self']: Client.user_id,
                                 'version': initial_types.Version})
        print(initial_channels)
        print(requirements)
            
        super().__init__(Client.token, initCh, requirements)

    async def on_ready(self, *args, **kwargs) -> None:
        print("Websocket ready!")

    async def on_event(self, metadata: dict = None, payload: dict = None, *args, **kwargs) -> None:

        if metadata['subscription_type'] == 'channel.follow':

            channel = payload['event']['broadcaster_user_id']
            follower = payload['event']['user_name']

            a = open('banlist.txt', 'r')
            users = [line.strip('\n') for line in a.readlines()]
            a.close()
            del a

            if follower in users:
                # do instaban
                pass

            else:
                # fetch user that followed
                usr = await self.bot.fetch_user(follower)
                chn = await self.bot.fetch_channel(channel)
                await self.bot.check_user(usr, chn)

                del usr, chn

            del users, channel, follower

    async def on_reconnect(self, payload, *args, **kwargs) -> None:
        print("Reconnected successfully.")

    async def on_token_expired(self) -> str:
        return await self.bot.event_token_expired()
    
    async def on_close(self, reason: str, *args, **kwargs) -> None:
        print("Connection closed: ", reason)
        await self.start()

    async def on_revoked(self, metadata: dict = None, payload: dict = None, *args, **kwargs) -> None:
        print("Access revoked: ", payload['status'])

    async def on_keepalive(self, *args, **kwargs) -> None:
        pass
