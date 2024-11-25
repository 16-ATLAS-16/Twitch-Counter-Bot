from api.WSEventSub import wshandler, classes, subscription
from requests import get
from typing import *
import twitchio

class WSEvents(wshandler.WSHandler):

    bot = None

    def __init__(self, Client, initial_channels: list[str] = [], initial_types: list[classes.SubscriptionType] = None):
        print("I GOT GIVEN ", Client.user_id)
        initCh = []
        for channel in initial_channels:
            for subType in initial_types:
                initCh.append((channel, subType.Type))
        self.bot = Client

        requirements = []
        print("INIT SUBS")
        for channel in initial_channels:
            print(channel)
            for subType in initial_types:
                fields = subType.Fields
                requirements.append({fields['target']: channel,
                                     fields['self']: Client.user_id,
                                     'version': subType.Version})
        print(initial_channels)
        print(requirements)
            
        super().__init__(Client.token, initCh, requirements)

    async def on_ready(self, *args, **kwargs) -> None:
        print("Websocket ready!")

    async def on_event(self, metadata: dict = None, payload: dict = None, *args, **kwargs) -> None:

        match metadata['subscription_type']:
            
            case 'channel.follow':

                channel = payload['event']['broadcaster_user_login']
                follower = payload['event']['user_name']
                print("PAYLOAD", payload)
                print("FOLLOWED!\n", follower, channel)

                a = open('banlist.txt', 'r')
                users = [line.strip('\n') for line in a.readlines()]
                a.close()
                del a

                if follower in users:
                    # do instaban
                    pass

                else:
                    # fetch user that followed
                    print(channel, follower)
                    usr, chn = await self.bot.fetch_users([follower, channel])
                    #chn = await self.bot.fetch_channels([channel])
                    print("USER IS ", usr)
                    print("CHANNEL IS ", chn)
                    await self.bot.check_user(usr, chn)

                    del usr, chn

                del users, channel, follower

            case 'channel.subscribe':

                self.bot.subcounter += 1

            case 'channel.subscription.message':

                self.bot.subcounter += 1

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
