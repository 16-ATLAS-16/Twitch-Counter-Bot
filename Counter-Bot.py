#! /usr/bin/env python
import os
import sys
from twitchio.ext import commands
from requests import get
from requests import delete
from requests import post
from requests import patch
import datetime
import time
import dotenv

dotenv.load_dotenv()

#define debug
DEBUG = open("TWITCH_LOGFILE", 'a')
DEBUG.close()

class debug():

    def write(text=None, timestamp=True):
        if text != None:
            DEBUG = open("TWITCH_LOGFILE", 'a')
            DEBUG.write("\n")
            if timestamp == True:
                DEBUG.write("["+str(datetime.datetime.now())+"]> ")
            DEBUG.write(text)
            DEBUG.close()

debug.write("\n", False)
debug.write("@@@@@@@@@@@@@@@@ CODE: INIT SUCCESS @@@@@@@@@@@@@@@@")

#setup helper function to write env variables
def writeEnv(Settings=None):
    if Settings != None:

        values = []
        keys = ["CHANNEL", "BOT_CAP", "AUTO_BLACKLIST", "BLACKLISTED_WORDS", "GREETER_NAME", "GREETER_INDEX", "WELCOME_MARKER", "FOLLOWERS_TIME", "TKN"]
        finalSet = {}
        passThrough = False
        debugWrite = []

        if len(Settings) == len(keys):

            if type(Settings) == dict:

                for setting in Settings:
                    values.append(Settings.get(setting))

                for key in keys:
                    finalSet.update({key: values[keys.index(key)]})

                passThrough =  True

            elif type(Settings) == list:

                for key in keys:
                    finalSet.update({key: Settings[keys.index(key)]})

                passThrough = True

            else:
                Type = str(type(Settings)).split(' ')[1].split("'")[1]
                raise TypeError(f"Incorrect type {Type}, writeEnv takes dict or list.")

            new_env_file = open(".env", 'w')
            new_env_file.close()
            new_env_file = open(".env", 'a')
            
            new_env_file.write("# .env setup, change values at own risk")
            new_env_file.write("\n")
            
            for key in finalSet:
                new_env_file.write(f"\n{key}={finalSet.get(key)}")

            new_env_file.close()

            for key in finalSet:
                debugWrite.append(f"\n{key} |> {finalSet.get(key)}")
            debug.write("Wrote new environment settings to file")
            debug.write(f"{finalSet}", False)

        else:
            raise IndexError(f"Settings provided don't match required parse length. Provided: {len(Settings)}, Required: {len(keys)}")

            
            
