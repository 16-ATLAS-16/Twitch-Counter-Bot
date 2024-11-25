#from token_manager import TokenManager
#import queue

#retQueue = queue.Queue()
#manager = TokenManager(out=retQueue,
#  refreshToken='brbbxpdai5lh7swbeqif5a8gnx1ydm3ncqa8niyjg059tb5etw')
#print(manager.refresh())
#brbbxpdai5lh7swbeqif5a8gnx1ydm3ncqa8niyjg059tb5etw
#brbbxpdai5lh7swbeqif5a8gnx1ydm3ncqa8niyjg059tb5etw , token='ehd3vagxt9fva7pgewqvwlch751j5j'

#pp0m9ufxh85jedq6qis2h3f1t30m4s4o1tgrj9mmg83x9910ct
#w2caxvajbpd5vbcbc2wnsndbi20z2l
from bot import Bot

bot = Bot(channels=['drbreadtv'], token='5g26af8vklrndtvwn663itbir4v0pw')
bot.loop.create_task(bot.sub_all())
bot.run()
input()
