import twitchio, requests, json
from . import exceptions

class Subscription:
    channel: twitchio.channel = None
    channelID: str = None
    keepalive: int = 10
    active: bool = True
    type: str = 'channel.follow'
    id: str = ''
    token: str = ''

    def __init__(self, token: str, channelID: str = None, keepaliveTimeout: int  = 0, type: str = 'channel.follow') -> None:
        assert channelID is not None, "A User must be provided."
        
        self.channel = channelID
        self.channelID = channelID
        self.keepalive = keepaliveTimeout
        self.type = type
        self.token = token
        
    def subscribe(self, sid: str, requirements: dict) -> tuple[bool, int, str]:

        cond = {"broadcaster_user_id": str(self.channelID)}
        for arg in requirements:
            if arg != 'version':
                cond.update({arg: str(requirements[arg])})

        print("POSTING! >>> ", self.token, self.type, requirements['version'], cond, sid)
        resp = requests.post('https://api.twitch.tv/helix/eventsub/subscriptions',
                     headers={
                         'Authorization': f'Bearer {self.token}',
                         'Client-Id': '7583ak4tqsqbnpbdoypfpg2h0ie4tu',
                         'Content-Type': 'application/json'},
                     json = {"type": self.type,
                             "version": requirements['version'] if 'version' in requirements else "1",
                             "condition": cond,
                             "transport": {
                                "method": "websocket",
                                "session_id": sid
                                }
                             }
                     )
        
        if resp.status_code == 401:
            raise exceptions.InvalidToken("Invalid token passed.")
        
        print(resp.content.decode())
        
        respJSON = json.loads(resp.content.decode())
        data = respJSON['data'][0]
        self.id = data['id']
        self.active = data['status']

        cost = respJSON['total']

        print(respJSON)

        if self.active not in ['enabled', 'disabled']:
            raise exceptions.UnexpectedResponse(f'Received a subscription status of {self.active} while expecting "enabled".')
        
        else:
            return (self.active == 'enabled', cost, self.active)
