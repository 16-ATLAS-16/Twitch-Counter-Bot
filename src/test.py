import websockets, aiohttp
import json, requests, asyncio

async def test():
    init = True
    session = aiohttp.ClientSession()
    async with session.ws_connect('ws://127.0.0.1:8080/ws?keepalive_timeout_seconds=60', timeout=10, autoclose=False) as ws:
        while 1:
            data = await ws.receive()
            print(data.data)
            try:
                initial = json.loads(data.data)
            except:
                print(data.data)
            if init:
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
                init = False
            else:
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
                                print("Keepalive")
                            case 'notification':
                                print("EVENT! ", metadata, payload)
                            case 'session_reconnect':
                                print("Reconnect!")
                                await ws.close()
                                ws = await session.ws_connect(payload['session']['reconnect_url'])
                            case 'revocation':
                                print("Revoke!", metadata, payload)
                            case 'session_welcome':
                                print("SID IS", payload['session']['id'])

    await session.close()

asyncio.run(test())