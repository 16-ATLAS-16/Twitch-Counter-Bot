from requests import get, post
import webhooks, json, datetime, queue, webbrowser, time
from threading import Thread


class TokenManager(object):
  """A Token Manager for Twitch Tokens"""

  refreshToken = None
  token = None
  expires = None
  status = 'Waiting'

  def __init__(self,
               out: queue.Queue,
               refreshToken: str = None,
               token: str = None,
               expires: datetime.datetime = None,
               *args,
               **kwargs):
    self.outQueue = out
    self.refreshToken = refreshToken
    self.expires = expires
    self.token = token
    self.status = 'Waiting'
    TICK = Thread(target=self.tickToken)
    TICK.start()

  class Exceptions:

    class InvalidToken(Exception):
      """Raised when the client token passed is not valid"""
      pass

    class InvalidRefresh(Exception):
      """Raised when the refresh token passed is not valid"""
      pass

    class Fatal(Exception):
      """Raised when a token cannot be obtained through conventional means
      This usually occurs if the redirect URI is changed or the webhook fails.
      Please contact developers if this naturally occurs."""

  def tickToken(self):
    while True:
      if self.expires is not None and datetime.datetime.now() > self.expires:
        self.status = f'Token needs refresh!'
      time.sleep(1)
      print(self.status, end='\r', flush=True)
      self.status = f'Waiting for {self.expires}, it is {datetime.datetime.now()}'

  def verifyToken(self, token: str) -> dict:

    Authorization = get('https://id.twitch.tv/oauth2/validate',
                        headers={
                          'client_id': '7583ak4tqsqbnpbdoypfpg2h0ie4tu',
                          'Authorization': f'Bearer {token}'
                        })
    Authorization = eval(Authorization.content.decode())
    print(f'Checking token {token}')

    if not 'client_id' in Authorization:
      print('\ntoken invalid\n')
      raise self.Exceptions.InvalidToken(
        f"Token | {token} | is no longer valid. Please use TokenManager.refresh or TokenManager.fetch"
      )
    else:
      print('\ntoken valid!\n')
      self.expires = datetime.datetime.now() + datetime.timedelta(
        seconds=Authorization['expires_in'])
      return token

  def fetch(self,
            clientId: str = '7583ak4tqsqbnpbdoypfpg2h0ie4tu',
            clientSecret: str = 'o1t8r5rjlgx35hc16jjqhqgrvnddu3',
            redirectUri: str = 'http://localhost:5000/webhook') -> str:
    tokenHook = webhooks.WebHook.AuthHook()
    print("Hook Run")
    webbrowser.open('https://id.twitch.tv/oauth2/authorize?client_id=7583ak4tqsqbnpbdoypfpg2h0ie4tu&redirect_uri=http://localhost:5000/webhook&response_type=token&scope=openid+channel:read:editors+moderator:manage:automod+moderator:manage:banned_users+moderator:read:followers+channel:read:hype_train+channel:read:polls+channel:manage:polls+channel:read:predictions+channel:read:redemptions+channel:read:subscriptions+moderation:read+user:edit+user:read:broadcast+user:read:email+user:read:follows+user:read:subscriptions+channel:moderate+chat:edit+chat:read+whispers:read+whispers:edit+channel:manage:polls', new=0, autoraise=True)
    token = tokenHook.run()

    try:
      print("Parse")
      parsedCode = json.loads(token[0].replace('\'', '"'))['code']
      returnedData = post(
        'https://id.twitch.tv/oauth2/token',
        data={
          'client_id': clientId,  
          'client_secret': clientSecret,  
          'code': parsedCode,
          'grant_type': 'authorization_code',
          'redirect_uri': redirectUri  #'http://localhost:5000/webhook'
        })
      print("Extract")
      extractedData = eval(returnedData.content.decode())
      parsedToken = extractedData['access_token']
      self.refreshToken = extractedData['refresh_token']
      print("Post Extract")
      if len(parsedToken) == 30:
        open('refreshtoken', 'w').write(self.refreshToken)
        self.verifyToken(parsedToken)
        return parsedToken
      else:
        print("nope")
    except Exception as e:
      raise e
      print(str(e))
      print(f"Failed to fetch token string, got {token}")

  def refresh(self,
              clientId: str = '7583ak4tqsqbnpbdoypfpg2h0ie4tu',
              clientSecret: str = 'o1t8r5rjlgx35hc16jjqhqgrvnddu3') -> str:
    responseData = post('https://id.twitch.tv/oauth2/token',
                        data={
                          'grant_type': 'refresh_token',
                          'refresh_token': self.refreshToken,
                          'client_id': clientId,
                          'client_secret': clientSecret
                        })
    extractedData = eval(responseData.content.decode())
    print(extractedData)
    if 'access_token' in extractedData:
      self.refreshToken = extractedData['refresh_token']
      self.verifyToken(extractedData['access_token'])
      return extractedData['access_token']
    else:
      print("Raised")
      raise self.Exceptions.InvalidRefresh("Invalid refresh token passed.")

  def auto(self):
    print("Attempting token return")
    if self.token:
      try:
        print('1')
        return self.verifyToken(self.token)
        print("Valid token passed.")
      except self.Exceptions.InvalidToken:
        try:
          print('2')
          return self.refresh()
          print("Refreshed token.")
        except self.Exceptions.InvalidRefresh:
          try:
            print('3')
            return self.fetch()
            print("Fetched token.")
          except:
            print('4')
            raise self.Exceptions.Fatal(
              "Fatal Exception: Token cannot be obtained.")
    else:
      try:
        print('5')
        return self.refresh()
        print("Refreshed token.")
      except self.Exceptions.InvalidRefresh:
        try:
          print('6')
          return self.fetch()
          print("Fetched token.")
        except:
          print('7')
          raise self.Exceptions.Fatal(
            "Fatal Exception: Token cannot be obtained.")
