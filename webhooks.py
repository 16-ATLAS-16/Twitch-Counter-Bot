from flask import Flask, request, render_template, redirect, current_app, Response
import urllib, threading, sys, queue, random, string
from werkzeug.serving import make_server


class webHook:

  class authHook:
    QUEUE = None
    HOST = 'localhost'
    PORT = 5000
    KEY = None
    app = Flask(__name__)

    def __init__(self,
                 outQueue: queue.Queue = None,
                 overrideHost: str = None,
                 overridePort: int = None):
      """Initialise an authHook object.
      Call authHook.run to run.
      
      Args: 
        outQueue: queue.Queue -> Multiprocessing Queue to return result to.
        overrideHost: str -> Overrides application default host (localhost)
        overridePort: int -> Overrides application default port (5000)
      """
      self.QUEUE = outQueue
      
      if overrideHost and overridePort:
        self.HOST, self.PORT = overrideHost, overridePort
      pass

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
    
    def outputData(self, data=None, affResp: str = None, negResp: str = None):
      """Puts data into the output queue.
      
      Args:
        data: any -> Data to output
        affResp: str -> Response to return if data has successfully been stored
        negResp: str -> Response to return if data has not been stored
      """
      if self.QUEUE and data:
        self.QUEUE.put(data)
        return affResp
      else:
        return negResp

    @app.route('/', methods=["POST", "GET"])
    def home():
      """Homepage.
      Redirects to /webhook if query data is present"""
      if request.method == "POST":
        if request.json:
          try:
            return redirect(        
              f"http://{current_app.PARENT.HOST}:{current_app.PARENT.PORT}/webhook/{urllib.parse.urlencode(request.json)}"
            )
          except TypeError:
            return 400
        else:
          return 400
      else:
          return redirect(
              f'http://{current_app.PARENT.HOST}:{current_app.PARENT.PORT}/shutdown'
              )#"""<h1>Welcome to a temporary homepage</h1>"""

    @app.route('/webhook/<data>', methods=["GET"])
    def webhook(data):
      """Main webhook path.
      Used as redirect target if homepage is visited"""

      #TODO -> implement check for valid response
      args = urllib.parse.parse_qs(data)
      if True:
        current_app.PARENT.KEY = ''.join(random.choices(string.ascii_lowercase, k=16))
        argToPass = {'key': current_app.PARENT.KEY,
                     'args':args}
        return redirect(
          f'http://{current_app.PARENT.HOST}:{current_app.PARENT.PORT}/shutdown/{urllib.parse.urlencode(argToPass)}'
        )
      else:
        return 400

    @app.route('/shutdown/<key>')
    def shutdown(key):
      """Used for thread-safe shutdown."""
      
      if current_app.PARENT.KEY is None:
        return Response("Bad Request", 400)
      elif current_app.PARENT.KEY == urllib.parse.parse_qs(key)['key'][0]:
        retcode = current_app.PARENT.outputData(urllib.parse.parse_qs(key)['args'], True, False)
        if retcode:
          return Response("", 204)
        else:
          return Response("Bad Request.", 400)
      else:
        return Response("Forbidden.", 403)

    def run(self):
        
      authHookProcess = self.ServerThread(self.app, self)
      if not self.QUEUE:
        self.QUEUE = queue.Queue(maxsize=1)

      authHookProcess.start()
      outValue = self.QUEUE.get(block=True)
      if outValue:
        authHookProcess.shutdown()
        return outValue