#create a setup to write initial env variables. can be re-triggered as needed.
def SetupScreen():
    channel = None
    botcap = 20
    blacklist = True
    blacklisted_phrases = []
    greeters = ['nightbot', 'streamelements', 'streamlabs']
    greeter = 'nightbot'
    word_index = 0
    welcome_marker = None
    duration = 10
    
    def clr():
        for x in range(500):
            print("\n")

    clr()

    #step 1
    while 1:
        try:
            print("<===---~~~ SETUP ~~~---===>")
            print("\n")
            print("Channel Name Setup:")
            channel = input("Enter Your Channel Name > ")
            clr()
            break
        except KeyboardInterrupt:
            clr()

    #step 2
    while 1:
        try:
            print("<====----~~~~ SETUP ~~~~----====>")
            print("\n")
            print("Bot Follow Cap is 20 by default.")
            modify = input("Modify bot cap? [Y/N]> ")
            if modify.lower() == 'y':
                new_cap = input("Enter the new follow cap for bot raid event trigger > ")
                try:
                    botcap = int(new_cap)
                    clr()
                    break
                except:
                    print("Please only enter numerical values.")
                    time.sleep(1)
                    clr()
            elif modify.lower() == 'n':
                new_cap = botcap
                clr()
                break
            else:
                clr()
        except KeyboardInterrupt:
            clr()

    #step 3
    while 1:
        try:
            print("<<======------~~~~~~ SETUP ~~~~~~------======>>")
            print("\n")
            print("Auto Blacklist Bot Phrases is on by default.")
            modify = input("Turn off? [Y/N]> ")
            if modify.lower() == 'y':
                blacklist = False
                clr()
                break
            elif modify.lower() == 'n':
                blacklist = True
                clr()
                break
            else:
                clr()
        except KeyboardInterrupt:
            clr()

    #step 4
    while 1:
        try:
            print("<<======------~~~~~~ SETUP ~~~~~~------======>>")
            print("\n")
            print("Beforfe setup continues, set up some blocked phrases.")
            print("Current blocked phrases: ")
            for phrase in blacklisted_phrases:
                print(f"|- > {phrase}")
            toAdd = input("Enter phrase to add or press CTRL+C to continue > ")
            blacklisted_phrases.append(toAdd)
            clr()
        except KeyboardInterrupt:
            clr()
            break

    #step 5
    while 1:
        try:
            print("<<======------~~~~~~ SETUP ~~~~~~------======>>")
            print("\n")
            print("This bot relies on follow messages to read follows. (patch soon!)\nPlease add the name of any bot that sends a message on follow in chat\n(Only 1 may trigger the follow function on this bot)")
            print("Bot names on list: ")
            for greeter in greeters:
                print(f"| - > {greeter}")
            botToAdd = input("Please enter the name of your bot (streamlabs, nightbot, and streamelements are on the list by default)\n(Press CTRL + C to select, or keep entering names) > ")
            greeters.append(botToAdd)
            clr()
        except KeyboardInterrupt:
            clr()
            break

    while 1:
        try:
            print("<<======------~~~~~~ SETUP ~~~~~~------======>>")
            print("\n")
            print("Now choose 1 from the list below")
            for greeter in greeters:
                print(f"| - > {greeter} | index [{greeters.index(greeter)}]")
            try:
                chosen = input("Choose 1 bot to read follow messages from (index only) > ")
                try:
                    conf = input(f"You selected {greeters[int(chosen)]}, is this correct? [Y/N] > ")
                    conf = conf.lower()
                    if conf == 'y':
                        try:
                            greeter = greeters[int(chosen)]
                            clr()
                            break
                        except:
                            print("Please pick an index off the list provided.")
                    elif conf == 'n':
                        clr()
                    else:
                        clr()
                except KeyboardInterrupt:
                    clr()
            except IndexError:
                print("Please pick an index off the list provided.")
                time.sleep(1)
                clr()
        except KeyboardInterrupt:
            clr()

    print("Hey there. If you're reading this you've made it this far :D")
    time.sleep(5)
    print("There's only a couple more setup stages left, this is to ensure we don't misdetect anything.")
    time.sleep(6)
    print("You ready?")
    input("Press ENTER to proceed! ")

    clr()
    
    while 1:
        try:
            print("<<======------~~~~~~ SETUP ~~~~~~------======>>")
            print("\n")
            print("This next one might sound odd, but trust me it works.")
            phrase = input("Please enter the bot's template follow message > ")
            words = phrase.split(' ')
            clr()

            while 1:
                try:
                    print("<<======------~~~~~~ SETUP ~~~~~~------======>>")
                    print("\n")
                    print("Now please select the index that corresponds to where the username is within the sentence.")
                    for word in words:
                        print(f"| - > [{word}] | index [{words.index(word)}]")
                    try:
                        chosen = input("Word index > ")
                        try:
                            conf = input(f"You selected {words[int(chosen)]}, is this correct? [Y/N] > ")
                            conf = conf.lower()
                            if conf == 'y':
                                word_index = int(chosen)
                                clr()
                                break
                            elif conf == 'n':
                                clr()
                            else:
                                clr()
                        except KeyboardInterrupt:
                            clr()
                    except:
                        print("Please pick an index off the list provided.")
                        time.sleep(1)
                        clr()
                except KeyboardInterrupt:
                    clr()

            while 1:
                try:
                    print("<<======------~~~~~~ SETUP ~~~~~~------======>>")
                    print("\n")
                    print("Now please select the index that corresponds to the greeting word or a greeting marker (Welcome, Follow, etc.).")
                    for word in words:
                        print(f"| - > [{word}] | index [{words.index(word)}]")
                    try:
                        chosen = input("Word index > ")
                        try:
                            conf = input(f"You selected {words[int(chosen)]}, is this correct? [Y/N] > ")
                            conf = conf.lower()
                            if conf == 'y':
                                welcome_marker = words[int(chosen)]
                                clr()
                                break
                            elif conf == 'n':
                                clr()
                            else:
                                clr()
                        except KeyboardInterrupt:
                            clr()
                    except:
                        print("Please pick an index off the list provided.")
                        time.sleep(1)
                        clr()
                except KeyboardInterrupt:
                    clr()
            break
        except KeyboardInterrupt:
            clr()

    #last step (as of v1)
    while 1:
        try:
            print("<<======------~~~~~~ SETUP ~~~~~~------======>>")
            print("\n")
            print("When a bot raid occurs, followers only is enabled. By default this is 10 (mintues)\nHow long should users follow for in order to chat?")
            duration = input("Follow age to chat <in minutes, 1 = 1 minute, etc.> (NON-ZERO!) > ")
            try:
                duration = int(duration)
                clr()
                break
            except:
                print("Please only enter numerical values.")
                time.sleep(1)
                clr()
        except KeyboardInterrupt:
            clr()

    while 1: #last step as of v1.1
        try:
            print("<<======------~~~~~~ SETUP ~~~~~~------======>>")
            print("\n")
            print("FINAL STEP! Congrats on making it :)")
            print("Head to this website and click Authenticate: https://id.twitch.tv/oauth2/authorize?client_id=7583ak4tqsqbnpbdoypfpg2h0ie4tu&redirect_uri=http://localhost&response_type=token+id_token&scope=openid+channel:read:editors+channel:read:hype_train+channel:read:polls+channel:read:predictions+channel:read:redemptions+channel:read:subscriptions+moderation:read+user:edit+user:read:broadcast+user:read:email+user:read:follows+user:read:subscriptions+channel:moderate+chat:edit+chat:read+whispers:read+whispers:edit+channel:manage:polls")
            tkn = input("This should have redirected you to a localhost site.\nPaste the site URL here > ")
            tkn = tkn.split('/')[3].split('=')[1].split('&')[0]
            if len(tkn) == 30:
                clr()
                break
            else:
                print("Invalid URL provided. Please double-check and re-enter.")
                input("ENTER to re-enter ")
                clr()
        except KeyboardInterrupt:
            clr()

    #Final settings data
    print("<<<<========-------- RESULTS --------========>>>>")
    print("\n")
    print(f"Channel Name: {channel}\nBot Follow Cap: {botcap}\nBlacklist Bot Raid Phrases: {blacklist}\nBot to Accept Follow Messages From: {greeter}\nUsername Word Index: {word_index}\nWelcome Marker Word: {welcome_marker}\nFollower Only Min. Follow Age: {duration}")
    print("To re-enter information, please press CTRL + C within the next 10 seconds to start over. (or modify .env as you see fit)")
    time.sleep(10)
    
    writeEnv([channel, botcap, blacklist, blacklisted_phrases, greeter, word_index, welcome_marker, duration, tkn])
    
    print("Config updated. Bot Starting :) ")
    time.sleep(2)
            
            
        
