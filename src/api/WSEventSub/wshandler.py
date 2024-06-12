import aiohttp
import json, requests, twitchio, websocket, threading, asyncio
from WSEventSub import subscription, exceptions
""" ws = create_connection('ws://127.0.0.1:8080/ws?keepalive_timeout_seconds=60', 600)
initial = json.loads(ws.recv())
print(f'SESSION ID IS {str(initial["payload"]["session"]["id"])}')
resp = requests.post('http://127.0.0.1:8080/eventsub/subscriptions',
                     headers={
                         'Authorization': 'Bearer e6iwgt0q35483723ver1o8amxr8zwf',
                         'Client-Id': '7583ak4tqsqbnpbdoypfpg2h0ie4tu',
                         'Content-Type': 'application/json'},
                     json = {"type": "channel.follow",
                             "version": "2",
                             "condition": {"user_id": "495706279"},
                             "transport": {
                                "method": "websocket",
                                "session_id": str(initial['payload']['session']['id'])
                                }
                             }
                     )

print(resp.content)
while 1:
    try:
        opcode, data = ws.recv_data_frame()
        data = data.data
        print(opcode)
        print(data.decode('ascii'))
    except Exception as e:
        print(ws.connected)
 """
class WSHandler:

    SID: str = None
    WSCLIENT: aiohttp.ClientWebSocketResponse = None
    TOKEN: str = None
    SHUTDOWN: bool = False
    timeout: int = 10
    subscriptions: list = []
    currentCost: int = 0
    RUNNING = False
    startsubs = []
    reqs = []
    SESSION: aiohttp.ClientSession = None

    def __init__(self, token: str, subscriptions: list[tuple] = [], requirements: list[dict] = [], timeout: int = 10):
        self.TOKEN = token
        self.timeout = timeout
        self.startsubs = subscriptions
        self.reqs = requirements

    async def __create_session(self):
        if not self.SESSION:
            self.SESSION = aiohttp.ClientSession()

        self.WSCLIENT = await self.SESSION.ws_connect(f'wss://eventsub.wss.twitch.tv/ws?keepalive_timeout_seconds={self.timeout}', timeout=self.timeout)

        setupData = await self.WSCLIENT.receive()
        setupData = json.loads(setupData.data)
        self.SID = setupData['payload']['session']['id']

        print(self.SID)

        return self.WSCLIENT
    
    async def __on_reconnect(self, reconnectURL: str):
        self.WSCLIENT.close()
        self.WSCLIENT = await self.SESSION.ws_connect(reconnectURL, timeout=self.timeout)

    async def __main__(self):

        ws = self.WSCLIENT or await self.__create_session()
        await self.on_ready()

        for index, value in enumerate(self.startsubs):
            channel, topic = value
            await self.subscribe(channel, topic, self.reqs[index])


        self.RUNNING = True

        while True:
            if self.SHUTDOWN:
                break

            data = await ws.receive()
            print(data.type.name)
            print(data.data)

            match data.type:
                case aiohttp.WSMsgType.CLOSE:
                    match data.data:
                        case '4000':
                            print("Internal Error")
                        case '4001':
                            print('Client sent inbound traffic')
                        case '4002':
                            print('Client failed ping-pong')
                        case '4003':
                            print('Connection unused')
                        case '4004':
                            print('Reconnect grace time expired')
                        case '4005':
                            print('Network timeout')
                        case '4006':
                            print('Network error')
                        case '4007':
                            print('Invalid reconnect')

                    break

                case aiohttp.WSMsgType.TEXT:

                    data = json.loads(data.data)

                    #print(data)

                    metadata = data['metadata']
                    payload = data['payload']

                    match metadata['message_type']:
                        case 'session_keepalive':
                            await self.on_keepalive()
                        case 'notification':
                            await self.on_event(metadata, payload)
                        case 'session_reconnect':
                            await self.__on_reconnect(payload['session']['reconnect_url'])
                        case 'revocation':
                            await self.on_revoked(metadata, payload)
                        case 'session_welcome':
                            self.SID = payload['session']['id']
                            await self.on_reconnect(payload)

        await self.WSCLIENT.close()
                    

    async def subscribe(self, channel: str, topic: str, requirements: dict = {}, keepalive: int = 10) -> subscription.Subscription:

        print("Subscribing to channel: ", channel)
        sub = subscription.Subscription(self.TOKEN, channel, keepalive, topic)

        try:
            success, cost, status = sub.subscribe(self.SID, requirements)
            print("Success.")
        except exceptions.InvalidToken:
            self.TOKEN = await self.on_token_expired()
            success, cost, status = sub.subscribe(self.SID, requirements)

        if success:
            self.subscriptions.append(sub)
            self.currentCost += cost

        else:
            raise exceptions.UnexpectedResponse(f'Got subscription response {status} when expecting "enabled".')
        
        return sub
        
    async def on_keepalive(self, *args, **kwargs) -> None:
        pass

    async def on_event(self, metadata: dict = None, payload: dict = None, *args, **kwargs) -> None:
        """Callback hook ->
            Called when an event is received."""
        print(payload)

    async def on_ready(self, *args, **kwargs) -> None:
        "Called when the WebSocket Handler is ready."

    async def on_revoked(self, metadata: dict = None, payload: dict = None, *args, **kwargs) -> None:
        """
        Callback hook ->
            Called when authorization is revoked.
        """

    async def on_reconnect(self, payload, *args, **kwargs) -> None:
        """Callback hook ->
            Called when the Websocket client successfully reconnects."""

    async def on_close(self, reason: str, *args, **kwargs) -> None:
        """Callback hook ->
            Called when Twitch closes the connection.
        """

    async def on_token_expired(self) -> str:
        """Callback hook ->
            Called when the token passed is no longer valid.
            Should return a new valid token"""

    async def start(self) -> None:
        if not self.RUNNING:
            await self.__main__()