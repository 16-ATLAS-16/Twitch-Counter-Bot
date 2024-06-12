from memory_profiler import profile
import shelve

@profile
def main():
    A=shelve.open('test')
    q=[]
    a=open('bot.py', 'r')
    q=a.readlines()
    a.close()
    A['test'] = q
    print(q[:5])
    print('class Bot(commands.Bot):\n' in q)

    del q
    del a

    q = A['test']
    A.close()

    del q
    del A
    print("k done!")
    print("something else")

if __name__ == '__main__':
    main()