#INITIAL SETUP CODE FOR FIRST TIME RUN
try:
    a = open(".env", 'r')
    a.close()
except FileNotFoundError:
    while 1:
        try:
            SetupScreen()
            break
        except Exception as e:
            print(str(e))

            
#all settings related code is found here.
class settings():
    
    def Load(file=None): #this load notifies the user and writes to debug...
        'Imports custom settings struct from ENV or file specified'

        def LoadEnv(customFile=False, filepath=None):

            failed_import=False
            new_file = None

            debug.write("----SETTINGS: LOAD----")
        
            if customFile == False:
                pass

            else:

                if failed_import == False:
                    debug.write("Attempting settings load from file specified: " + str(file), False)

                    try:
                        os.remove(".env.bkp")
                    except:
                        pass
                                    
                    os.rename(".env", ".env.bkp")
                    debug.write("\n|---- > Renamed default environmental file |> .env -> .env.bkp", False)
                        
                else:
                    debug.write("Attempting settings load from file specified: " + str(new_file), False)
                try:
                    copy_env = open(file, 'rb').read()
                    paste_env = open(".env", 'wb')
                    paste_env.write(copy_env)
                    paste_env.close()
                except FileNotFoundError:
                    pass


            try:

                if sys.platform == 'win32':
                    channel = os.environ["CHANNEL"]
                    bot_cap = os.environ["BOT_CAP"]
                    blacklist = os.environ["AUTO_BLACKLIST"]
                    blacklisted_words = os.environ["BLACKLISTED_WORDS"]
                    greeter = os.environ["GREETER_NAME"]
                    username_index = os.environ["GREETER_INDEX"]
                    welcome_marker = os.environ["WELCOME_MARKER"]
                    follow_time = os.environ["FOLLOWERS_TIME"]
                    tkn = os.environ["TKN"]

                else:

                    def find_setting(setting_name=None):
                        all_settings = open('.env', 'r').read().split('\n')
                        setting_to_return = None

                        for setting in all_settings:
                            if setting_name in setting:
                                setting_to_return = setting.split('=')[1]
                                break

                        return setting_to_return


                    channel = find_setting("CHANNEL")
                    bot_cap = find_setting("BOT_CAP")
                    blacklist = find_setting("AUTO_BLACKLIST")
                    blacklisted_words = find_setting("BLACKLISTED_WORDS")
                    greeter = find_setting("GREETER_NAME")
                    username_index = find_setting("GREETER_INDEX")
                    welcome_marker = find_setting("WELCOME_MARKER")
                    follow_time = find_setting("FOLLOWERS_TIME")
                    tkn = find_setting("TKN")
                    
                debug.write(f"(OS: {sys.platform} |> Successfully loaded settings:")
                    
                Settings = {"Channel": channel,
                            "Bot Follow Cap": bot_cap,
                            "Auto-Blacklist Bot Spam": blacklist,
                            "Blacklisted Words/Phrases": blacklisted_words,
                            "Bot to Read Welcome From": greeter,
                            "Username Index in Welcome": username_index,
                            "Welcome Marker Word": welcome_marker,
                            "Follower Only Time Upon Bot Trigger": follow_time,
                            "Token": tkn}
                    
                for setting in Settings:
                    debug.write(f"|---- > {setting} |> {Settings.get(setting)}", False)

                debug.write("----SETTINGS: LOAD END----")
                print(f"DEBUG: LOAD SUCCESS {Settings}")

                return Settings

            except FileNotFoundError:
                if failed_import == True:
                    os.remove(".env")
                failed_import=True
                debug.write("----SETTINGS: LOAD FAILED----")
                    
                try:
                    new_file = input("The file provided either does not exist or was provided without full path.\nPlease enter the full file path or press CTRL+C to cancel and load defaults in current directory > ")
                    
                except KeyboardInterrupt:
                    print("DEBUG: Loading directory default settings.")
                    debug.write("Restoring old default environment file |> .env.bkp -> .env")
                    os.rename(".env.bkp", ".env")

        for x in range(3):
            try:
                print(f"Loading directory stored settings in: {3-x} | Press CTRL+C to load from different file.", sep=' ', end='\r', flush=True)
                time.sleep(1)
                file = None
                customFile = False
            except KeyboardInterrupt:
                file = input("\n\n\nPlease specify the file (full path) > ")
                customFile = True
                break
        try:
            data = LoadEnv(customFile, file)
        except Exception as e:
            print(str(e))
            input()

        return data

    def silentLoad(): #... and this one doesn't.

        if sys.platform == 'win32':
            channel = os.environ["CHANNEL"]
            bot_cap = os.environ["BOT_CAP"]
            blacklist = os.environ["AUTO_BLACKLIST"]
            blacklisted_words = os.environ["BLACKLISTED_WORDS"]
            greeter = os.environ["GREETER_NAME"]
            username_index = os.environ["GREETER_INDEX"]
            welcome_marker = os.environ["WELCOME_MARKER"]
            follow_time = os.environ["FOLLOWERS_TIME"]
            tkn = os.environ["TKN"]

        else:

            def find_setting(setting_name=None):
                all_settings = open('.env', 'r').read().split('\n')
                setting_to_return = None

                for setting in all_settings:
                    if setting_name in setting:
                        setting_to_return = setting.split('=')[1]
                        break

                return setting_to_return


            channel = find_setting("CHANNEL")
            bot_cap = find_setting("BOT_CAP")
            blacklist = find_setting("AUTO_BLACKLIST")
            blacklisted_words = find_setting("BLACKLISTED_WORDS")
            greeter = find_setting("GREETER_NAME")
            username_index = find_setting("GREETER_INDEX")
            welcome_marker = find_setting("WELCOME_MARKER")
            follow_time = find_setting("FOLLOWERS_TIME")
            tkn = find_setting("TKN")
                    
        Settings = {"Channel": channel,
                    "Bot Follow Cap": bot_cap,
                    "Auto-Blacklist Bot Spam": blacklist,
                    "Blacklisted Words/Phrases": blacklisted_words,
                    "Bot to Read Welcome From": greeter,
                    "Username Index in Welcome": username_index,
                    "Welcome Marker Word": welcome_marker,
                    "Follower Only Time Upon Bot Trigger": follow_time,
                    "Token": tkn}

        return Settings
        




                        

