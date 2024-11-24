import urllib, threading, sys, queue, random, string, logging, time
from flask import Flask, request, render_template, redirect, current_app, Response
from werkzeug.serving import make_server


class WebHook:

  class AuthHook:
    QUEUE = None
    KEY = None
    app = Flask(__name__)
    waiting: list = []

    def __init__(self,
                 outQueue: queue.Queue = None,
                 overrideHost: str = 'localhost',
                 overridePort: int = 5000):
      """Initialise an authHook object.
			Call authHook.run to run.
			
			Args: 
				outQueue: queue.Queue -> Multiprocessing Queue to return result to.
				overrideHost: str -> Overrides application default host (localhost)
				overridePort: int -> Overrides application default port (5000)
			"""
      self.QUEUE = outQueue or queue.Queue(maxsize=1)

      self.HOST, self.PORT = overrideHost, overridePort

    class ServerThread(threading.Thread):

      def __init__(self, app, parent):
        threading.Thread.__init__(self)
        app.PARENT = parent
        self.server = make_server(parent.HOST, parent.PORT, app)
        self.ctx = app.app_context()
        self.ctx.push()
        self.parent: WebHook.AuthHook = parent

      def run(self):
        self.server.serve_forever()

      def shutdown(self):
        self.server.shutdown()

    def outputData(self, data=None, affResp: any = None, negResp: any = None):
      """Puts data into the output queue.
			
			Args:
				data: any -> Data to output
				affResp: str -> Response to return if data has successfully been stored
				negResp: str -> Response to return if data has not been stored"""

      if self.QUEUE and data:
        self.QUEUE.put(data)
        return affResp
      else:
        return negResp
      
    @app.before_request
    def before_request_func():
      print(request.base_url)
      current_app.PARENT.waiting.append(request)
      print(f'Waiting now on {len(current_app.PARENT.waiting)} requests')

    @app.after_request
    def after_request_func(response):
      current_app.PARENT.waiting.remove(request)
      print(f'Waiting now on {len(current_app.PARENT.waiting)} requests')
      return response

    @app.route('/', methods=["GET"])
    def home():
      """Homepage.
			Redirects to /webhook if query data is present"""

      return redirect(f"/webhook?{urllib.parse.urlencode(request.args)}")
    
#    @app.route('/<path:path>')
#    def catch_all(path):

    @app.route('/webhook', methods=["GET"])
    def webhook():
      """Main webhook path.
			Used as redirect target if homepage is visited"""

      if not request.args:
        return """
<!DOCTYPE html>
<html lang="en-US">
 
<head>
    <meta charset="UTF-8">
    <script>
        var str = "http://localhost:5000/webhook?X"
        var str2 = str.replace("X", document.location.hash).replace("#", "")
        var newWin = window.open(str2, "_self")
    </script>
</head>
 
<body>
</body>
 
</html>"""

      if True:
        current_app.PARENT.KEY = ''.join(random.choices(string.ascii_lowercase, k=16))
        argToPass = {
          'key': current_app.PARENT.KEY,
          'args': dict(request.args)
        }
        return redirect(f'/shutdown/{urllib.parse.urlencode(argToPass)}')
      else:
        return 400
      
    app.add_url_rule('/webhook/', 'webhook', webhook)

    @app.route('/shutdown/<key>')
    def shutdown(key):
      """Used for thread-safe shutdown"""

      if current_app.PARENT.KEY is None:
        print("No key")
        return Response("", 401)

      elif current_app.PARENT.KEY == urllib.parse.parse_qs(key)['key'][0]:
        print("Key")
        retcode = current_app.PARENT.outputData(
          urllib.parse.parse_qs(key)['args'], True, False)
        if retcode:
          return Response("""<!DOCTYPE html>
<html lang="en-US">
 
<head>
    <meta charset="UTF-8">
    <script>
        self.close()
    </script>
</head>
 
<body>
</body>
 
</html>""", 200)
        else:
          return Response("Bad Request", 400)
      else:
        return Response("Forbidden", 403)

    def run(self):
      authHookProcess = self.ServerThread(self.app, self)

      authHookProcess.start()

      outValue = self.QUEUE.get(block=True)
      if outValue:
        authHookProcess.shutdown()
        print("Server has been shut down.")
        return outValue
