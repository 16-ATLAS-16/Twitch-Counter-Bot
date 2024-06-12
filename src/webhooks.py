import urllib, threading, sys, queue, random, string, logging
from flask import Flask, request, render_template, redirect, current_app, Response
from werkzeug.serving import make_server


class WebHook:

  class AuthHook:
    QUEUE = None
    KEY = None
    app = Flask(__name__)

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

    @app.route('/', methods=["GET"])
    def home():
      """Homepage.
			Redirects to /webhook if query data is present"""

      return redirect(f"/webhook?{urllib.parse.urlencode(request.args)}")

    @app.route('/webhook', methods=["GET"])
    def webhook():
      """Main webhook path.
			Used as redirect target if homepage is visited"""

      #TODO -> implement check for valid response
      if not request.args:
        return Response("Bad request", 400)

      if True:
        current_app.PARENT.KEY = ''.join(random.choices(string.ascii_lowercase, k=16))
        argToPass = {
          'key': current_app.PARENT.KEY,
          'args': dict(request.args)
        }
        return redirect(f'/shutdown/{urllib.parse.urlencode(argToPass)}')
      else:
        return 400

    @app.route('/shutdown/<key>')
    def shutdown(key):
      """Used for thread-safe shutdown"""

      if current_app.PARENT.KEY is None:
        return 401

      elif current_app.PARENT.KEY == urllib.parse.parse_qs(key)['key'][0]:
        retcode = current_app.PARENT.outputData(
          urllib.parse.parse_qs(key)['args'], True, False)
        if retcode:
          return Response("", 204)
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