# set up the bot
class Bot(commands.Bot):
    counter = 0
    botlist = []
    streamerID = None

    Settings = settings.Load() # load base settings. key names are the same as what's written to debug for the sake of not having to re-write the return value (yes I'm lazy in that way)
    channelToJoin = Settings.get("Channel")
    bot_cap = int(Settings.get("Bot Follow Cap"))
    blacklist = bool(Settings.get("Auto-Blacklist Bot Spam"))
    blacklisted_words = eval(Settings.get("Blacklisted Words/Phrases"))
    greeter_name = Settings.get("Bot to Read Welcome From")
    user_index = int(Settings.get("Username Index in Welcome"))
    welcome_marker = Settings.get("Welcome Marker Word")
    follow_duration = Settings.get("Follower Only Time Upon Bot Trigger")
    client_id="udejckrsxv14xdt43ut43sto8wc5c4"
    token = Settings.get("Token")

    
    streamerID = None
    prevage=''
    prevprevage=''
    


    def __init__(self):

        super().__init__(
    token=f"{self.token}",
    client_id="7583ak4tqsqbnpbdoypfpg2h0ie4tu",
    nick="crimsoneye16",
    prefix="<prefix goes here>",
    initial_channels=[f"#{self.channelToJoin}"]
)

    async def event_ready(self):
        print("good to go")
        #try:
        #    await self.get_channel(self.channelToJoin).send("Bot Ready!") <- optional and doesn't always work
        #except Exception as e:
        #    print(str(e))

        debug.write("====CHAT: LOG BEGIN====")


    #@bot.event
    async def event_message(self, ctx):
        
        Settings = settings.silentLoad() # constantly updating settings via silent load allows for variables to be changed during runtime, however loading it before bot runs is crucial to make the bot run
        channelToJoin = Settings.get("Channel")
        bot_cap = int(Settings.get("Bot Follow Cap"))
        blacklist = bool(Settings.get("Auto-Blacklist Bot Spam"))
        blacklisted_words = eval(Settings.get("Blacklisted Words/Phrases"))
        greeter_name = Settings.get("Bot to Read Welcome From")
        user_index = int(Settings.get("Username Index in Welcome"))
        welcome_marker = Settings.get("Welcome Marker Word")
        follow_duration = Settings.get("Follower Only Time Upon Bot Trigger")

        message = ctx
        words = message.content.split(' ')
        author = message.author
        channel = message.channel
        try:
            is_welcome = author.name == greeter_name and welcome_marker in words
            is_streamer = author.name == channel.name
            is_mod = author.is_mod
            is_sub = author.is_subscriber
            is_creator = author.id == '495706279'
        except AttributeError:
            is_welcome = False
            is_streamer = False
            is_mod = False
            is_sub = False
            is_creator = False
        
        
        try:
            #DEBUG.write(debug_datetime())
            debug.write(f"{ctx.author.name}: {ctx.content}")
            print(f"{author.name}: {message.content}")
            
            if author.name in self.botlist: # if any chatbot talks and they haven't been banned for whatever reason, silence them.
                await ctx.channel.send(f"/timeout {author.name} 5000000")
                debug.write(f"Timed out {author.name} (BOT USER) for 5000000 seconds")

            for word in words: # simple blacklist because twitch doesn't let bots add blacklisted phrases (yet)
                if word in blacklisted_words:
                    await channel.send(f"/timeout {author.name} 1")
                    await author.send(f"@{author.name} Some words in your message may have been blacklisted and thus your messages were removed.")
                    debug.write(f"Removed {ctx.author.name}'s messages for posting blacklisted words or phrases |> {word}")
                    break
            
            if is_streamer: # make sure to grab the streamer ID in case we poll for followers or make a poll via request.
                self.streamerID = author.id
                    
            if is_welcome: # triggers on user follow. once twitchio allows 
                debug.write("~~~~User Follow Triggered~~~~")

                user=words[int(user_index)]
                if '!' in user:
                    user=user[:-1]
                debug.write(f"| - > Username |> {user}", False)
                
                newList = get(f"https://decapi.me/twitch/accountage/{user}").content.decode().split(',')
                debug.write(f"| - > User Age |> {newList}", False)
                curAge=newList[0]
                
                for item in newList:

                    #print(f"{self.prevage}, {curAge}")
                    
                    if curAge == self.prevage or curAge == self.prevprevage:
                            
                        if user not in self.botlist:
                            self.botlist.append(user)
                            debug.write(f"| - > Added {user} to botlist, user will be banned on bot raid trigger.", False)
                            self.counter += 1

                if self.counter >= int(bot_cap):
                    debug.write("<<<<BOT RAID DETECTED>>>>")
                                
                    await channel.send(f"/followers {follow_duration}")
                    debug.write(">> Enabled 10 minute Followers-Only Mode.", False)
                    await channel.send("/clear")
                    debug.write(">> Cleared Chat to remove any other messages.", False)
                                
                    for user in self.botlist:
                                    
                        await channel.send("/ban " + user + " bot follower.")
                        debug.write(f">> BOT RAID: BANNED |> {user}", False)

                    self.counter = 0
                    self.botlist = []
                    await channel.send("/followersoff")
                    debug.write(">> Disabled Followers-Only Mode. Bot raid crisis averted.", False)

                    
                self.prevprevage = self.prevage
                self.prevage = curAge

                if self.prevage != self.prevprevage and self.prevage != None and self.prevprevage != None:
                    self.botlist.remove(f"{user}")

            if "ab!setFTime" == words[0] and is_streamer:
                if len(words) == 2:
                    try:
                        int(words[1])
                        writeEnv([channelToJoin, bot_cap, blacklist, blacklisted_words, greeter_name, user_index, welcome_marker, words[1]])
                        await channel.send(f"Successfully set variable to: {words[1]}")
                        
                    except ValueError:
                        await channel.send("Usage: ab!setFTime {minutes (integer)}")

                else:
                    await channel.send("Usage: ab!setFTime {minutes (integer)}")

            if "ab!setCap" == words[0] and is_streamer:
                if len(words) == 2:
                    try:
                        int(words[1])
                        writeEnv([channelToJoin, words[1], blacklist, blacklisted_words, greeter_name, user_index, welcome_marker, follow_duration])
                        await channel.send(f"Successfully set cap to: {words[1]}")

                    except ValueError:
                        await channel.send("Usage: ab!setCap {trigger cap (integer)}")

                else:
                    await channel.send("Usage: ab!setCap {trigger cap (integer)}")

            if "ab!setGreeter" == words[0] and is_streamer:
                if len(words) == 4:
                    writeEnv([channelToJoin, bot_cap, blacklist, blacklisted_words, words[1], words[2], words[3], follow_duration])
                    await channel.send(f"Successfully set greeter to {words[1]}, set username index to {words[2]}, and set follow event marker to {words[3]}")
                else:
                    await channel.send("Usage: ab!setGreeter {Bot/Greeter name (string)} {Username index (integer index) {Follow event marking word (string)}")
                    await channel.send("Do ab!varHelp for more.")

            if "ab!varHelp" == words[0] and is_streamer:
                await channel.send("Variable Types Help:")
                await channel.send("string: any characters you can type on a keyboard")
                await channel.send("integer: any whole number")
                await channel.send("(integer) index: integer used to determine a position in a list or dict, starts at 0 for first entry")
                await channel.send("bool: value of either true or false")

            if "ab!commands" == words[0] or "ab!help" == words[0]:
                await channel.send("varHelp : Display variable types help")
                await channel.send("setGreeter : Updates follow trigger conditions (broadcaster only)")
                await channel.send("setCap : Sets the follow cap before anti-bot response is triggered (broadcaster only)")
                await channel.send("setFTime : Sets the follow only mode time in case of bot raid (broadcaster only)")
                await channel.send("poll : Starts a poll. (moderator and above)")

            if "ab!poll" == words[0] and is_mod:
                if len(words) == 6 or len(words) == 7:
                    try:
                        title = words[1]
                        choice_1 = words[2]
                        choice_2 = words[3]
                        dur = int(words[4])
                        cpvote = bool(words[5])
                        if len(words) == 7:
                            votecost = int(words[6])
                        else:
                            votecost = 0

                        resp = post("https://api.twitch.tv/helix/polls", headers={"Authorization": f"Bearer {self.token}",
                                                                                 "Client-Id": f"{self.client_id}",
                                                                                 "Content-Type": "application/json"}, json={"broadcaster_id": f"{self.streamerID}", "title": f"{title}", "choices": [{'title': choice_1}, {'title': choice_2}], "duration": dur})

                    except ValueError:
                        await channel.send("Usage: ab!poll {title (string)} {choice 1 (string)} {choice 2 (string)} {duration (int)} {channel points vote (bool)} {channel point cost (int) [optional]}")

                else:
                    await channel.send("Usage: ab!poll {title (string)} {choice 1 (string)} {choice 2 (string)} {duration (int)} {channel points vote (bool)} {channel point cost (int) [optional]}")

            if "ab!endpoll" == words[0] and is_mod:
                resp = get(f"https://api.twitch.tv/helix/polls?broadcaster_id={self.streamerID}", headers={'Authorization': f"Bearer {self.token}", 'Client-Id': f"{self.client_id}"})
                poll_id = resp.content.decode()[16:52]

                patch('https://api.twitch.tv/helix/polls', headers={"Authorization": f"Bearer {self.token}", "Client-Id": f"{self.client_id}", "Content-Type": "application/json"}, json={"broadcaster_id": f"{self.streamerID}", "id": f"{poll_id}", "status": "TERMINATED"})

            if "ab!botFuncTest" == words[0] and is_creator:
                await channel.send("All systems functional, debug successful.")

                                    
            'Runs every time a message is sent in chat.'
            # make sure the bot ignores itself and the streamer
            try:
                if author.name.lower() == "CrimsonEye16".lower():
                    return

                
                #await bot.handle_commands(ctx)

                # await ctx.channel.send(ctx.content)

                if 'ab!' in words:
                    print(words)
            except Exception as e:
                print(str(e))
        except Exception as e:
            print(str(e))

    async def event_raw_usernotice(self, channel, tags):
        print("join event")
        print(tags)


    @commands.command(name='test')
    async def test(ctx):
        
        await ctx.send('test passed!')

        

if __name__ == "__main__":
    try:
        bot = Bot()
        bot.run()
    except:
        pass

debug.write("<<--Shutting Down-->>")

