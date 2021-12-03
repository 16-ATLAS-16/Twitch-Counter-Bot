#! /usr/bin/env python
import os
import sys
#try:
#    if sys.version_info < (3,7):
#        raise ImportError('Incorrect Version')
##    else:
##        print("this triggers")
##        self = open(__file__, 'r')
##        data = self.readlines()
##        self.close()
##        print(data[3:75])
##        input()
##        new = open(__file__, 'w')
##        linecount = 0
##        undo = False
##        if data[0][0] == '#':
##            for line in data:
##                if line != data[0] and line[0] =='#':
##                    if "UNDO END" in line:
##                        undo = False
##                    if undo == True:
##                        new.write(line[1:])
##                        print(f'Wrote {line[1:]}')
##                    if "UNDO START" in line:
##                        undo = True
##                elif linecount >= 3 and linecount <= 87:
##                    print("Wrote none")
##                    print(f'Skipped {line}')
##                    pass
##                else:
##                    print(f"Line : {linecount}")
##                    print(f'Wrote {line}')
##                    new.write(line)
##                linecount += 1
##        new.close()
##        os.popen(__file__)
##        sys.exit(0)
##        
##
##except ImportError:
##
##    import sys
##    import os
##    if sys.version_info < (3,7):
##        if sys.platform == 'linux':
##            cmdOutput = os.popen('whereis python').read()
##            greatestVersion = ''
##
##            for version in cmdOutput.split('\n')[0].split(' '):
##                if version.split('/')[-1][-3:] > greatestVersion.split('/')[-1][-3:]:
##                    try:
##                        int(version.split('/')[-1][-3])
##                        int(version.split('/')[-1][-1])
##                        greatestVersion = version
##                    except:
##                        pass
##
##            if greatestVersion.split('/')[-1][-3:] >= '3.7':
##                prevData = open('Counter-Bot.py', 'r').readlines()
##                newData = open('Counter-Bot.py', 'w')
##                for line in prevData:
##                    if prevData.index(line) == 0:
##                        newData.write('#! '+str(greatestVersion)+'\n')
##                    else:
##                        newData.write(line)
##
##                newData.close()
##
##                os.popen('./Counter-Bot.py')
##                sys.exit(0)
##
##            else:
##                print("Python version 3.7.0 or greater required. Please install it, then re-run this script.")
##                input("Press ENTER to exit.")
##                sys.exit(1)
##
##        else:
##            print("Python version 3.7.0 or greater required. Please install it, then re-run this script.")
##            input("Press ENTER to exit.")
##            sys.exit(1)
##
##    else:
##        os.system('pip'+str(sys.version_info[0])+'.'+str(sys.version_info[1])+' install -r requirements.txt')
##        os.popen('./Counter-Bot.py')
##        sys.exit(0)
 #START
from twitchio.ext import commands
import twitchio
from requests import get
from requests import delete
from requests import post
from requests import patch
import datetime
import time
import dotenv
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import webbrowser
import threading
import concurrent.futures
import asyncio
import re

#dotenv.load_dotenv()
os.chdir(__file__.replace('Counter-Bot.py', ''))
#define debug
try:
    DEBUG = open("TWITCH_LOGFILE", 'a')
    DEBUG.close()
except Exception as e:
    print(e)
    input()
class debug():

    def write(text=None, timestamp=True):
        if text:
            DEBUG = open("TWITCH_LOGFILE", 'a', encoding='utf-8')
            DEBUG.write("\n")
            if timestamp == True:
                DEBUG.write("["+str(datetime.datetime.now())+"]> ")
            DEBUG.write(text)
            DEBUG.close()

debug.write("\n", False)
debug.write("@@@@@@@@@@@@@@@@ CODE: INIT SUCCESS @@@@@@@@@@@@@@@@")

#setup helper function to write env variables

def writeEnv(Settings=None, path_to_file=None):
    if Settings and path_to_file:

        values = []
        keys = ["CHANNEL", "BOT_CAP", "AUTO_BLACKLIST", "BLACKLISTED_WORDS", "GREETER_NAME", "GREETER_INDEX", "WELCOME_MARKER", "FOLLOWERS_TIME", "TKN"]
        finalSet = {}
        passThrough = False
        debugWrite = []

        if len(Settings) == len(keys) or len(Settings) == len(keys)-1:

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

            new_env_file = open(path_to_file, 'w')
            new_env_file.close()
            new_env_file = open(path_to_file, 'a')
            
            new_env_file.write("# .pf setup, change values at own risk")
            new_env_file.write("\n")
            
            for key in finalSet:
                if len(Settings) == len(keys)-1:
                    if keys.index(key) == 9:
                        pass
                else:
                    new_env_file.write(f"\n{key}={finalSet.get(key)}")

            new_env_file.close()

            for key in finalSet:
                debugWrite.append(f"\n{key} |> {finalSet.get(key)}")
            debug.write(f"Wrote new environment settings to file: {path_to_file}")
            debug.write(f"{finalSet}", False)

        else:
            raise IndexError(f"Settings provided don't match required parse length. Provided: {len(Settings)}, Required: {len(keys)}")

def writePF(Settings=None, out_path=None, overwrite=False):
    if Settings:

        keys = ["CHANNEL", "BOT_CAP", "AUTO_BLACKLIST", "BLACKLISTED_WORDS", "GREETER_NAME", "GREETER_INDEX", "WELCOME_MARKER", "FOLLOWERS_TIME"]
        if len(Settings) == len(keys):

            fileExists = False
            
            try:
                f = open(f'{out_path}\\{Settings[0]}.pf', 'a')
                f.close()
                
                if not overwrite:
                    fileExists = True
                    
            except FileNotFoundError:
                pass

            if not fileExists:
                if not out_path:
                    out_path = os.getcwd()
                file = open(f'{out_path}\\{Settings[0]}.pf', 'w')

                for key in keys:
                    file.write(f'\n{key}={Settings[keys.index(key)]}')

                file.close()

            else:
                raise Exception("Output File Already Exists")

        else:
            if len(Settings) > len(keys):
                raise Exception(f"Too many arguments provided. Got {len(Settings)} | Expected {len(keys)}")

            else:
                raise Exception(f"Too few arguments provided. Got {len(Settings)} | Expected {len(keys)}")

        
        



#this next one's a bit of a doozy so hold tight
# styles follow format {name:{style item:{setting:value}}}, any style that isn't defined will return default or first defined col for other widget depending on setting.
# values such as buttonAlt are for toggleable buttons such as the boolButton (replacement for Checkbutton for better visual representation of a boolean switch)

styles={'dark':{'window':{'bg':'#323232'},
                'button':{'bg':'#484848',
                             'fg':'#ffffff',
                          'relief':'flat'},
                   'buttonAlt':{'bg':'#848484',
                                'fg':'#000000'},
                   'inputField':{'bg':'#484848',
                                 'fg':'#ffffff',
                                 'justify':CENTER,
                                 'relief':'flat'},
                   'checkbutton':{'bg':'#323232',
                                  'fg':'#848484'},
                   'radiobutton':{'bg':'#323232',
                                  'fg':'#848484'},
                'label':{'bg':'#323232',
                         'fg':'#ffffff',
                         'justify':CENTER},
                'optionMenu':{'bg':'#484848',
                              'fg':'#ffffff',
                              'arrowcolor':'#ffffff'}
                                  },
        'light':{'window':{'bg':'#ffffff'},
                 'button':{'bg':'#ffffff',
                           'fg':'#000000'},
                 'buttonAlt':{'bg':'#000000',
                              'fg':'#ffffff'},
                 'inputField':{'bg':'#ffffff',
                               'fg':'#000000',
                               'justify':CENTER},
                 'checkbutton':{'bg':'#ffffff',
                                'fg':'#000000'},
                 'radiobutton':{'bg':'#ffffff',
                                'fg':'#000000'},
                 'label':{'bg':'#ffffff',
                          'fg':'#000000'},
                 'optionMenu':{'bg':'#ffffff',
                               'fg':'#000000'}
                                  }}

class boolButton(Button): # better version of a checkbutton.

    value = False
    btn = None
    toggleCommand = None

    def __init__(self, states=None, defaultValue=False, toggleCommand=None, *args, **kwargs): # example for states {'off':{'text':'off','bg':'red','fg':'black'}, 'on':{'text':'on','bg':'green','fg':'black'}}
        Button.__init__(self, *args, **kwargs)
        Button.configure(self, command=lambda: boolButton.toggleButton(states, self))
        if defaultValue == False:
            boolButton.toggleButton(states, self)
            boolButton.toggleButton(states, self)
        else:
            boolButton.toggleButton(states, self)
        boolButton.toggleCommand = toggleCommand

    def toggleButton(opts, btn):

        if btn.value:
            btn['text'] = opts.get('off').get('text')
            btn['bg'] = opts.get('off').get('bg')
            btn['fg'] = opts.get('off').get('fg')
            btn['relief'] = 'raised'

        if not btn.value:
            btn['text'] = opts.get('on').get('text')
            btn['bg'] = opts.get('on').get('bg')
            btn['fg'] = opts.get('on').get('fg')
            btn['relief'] = 'sunken'

        btn.value = not btn.value
        if btn.toggleCommand:
            btn.toggleCommand()

def findOpt(Widget=None, Style=None, styleSet=None, specificOption=None, overrides=None): # Finds style options for the widget provided from either default styles list or a given set. lookups for specific options are supported, but only 1 option at a time may be looked up.

        if overrides == None or overrides.get(specificOption) == None:
            if styleSet != None and Style != None:
                if Widget != None:
                    if specificOption == None:
                        #print(f"returning {styleSet.get(Style).get(Widget)}")
                        return styleSet.get(Style).get(Widget)

                    elif specificOption != None:
                        #print(f"STYLE {Style}, STYLESET {styleSet}")
                        if styleSet.get(Style).get(Widget) != None:
                         #   print(f"request {Widget} returning {styleSet.get(Style).get(Widget).get(specificOption)}")
                            return styleSet.get(Style).get(Widget).get(specificOption)
                        else:
                            return None

                else:
                    if specificOption != None:
                        #print(f"request {Widget} returning {styleSet.get(Style).get(specificOption)}")
                        return styleSet.get(Style).get(specificOption)

                    else:
                        #print(f"request {Widget} returning None")
                        return None

            elif Style == None and styleSet != None and specificOption != None:
                if Widget != None:
                    #print(f"request {Widget} returning {styleSet.get(Widget).get(specificOption)}")
                    return styleSet.get(Widget).get(specificOption)

                elif Widget == None:
                    #print(f"request {Widget} returning {styleSet.get(specificOption)}")
                    return styleSet.get(specificOption)

            else:
                #print(f"request {Widget} returning None")
                return None
        elif overrides != None and specificOption != None:
            #print(f"request {Widget} returning {overrides.get(specificOption)}")
            return overrides.get(specificOption)

        else:
            return None

def initialize(windowOptions=None, style=None, widgets=[], Master=None): # main function to create a tkinter window and add widgets to it. messy, I know; but it works and doesn't need me to rewrite half the code for multiple days. might also work with json files.

    retWidgets = []
    retVars = [] # NOTE: retVars uses tuples with structure (variable, attachedObject).

    def createWidget(Widget, widgetOpts): # this function is responsible for adding the widget to the main window.

        if list(widgetOpts.keys())[0] != 'menu':
            wOpts = widgetOpts.get(list(widgetOpts.keys())[0])
            if 'pos' in wOpts:
                if type(wOpts.get('pos')) == tuple:
                    posKey = 'posTuple'
                if type(wOpts.get('pos')) == list:
                    posKey = 'posList'
                if type(wOpts.get('pos')) == dict:
                    posKey = 'posDict'

            elif 'side' in wOpts:
                posKey = 'posPack'
                
            elif 'row' in wOpts:
                posKey = 'posGrid'
                    
            elif 'x' in wOpts:
                if 'y' in wOpts:
                    posKey = 'posDict2'

            elif wOpts.get('placemode') == 'pack' and wOpts.get('side') == None:
                posKey = 'posPack'

            else:
                posKey = None

            #print(posKey, wOpts)
            
            if posKey == 'posTuple' or posKey == 'posList':
                Widget.place(x=wOpts.get('pos')[0], y=wOpts.get('pos')[1], width=wOpts.get('placeWidth'), height=wOpts.get('placeHeight'), padx=wOpts.get('padx'), pady=wOpts.get('pady'), ipadx=wOpts.get('ipadx'), ipady=wOpts.get('ipady'))

            elif posKey == 'posDict':
                Widget.place(x=wOpts.get('pos').get('x'), y=wOpts.get('pos').get('y'), width=wOpts.get('placeWidth'), height=wOpts.get('placeHeight'), padx=wOpts.get('padx'), pady=wOpts.get('pady'), ipadx=wOpts.get('ipadx'), ipady=wOpts.get('ipady'))

            elif posKey == 'posDict2':
                Widget.place(x=wOpts.get('x'), y=wOpts.get('y'), padx=wOpts.get('padx'), pady=wOpts.get('pady'), ipadx=wOpts.get('ipadx'), ipady=wOpts.get('ipady'))

            elif posKey == 'posPack':
                Widget.pack(side=wOpts.get('side'), padx=wOpts.get('padx'), pady=wOpts.get('pady'), ipadx=wOpts.get('ipadx'), ipady=wOpts.get('ipady'))

            elif posKey == 'posGrid':
                Widget.grid(row=wOpts.get('row'), column=wOpts.get('column'), padx=wOpts.get('padx'), pady=wOpts.get('pady'), ipadx=wOpts.get('ipadx'), ipady=wOpts.get('ipady'))

            else:
                print(f"TKUI NOTICE: Widget {widget} at index {list(widgetOpts.keys())[0]} has been given an invalid position descriptor.")

            

    if not Master:
        mainWindow = Tk() # create the main window
        #print(windowOptions) # debug print because I said so
        mainWindow.title(findOpt(None, specificOption='name', styleSet=windowOptions)) # set window title
        mainWindow['bg'] = findOpt('window', style, styleSet=styles).get('bg') # set window background
        mainWindow.geometry(findOpt(None, specificOption='geometry', styleSet=windowOptions)) # and the geometry (size) too. don't want a small window for something big like a fullscreen application

    else:
        mainWindow = Master

    for conf in widgets: # iterate the widgets list
        #print(conf)
        try:
            widget = list(conf.keys())[0] # get options
        except:
            break
        #print(f"processing : {conf}")
        try:
            if conf.get(widget).get('master').get("widgetIndex") != None: # if the widget has a desired parent defined return it
                master=retWidgets[int(conf.get(widget).get('master').get("widgetIndex"))]
            else:
                master=conf.get(widget).get('master') # otherwise default to the defined master (non-specific to the current list of widgets)
        except:
            master=conf.get(widget).get('master') # handle exceptions and default to the master there (I forgot when this exception occurs but it seems to fix it)

        if Master and not master:
            master = Master

        # from this point on it just selects the widget type given the name of the widget, and sets it up with the style provided. sometimes themed tkinter is used because normal tkinter either doesn't have the option or it looks ugly :P
        if widget == 'button':
            new = Button(master,
                         activebackground=findOpt(widget, style, styles, 'activebackground', conf.get(widget)),
                               activeforeground=findOpt(widget, style, styles, 'activeforeground', conf.get(widget)),
                               bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                               bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                               command=conf.get(widget).get('command'),
                               fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                               font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                               height=conf.get(widget).get('height'),
                               highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                               image=conf.get(widget).get('image'),
                               justify=findOpt(widget, style, styles, 'justify', conf.get(widget)),
                               padx=findOpt(widget, style, styles, 'padx', conf.get(widget)),
                               pady=findOpt(widget, style, styles, 'pady', conf.get(widget)),
                               relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                               state=conf.get(widget).get('state'),
                               text=conf.get(widget).get('text'),
                               underline=conf.get(widget).get('underline'),
                               width=conf.get(widget).get('width'),
                               wraplength=conf.get(widget).get('wraplength')
                               )

        elif widget == 'boolButton': # includes my custom boolean button because it's more fun that way (this was a pain to write btw)
            new = boolButton(master=master,
                             states=conf.get(widget).get('states'),
                             defaultValue=conf.get(widget).get('defaultValue'),
                                   activebackground=findOpt(widget, style, styles, 'activebackground', conf.get(widget)),
                                   activeforeground=findOpt(widget, style, styles, 'activeforeground', conf.get(widget)),
                                   bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                                   bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                                   fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                                   font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                                   height=conf.get(widget).get('height'),
                                   highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                                   image=conf.get(widget).get('image'),
                                   justify=findOpt(widget, style, styles, 'justify', conf.get(widget)),
                                   padx=findOpt(widget, style, styles, 'padx', conf.get(widget)),
                                   pady=findOpt(widget, style, styles, 'pady', conf.get(widget)),
                                   relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                                   state=conf.get(widget).get('state'),
                                   underline=conf.get(widget).get('underline'),
                                   width=conf.get(widget).get('width'),
                                   wraplength=conf.get(widget).get('wraplength')
                                   )

        elif widget == 'canvas':
            new = Canvas(master,
                         bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                         bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                         confine=conf.get(widget).get('confine'),
                         cursor=conf.get(widget).get('cursor'),
                         height=conf.get(widget).get('height'),
                         highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                         relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                         scrollregion=conf.get(widget).get('scrollregion'),
                         width=conf.get(widget).get('width'),
                         xscrollincrement=conf.get(widget).get('xscrollincrement'),
                         xscrollcommand=conf.get(widget).get('xscrollcommand'),
                         yscrollincrement=conf.get(widget).get('yscrollincrement'),
                         yscrollcommand=conf.get(widget).get('yscrollcommand')
                         )

        elif widget == 'checkbutton':
            new = Checkbutton(master,
                              activebackground=findOpt(widget, style, styles, 'activebackground', conf.get(widget)),
                              activeforeground=findOpt(widget, style, styles, 'activeforeground', conf.get(widget)),
                              bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                              bitmap=conf.get(widget).get('bitmap'),
                              bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                              command=conf.get(widget).get('command'),
                              cursor=conf.get(widget).get('cursor'),
                              disabledforeground=findOpt(widget, style, styles, 'disabledforeground', conf.get(widget)),
                              font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                              fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                              height=conf.get(widget).get('height'),
                              highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                              image=conf.get(widget).get('image'),
                              justify=findOpt(widget, style, styles, 'justify', conf.get(widget)),
                              offvalue=conf.get(widget).get('offvalue'),
                              onvalue=conf.get(widget).get('onvalue'),
                              padx=findOpt(widget, style, styles, 'padx', conf.get(widget)),
                              pady=findOpt(widget, style, styles, 'pady', conf.get(widget)),
                              relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                              selectcolor=findOpt(widget, style, styles, 'selectcolor', conf.get(widget)),
                              selectimage=conf.get(widget).get('selectimage'),
                              state=conf.get(widget).get('state'),
                              text=conf.get(widget).get('text'),
                              underline=conf.get(widget).get('underline'),
                              width=conf.get(widget).get('width'),
                              wraplength=conf.get(widget).get('wraplength')
                              )

        elif widget == 'entry' or widget == 'inputField':
            wid = 'inputField'
            new = Entry(master,
                        bg=findOpt(wid, style, styles, 'bg', conf.get(widget)),
                        bd=findOpt(wid, style, styles, 'bd', conf.get(widget)),
                        cursor=conf.get(widget).get('cursor'),
                        font=findOpt(wid, style, styles, 'font', conf.get(widget)),
                        exportselection=conf.get(widget).get('exportselection'),
                        fg=findOpt(wid, style, styles, 'fg', conf.get(widget)),
                        highlightcolor=findOpt(wid, style, styles, 'highlightcolor', conf.get(widget)),
                        justify=findOpt(wid, style, styles, 'justify', conf.get(widget)),
                        relief=findOpt(wid, style, styles, 'relief', conf.get(widget)),
                        selectbackground=findOpt(wid, style, styles, 'selectbackground', conf.get(widget)),
                        selectforeground=findOpt(wid, style, styles, 'selectforeground', conf.get(widget)),
                        show=conf.get(widget).get('show'),
                        textvariable=conf.get(widget).get('textvariable'),
                        width=conf.get(widget).get('width')
                        )

        elif widget == 'frame':
            new = Frame(master,
                        bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                        bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                        cursor=conf.get(widget).get('cursor'),
                        height=conf.get(widget).get('height'),
                        highlightbackground=conf.get(widget).get('highlightbackground'),
                        relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                        width=conf.get(widget).get('width')
                        )

        elif widget == 'label':
            new = Label(master,
                        anchor=conf.get(widget).get('anchor'),
                        bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                        bitmap=conf.get(widget).get('bitmap'),
                        bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                        cursor=conf.get(widget).get('cursor'),
                        font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                        fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                        height=conf.get(widget).get('height'),
                        image=conf.get(widget).get('image'),
                        justify=findOpt(widget, style, styles, 'justify', conf.get(widget)),
                        padx=findOpt(widget, style, styles, 'padx', conf.get(widget)),
                        pady=findOpt(widget, style, styles, 'pady', conf.get(widget)),
                        relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                        text=conf.get(widget).get('text'),
                        textvariable=conf.get(widget).get('textvariable'),
                        underline=conf.get(widget).get('underline'),
                        width=conf.get(widget).get('width'),
                        wraplength=conf.get(widget).get('wraplength')
                        )

        elif widget == 'listbox':
            new = Listbox(master,
                          bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                          cursor=conf.get(widget).get('cursor'),
                          font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                          fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                          height=conf.get(widget).get('height'),
                          highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                          highlightthickness=findOpt(widget, style, styles, 'highlightthickness', conf.get(widget)),
                          relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                          selectbackground=findOpt(widget, style, styles, 'selectbackground', conf.get(widget)),
                          selectmode=conf.get(widget).get('selectmode'),
                          width=conf.get(widget).get('width'),
                          xscrollcommand=conf.get(widget).get('xscrollcommand'),
                          yscrollcommand=conf.get(widget).get('yscrollcommand')
                          )

        elif widget == 'menubutton':
            new = Menubutton(master,
                             activebackground=findOpt(widget, style, styles, 'activebackground', conf.get(widget)),
                             activeforeground=findOpt(widget, style, styles, 'activeforeground', conf.get(widget)),
                             anchor=conf.get(widget).get('anchor'),
                             bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                             bitmap=conf.get(widget).get('bitmap'),
                             bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                             cursor=conf.get(widget).get('cursor'),
                             direction=conf.get(widget).get('direction'),
                             disabledforeground=findOpt(widget, style, styles, 'disabledforeground', conf.get(widget)),
                             fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                             height=conf.get(widget).get('height'),
                             highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                             image=conf.get(widget).get('image'),
                             justify=findOpt(wid, style, styles, 'justify', conf.get(widget)),
                             menu=conf.get(widget).get('menu'),
                             padx=findOpt(widget, style, styles, 'padx', conf.get(widget)),
                             pady=findOpt(widget, style, styles, 'pady', conf.get(widget)),
                             relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                             state=conf.get(widget).get('state'),
                             text=conf.get(widget).get('text'),
                             textvariable=conf.get(widget).get('textvariable'),
                             underline=conf.get(widget).get('underline'),
                             width=conf.get(widget).get('width'),
                             wraplength=conf.get(widget).get('wraplength')
                             )
                                                                            #heh nice line number
        elif widget == 'optionMenu':
            if conf.get(widget).get('values') != None:
                if conf.get(widget).get('variableType') == 'int':
                    newVar = IntVar(mainWindow)
                else:
                    newVar = StringVar(mainWindow)
            else:
                newVar = StringVar(mainWindow)

            Style=ttk.Style()
            Style.configure("NewStyle.TMenubutton",
                            foreground=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                            background=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                            )

            new = ttk.OptionMenu(master,
                             newVar,
                             conf.get(widget).get('default'),
                             *conf.get(widget).get('values'),
                             style="NewStyle.TMenubutton",
                             command=conf.get(widget).get("command")
                             )
            retVars.append((newVar, new))

        elif widget == 'menu':
            new = Menu(master,
                       activebackground=findOpt(widget, style, styles, 'activebackground', conf.get(widget)),
                       activeborderwidth=findOpt(widget, style, styles, 'activeborderwidth', conf.get(widget)),
                       activeforeground=findOpt(widget, style, styles, 'activeforeground', conf.get(widget)),
                       bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                       bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                       cursor=conf.get(widget).get('cursor'),
                       disabledforeground=findOpt(widget, style, styles, 'disabledforeground', conf.get(widget)),
                       font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                       fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                       postcommand=conf.get(widget).get('postcommand'),
                       relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                       image=conf.get(widget).get('image'),
                       selectcolor=conf.get(widget).get('selectcolor'),
                       tearoff=conf.get(widget).get('tearoff'),
                       title=conf.get(widget).get('title')
                       )

        elif widget == 'message':
            new = Message(master,
                          anchor=conf.get(widget).get('anchor'),
                          bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                          bitmap=conf.get(widget).get('bitmap'),
                          cursor=conf.get(widget).get('cursor'),
                          font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                          fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                          height=conf.get(widget).get('height'),
                          image=conf.get(widget).get('image'),
                          justify=findOpt(wid, style, styles, 'justify', conf.get(widget)),
                          padx=findOpt(widget, style, styles, 'padx', conf.get(widget)),
                          pady=findOpt(widget, style, styles, 'pady', conf.get(widget)),
                          relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                          text=conf.get(widget).get('text'),
                          textvariable=conf.get(widget).get('textvariable'),
                          underline=conf.get(widget).get('underline'),
                          width=conf.get(widget).get('width'),
                          wraplength=conf.get(widget).get('wraplength')
                          )

        elif widget == 'radiobutton':
            new = Radiobutton(master,
                              activebackground=findOpt(widget, style, styles, 'activebackground', conf.get(widget)),
                              activeforeground=findOpt(widget, style, styles, 'activeforeground', conf.get(widget)),
                              anchor=conf.get(widget).get('anchor'),
                              bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                              bitmap=conf.get(widget).get('bitmap'),
                              borderwidth=findOpt(widget, style, styles, 'borderwidth', conf.get(widget)),
                              command=conf.get(widget).get('command'),
                              cursor=conf.get(widget).get('cursor'),
                              font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                              fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                              height=conf.get(widget).get('height'),
                              highlightbackground=findOpt(widget, style, styles, 'highlightbackground', conf.get(widget)),
                              highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                              image=conf.get(widget).get('image'),
                              justify=findOpt(wid, style, styles, 'justify', conf.get(widget)),
                              padx=findOpt(widget, style, styles, 'padx', conf.get(widget)),
                              pady=findOpt(widget, style, styles, 'pady', conf.get(widget)),
                              relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                              selectcolor=findOpt(widget, style, styles, 'selectcolor', conf.get(widget)),
                              selectimage=conf.get(widget).get('selectimage'),
                              state=conf.get(widget).get('state'),
                              text=conf.get(widget).get('text'),
                              textvariable=conf.get(widget).get('textvariable'),
                              underline=conf.get(widget).get('underline'),
                              value=conf.get(widget).get('value'),
                              variable=conf.get(widget).get('variable'),
                              width=conf.get(widget).get('width'),
                              wraplength=conf.get(widget).get('wraplength')
                              )

        elif widget == 'scale':
            new = Scale(master,
                        activebackground=findOpt(widget, style, styles, 'activebackground', conf.get(widget)),
                        bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                        command=conf.get(widget).get('command'),
                        cursor=conf.get(widget).get('cursor'),
                        digits=conf.get(widget).get('digits'),
                        font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                        fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                        from_ = conf.get(widget).get('from_'),
                        highlightbackground=findOpt(widget, style, styles, 'highlightbackground', conf.get(widget)),
                        highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                        label=conf.get(widget).get('label'),
                        length=conf.get(widget).get('length'),
                        orient=conf.get(widget).get('orient'),
                        relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                        repeatdelay=conf.get(widget).get('repeatdelay'),
                        resolution=conf.get(widget).get('resolution'),
                        showvalue=conf.get(widget).get('showvalue'),
                        sliderlength=conf.get(widget).get('sliderlength'),
                        state=conf.get(widget).get('state'),
                        takefocus=conf.get(widget).get('takefocus'),
                        tickinterval=conf.get(widget).get('tickinterval'),
                        to=conf.get(widget).get('to'),
                        troughcolor=findOpt(widget, style, styles, 'troughcolor', conf.get(widget)),
                        variable=conf.get(widget).get('variable'),
                        width=conf.get(widget).get('width')
                        )

        elif widget == 'scrollbar':
            new = Scrollbar(master,
                            activebackground=findOpt(widget, style, styles, 'activebackground', conf.get(widget)),
                            bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                            bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                            command=conf.get(widget).get('command'),
                            cursor=conf.get(widget).get('cursor'),
                            elementborderwidth=conf.get(widget).get('elementborderwidth'),
                            highlightbackground=findOpt(widget, style, styles, 'highlightbackground', conf.get(widget)),
                            highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                            highlightthickness=findOpt(widget, style, styles, 'highlightthickness', conf.get(widget)),
                            jump=conf.get(widget).get('jump'),
                            orient=conf.get(widget).get('orient'),
                            repeatdelay=conf.get(widget).get('repeatdelay'),
                            repeatinterval=conf.get(widget).get('repeatinterval'),
                            takefocus=conf.get(widget).get('takefocus'),
                            troughcolor=findOpt(widget, style, styles, 'troughcolor', conf.get(widget)),
                            width=conf.get(widget).get('width')
                            )

        elif widget == 'text':
            new = Text(master,
                       bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                       bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                       cursor=conf.get(widget).get('cursor'),
                       exportselection=conf.get(widget).get('exportselection'),
                       font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                       fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                       height=conf.get(widget).get('height'),
                       highlightbackground=findOpt(widget, style, styles, 'highlightbackground', conf.get(widget)),
                       highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                       highlightthickness=findOpt(widget, style, styles, 'highlightthickness', conf.get(widget)),
                       insertbackground=conf.get(widget).get('insertbackground'),
                       insertborderwidth=conf.get(widget).get('insertborderwidth'),
                       insertofftime=conf.get(widget).get('insertofftime'),
                       insertontime=conf.get(widget).get('insertontime'),
                       insertwidth=conf.get(widget).get('insertwidth'),
                       padx=findOpt(widget, style, styles, 'padx', conf.get(widget)),
                       pady=findOpt(widget, style, styles, 'pady', conf.get(widget)),
                       relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                       selectbackground=findOpt(widget, style, styles, 'selectbackground', conf.get(widget)),
                       selectborderwidth=conf.get(widget).get('selectborderwidth'),
                       spacing1=conf.get(widget).get('spacing1'),
                       spacing2=conf.get(widget).get('spacing2'),
                       spacing3=conf.get(widget).get('spacing3'),
                       state=conf.get(widget).get('state'),
                       tabs=conf.get(widget).get('tabs'),
                       width=conf.get(widget).get('width'),
                       wrap=conf.get(widget).get('wrap'),
                       xscrollcommand=conf.get(widget).get('xscrollcommand'),
                       yscrollcommand=conf.get(widget).get('yscrollcommand')
                       )

        elif widget == 'toplevel':
            new = Toplevel(bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                           bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                           cursor=conf.get(widget).get('cursor'),
                           class_=conf.get(widget).get('class_'),
                           font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                           fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                           relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                           height=conf.get(widget).get('height'),
                           width=conf.get(widget).get('width')
                           )

        elif widget == 'spinbox':
            new = Spinbox(master,
                          activebackground=findOpt(widget, style, styles, 'activebackground', conf.get(widget)),
                          bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                          bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                          command=conf.get(widget).get('command'),
                          cursor=conf.get(widget).get('cursor'),
                          disabledbackground=findOpt(widget, style, styles, 'disabledbackground', conf.get(widget)),
                          disabledforeground=findOpt(widget, style, styles, 'disabledforeground', conf.get(widget)),
                          font=findOpt(widget, style, styles, 'font', conf.get(widget)),
                          fg=findOpt(widget, style, styles, 'fg', conf.get(widget)),
                          from_ = conf.get(widget).get('from_'),
                          justify=findOpt(wid, style, styles, 'justify', conf.get(widget)),
                          relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                          repeatdelay=conf.get(widget).get('repeatdelay'),
                          repeatinterval=conf.get(widget).get('repeatinterval'),
                          state=widgets.get(widget).get('state'),
                          textvariable=conf.get(widget).get('textvariable'),
                          to=conf.get(widget).get('to'),
                          validate=conf.get(widget).get('validate'),
                          validatecommand=conf.get(widget).get('validatecommand'),
                          values=conf.get(widget).get('values'),
                          vcmd=conf.get(widget).get('vcmd'),
                          width=conf.get(widget).get('width'),
                          wrap=conf.get(widget).get('wrap'),
                          xscrollcommand=conf.get(widget).get('xscrollcommand')
                          )

        elif widget == 'panedwindow':
            new = PanedWindow(master,
                              bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                              bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                              borderwidth=conf.get(widget).get('borderwidth'),
                              cursor=conf.get(widget).get('cursor'),
                              handlepad=conf.get(widget).get('handlepad'),
                              handlesize=conf.get(widget).get('handlesize'),
                              height=conf.get(widget).get('height'),
                              orient=conf.get(widget).get('orient'),
                              relief=findOpt(widget, style, styles, 'relief', conf.get(widget)),
                              sashcursor=conf.get(widget).get('sashcursor'),
                              sashrelief=findOpt(widget, style, styles, 'sashrelief', conf.get(widget)),
                              sashwidth=conf.get(widget).get('sashwidth'),
                              showhandle=conf.get(widget).get('showhandle'),
                              width=conf.get(widget).get('width')
                              )

        elif widget == 'labelframe':
            new = LabelFrame(master,
                             bg=findOpt(widget, style, styles, 'bg', conf.get(widget)),
                             bd=findOpt(widget, style, styles, 'bd', conf.get(widget)),
                             cursor=conf.get(widget).get('cursor'),
                             font=conf.get(widget).get('font'),
                             height=conf.get(widget).get('height'),
                             labelAnchor=conf.get(widget).get('labelAnchor'),
                             highlightbackground=findOpt(widget, style, styles, 'highlightbackground', conf.get(widget)),
                             highlightcolor=findOpt(widget, style, styles, 'highlightcolor', conf.get(widget)),
                             highlightthickness=findOpt(widget, style, styles, 'highlightthickness', conf.get(widget)),
                             relief=findOpt(widget, style, styles, 'relief'),
                             text=conf.get(widget).get('text'),
                             width=conf.get(widget).get('width')
                             )

        createWidget(new, conf) # once the widget is defined we just create it
        #print(widget)
        retWidgets.append(new) # and add it to the list of returned objects in case we want to change it later.

    if not Master:
        mainWindow.resizable(False, False) # you can set this to true but I like my windows non-resizable.

        return ([mainWindow, style], retWidgets, retVars) # return our values: the window (and style with it), the widgets, and any variables set up with them (widgetOBJECT:variable)

    if Master:
        return ([Master, style], retWidgets, retVars)

def matchType(inObj=None, targetType=None): # this function checks if any input object type matches a desired type. returns a boolean for match, the type of the object given, and the target type
    return [type(inObj) == targetType, type(inObj), targetType]

def add_greeter(index, offsetX=0, offsetY=0): # function used during setup to add a greeter.
    clear = True
    name = WIDGETS[-2][index].get()
    P = True
    for char in name: # check every character for non-alphanumeric characters. 
        if not char.isalnum():
            if char == '_': # the only exception is _ because twitch allows it idk why
                pass
            else:
                P = False
                break
    if not P:
        newstuff = []
        for x in errs:
                
            if WIDGETS[-2][index] == x[1]:
                delAllErrors(errs, errs.index(x))
                    
            else:
                newstuff.append(x)
                    
        exec("errs=newstuff")
        spawnErrorText('Only alphanumeric characters are permitted', [WIDGETS[-2][index].winfo_x()+offsetX, WIDGETS[-2][index].winfo_y()+offsetY], errs, WIDGETS[-2][index])
        clear = False

    if len(WIDGETS[-2][index].get()) == 0:
        clear = False
        newstuff = []
        
        for x in errs:
            
            if WIDGETS[-2][index] == x[1]:
                delAllErrors(errs, errs.index(x))
                
            else:
                newstuff.append(x)
                
        exec("errs=newstuff")
        spawnErrorText('Can\'t add blank item.', [WIDGETS[-2][index].winfo_x()+offsetX, WIDGETS[-2][index].winfo_y()+offsetY], errs, WIDGETS[-2][index])

    if clear == True: # if we passed the previous checks...
        
        if not WIDGETS[-2][index].get() in greeters: # add the greeter and delete any errors related to this step
            greeters.append(WIDGETS[-2][index].get().lower())
            WIDGETS[-2][index].delete(0,END)
            WIDGETS[1][13].set_menu(WIDGETS[-1][0][0].get(), *greeters)
            newstuff = []
            for x in errs:
                if WIDGETS[-2][index] == x[1]:
                    delAllErrors(errs, errs.index(x))
                else:
                    newstuff.append(x)
            exec("errs=newstuff")
            
        else: # don't add the same greeter multiple times
            spawnErrorText('Greeter already in list.', [WIDGETS[-2][index].winfo_x()+offsetX, WIDGETS[-2][index].winfo_y()+offsetY], errs, WIDGETS[-2][index])
            print([WIDGETS[-2][index].winfo_x(), WIDGETS[-2][index].winfo_y()])

def spawnErrorText(txt=None, loc=[], IDList=None, relateTo=None, source=None): # this spawns error text at the provided location.
    typeTXT = matchType(txt, str)
    if not typeTXT[0]:
        raise TypeError(f"Value provided for arg <txt> is {typeTXT[1]}, required {typeTXT[2]}")

    typeLoc = matchType(loc, list)
    if not typeLoc[0]:
        raise TypeError(f"Value provided for arg <loc> is {typeLoc[1]}, required {typeLoc[2]}")

    if len(loc) != 2:
        raise IndexError(f"spawnErrorText requires a list with length 2 (posX, posY). Length given: {len(loc)}")

    if source:
        WIDGETS = source
    else:
        WIDGETS = None
    newError=Label(text=txt,
                   fg='red',
                   bg=findOpt('label', WIDGETS[0][1], styles, 'bg'),
                   bd=findOpt('label', WIDGETS[0][1], styles, 'bd'),
                   font=findOpt('label', WIDGETS[0][1], styles, 'font'),
                   justify=findOpt('label', WIDGETS[0][1], styles, 'justify'),
                   padx=findOpt('label', WIDGETS[0][1], styles, 'padx'),
                   pady=findOpt('label', WIDGETS[0][1], styles, 'pady'),
                   relief=findOpt('label', WIDGETS[0][1], styles, 'relief'))
    newError.place(x=loc[0], y=loc[1])

    if IDList:
        typeIDL = matchType(IDList, list)
        if not typeIDL[0]:
            raise IndexError(f"Value provided for arg <IDList> is {typeIDL[1]}, required {typeIDL[2]}")

        IDList.append([newError, relateTo])

        return IDList

def delAllErrors(ErrorMessageList=[], specificIndex=None): # this removes all errors no matter what they're related to.
    typeERR = matchType(ErrorMessageList, list)
    if not typeERR:
        raise TypeError(f"Type of ErrorMessageList ({typeERR[1]}) does not match required type: {typeERR[2]}")

    if specificIndex != None:
        ErrorMessageList[specificIndex][0].destroy()
        return True
    #
    else:
        if len(ErrorMessageList) > 0:
            for item in ErrorMessageList:
                item[0].destroy()
            return []

def refreshOpts(opts, varList): # this refreshes the options for the button provided.
    
    for button in opts.get("buttons"):
        if type(button) == ttk.OptionMenu:
            for var, parent in varList:
                if parent == button:
                    button.set_menu(var.get(), *opts.get('source').get().split(' '))

    opts.get('source').delete(0,END)

def openLink(url): # this opens any link. yeah pretty self-explanatory
    if sys.platform == 'win32':
        webbrowser.open(url)
    elif sys.platform == 'linux':
        os.system(f'xdg-open {url}') # apparently linux dislikes the webbrowser lib, so we open it with a command instead.
        
def setBlacklistButton(initiator, blacklist): # test is just a dummy value for lambda: to work

    bList = blacklist

    initiator.set_menu(['Blacklist'][0], *bList)

def addToBlacklist(source=None, List=None, errList=None, SRC=None, INIT=None, reset=False): # adds a new entry to the blacklisted words

    if reset:
        setBlacklistButton(INIT, List)
    else:
        if not source.get() in List and len(source.get()) > 0:
            cont = True
            count = 0
            asd = len(source.get())
            errs = errList
            WIDGETS = SRC
            for x in source.get().split(' '):
                if len(x) == 0:
                    count += 1
                    print(count, asd)

            if count >= asd:
                cont = False
                newstuff = []
                for x in errs:
                    if WIDGETS[1][WIDGETS[1].index(source)] == x[1]:
                        delAllErrors(errs, errs.index(x))
                    else:
                        newstuff.append(x)

                exec("errs=newstuff")
                spawnErrorText('Spaces only can\'t be\nblacklisted', [source.winfo_x()+15, source.winfo_y()+20], errs, source, SRC)

            if cont == True:
                List.append(source.get())
                setBlacklistButton(INIT, List)
                newstuff = []
                for x in errs:
                    if WIDGETS[1][WIDGETS[1].index(source)] == x[1]:
                        delAllErrors(errs, errs.index(x))
                    else:
                        newstuff.append(x)

                WIDGETS[1][WIDGETS[1].index(source)].delete(0,END)

                exec("errs=newstuff")

        else:
            errs = errList
            WIDGETS = SRC
            newstuff = []
            for x in errs:
                if WIDGETS[1][WIDGETS[1].index(source)] == x[1]:
                    delAllErrors(errs, errs.index(x))
                else:
                    newstuff.append(x)

            exec("errs=newstuff")
            
            if source.get() in List:
                spawnErrorText('Already in blacklist', [source.winfo_x()+20, source.winfo_y()+30], errs, source, SRC)

            elif len(source.get()) == 0:
                spawnErrorText('Can\'t add blank to list', [source.winfo_x()+15, source.winfo_y()+30], errs, source, SRC)

class ToolTip(object): # tooltips are here

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text, offsetX, offsetY):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + offsetX
        y = y + cy + self.widget.winfo_rooty() + offsetY
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text, offsets=[0, 0]): # creates a tooltip with a specified offset.
    toolTip = ToolTip(widget)
    stillHovered = False
    import time
    def enter(event):
        toolTip.showtip(text, offsets[0], offsets[1])
    def leave(event):
        stillHovered = False
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

#all settings related code is found here.
class settings():
    
    def Load(file=None): #this load notifies the user and writes to debug...
        print(f"LOAD GOT: {file}")
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
                        copy_env = open(file, 'rb').read()
                        os.remove(".env.bkp")
                    except:
                        pass
                                    
                    os.rename(".env", ".env.bkp")
                    debug.write("\n|---- > Renamed default environmental file |> .env -> .env.bkp", False)
                        
                else:
                    debug.write("Attempting settings load from file specified: " + str(new_file), False)
                try:
                    #try:
                    #    os.mkdir('Counter-Bot Instances')
                    #except:
                    #    pass
                    #os.chdir('Counter-Bot Instances')
                    #try:
                    #    CBInstances = 0
                    #    while 1:
                    #        try:
                    #            os.mkdir(f'Inst-{CBInstances}')
                    #            os.chdir(f'Inst-{CBInstances}')
                    #            break
                    #        except:
                    #            CBInstances += 1
                    paste_env = open(".env", 'wb')
                    paste_env.write(copy_env)
                    paste_env.close()
                    dotenv.load_dotenv()
                except FileNotFoundError:
                    print("not found")


            try:

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


        customFile = file != None

        try:
            data = LoadEnv(customFile, file)
        except Exception as e:
            print(str(e))
            input()

        return data

    def silentLoad(): #... and this one doesn't.

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

    def LOADNEWENV(override=None):

        def find_setting(setting_name=None, stream=None):
            setting_to_return = None

            all_settings = stream

            for setting in all_settings:
                if setting_name in setting:
                    setting_to_return = setting.split('=')[1]
                    break

            return setting_to_return

        if override:
            a=override
        else:
            a='.env'

        asd = open(a, 'r').read().split('\n')

        Settings = {'TKN':find_setting('TKN', asd),
                    'CHNS':find_setting('CHNS', asd)
                    }

        return Settings

    def profileLoad(path_to_profile=None, noInst=False):
        print("LOADING PROFILES")
        if path_to_profile:
            
            def find_setting(setting_name=None, path=None):
                if path:
                    all_settings = open(path, 'r').read().split('\n')
                    setting_to_return = None

                    for setting in all_settings:
                        if setting_name in setting:
                            setting_to_return = setting.split('=')[1]
                            break

                    return setting_to_return

            if not noInst:

                if INSTANCE == "NONESET":
                    print("CREATING INSTANCE")
                
                    try:
                        os.mkdir('Counter-Bot Instances')
                    except FileExistsError:
                        pass
                    
                    counter = 0
                    
                    while 1:
                        try:
                            os.mkdir(f'Counter-Bot Instances\\Inst{counter}')
                            exec("global INSTANCE\nINSTANCE = counter")
                            break
                        except FileExistsError:
                            counter += 1

                else:
                    counter = INSTANCE

                oldFile = open(path_to_profile, 'rb')
                oldData = oldFile.read()
                oldFile.close()

                channelName = find_setting('CHANNEL', path_to_profile)

                newPath = os.getcwd()+f'\\Counter-Bot Instances\\Inst{counter}'

                newFile = open(newPath+f'\\{channelName}.pf', 'wb')
                newFile.write(oldData)
                newFile.close()

                newPath = newPath+f'\\{channelName}.pf'

            else:
                newPath = path_to_profile

            channel = find_setting("CHANNEL", newPath)
            bot_cap = find_setting("BOT_CAP", newPath)
            blacklist = find_setting("AUTO_BLACKLIST", newPath)
            blacklisted_words = find_setting("BLACKLISTED_WORDS", newPath)
            greeter = find_setting("GREETER_NAME", newPath)
            username_index = find_setting("GREETER_INDEX", newPath)
            welcome_marker = find_setting("WELCOME_MARKER", newPath)
            follow_time = find_setting("FOLLOWERS_TIME", newPath)

            if not all([channel, bot_cap, blacklist, blacklisted_words, greeter, username_index, welcome_marker, follow_time]):
                raise Exception("Invalid or incomplete profile provided.")
                        
            Settings = {"Channel": channel,
                        "Bot Follow Cap": bot_cap,
                        "Auto-Blacklist Bot Spam": blacklist,
                        "Blacklisted Words/Phrases": blacklisted_words,
                        "Bot to Read Welcome From": greeter,
                        "Username Index in Welcome": username_index,
                        "Welcome Marker Word": welcome_marker,
                        "Follower Only Time Upon Bot Trigger": follow_time,
                        "Path To Instance": newPath,
                        "Path To Source": path_to_profile
                        }

            return Settings
    
greeters=['nightbot', 'streamlabs', 'streamelements']

#create a setup to write initial env variables. can be re-triggered as needed.

#Check for updates

VERSION = '2.1.19'
devVersion = 'beta (oct. 30)'

latestVersion = get('https://github.com/16-ATLAS-16/Twitch-Counter-Bot/releases/latest').url.split('/tag/')[1].split('v')[1]
print(latestVersion)

def selfCheck(osPath):
    if "Previous Versions" in osPath:
        tempCounter = 0
        for subdir in osPath.split('\\'):
            tempCounter += 1

        tempCounter -= osPath.split('\\').index('Previous Versions')
        
        for x in range(tempCounter):
            os.chdir('../')

        fileVersion = None
        
        for filename in os.listdir(os.curdir):
            if 'Counter-Bot' in filename:
                fileVersion = filename.split('v')[1].split('-')[0]

        if fileVersion:
            return True

        else:
            return False

    else:
        return False
        

def update(): # this is responsible for updating the bot.
    import struct
    osBitVersion = struct.calcsize('P')*8 # gets the OS supported architecture

    PATH = f'https://github.com/16-ATLAS-16/Twitch-Counter-Bot/releases/download/v{latestVersion}/Counter-Bot-v{latestVersion}-x{osBitVersion}.zip' # construct download path
    print(PATH) #debug
    print("https://github.com/16-ATLAS-16/Twitch-Counter-Bot/releases/download/v2.1.0/Counter-Bot-v2.1.0-x64.zip") # debug
    
    updatedFile = get(f'https://github.com/16-ATLAS-16/Twitch-Counter-Bot/releases/download/v{latestVersion}/Counter-Bot-v{latestVersion}-x{osBitVersion}.zip') # this could be replaced with path but if it ain't broke don't fix it
    print(updatedFile) # debug
    updatedZip = open(f'Counter-Bot v{latestVersion}.zip', 'wb') # create a new file and open it
    updatedZip.write(updatedFile.content) # write the response

    import zipfile
    try:
        os.mkdir("Previous Versions") # try to make a directory to store previous versions in
    except FileExistsError:
        pass # but if it already exists we can just move on

    try:
        os.mkdir(f"Previous Versions/{VERSION}") # try making a directory for the current version (self-archiving i guess?)
    except FileExistsError:
        pass # if it exists we don't make nothing

    if sys.platform == 'win32':
        os.rename(f'{pathToSelf}/Counter-Bot-v{VERSION}-x{osBitVersion}.exe', f'{pathToSelf}/Previous Versions/{VERSION}/Counter-Bot-v{VERSION}-x{osBitVersion}.exe') # windows gets .exe files
    else:
        os.rename(f'{pathToSelf}/Counter-Bot-v{VERSION}-{sys.platform.lower()}.py', f'{pathToSelf}/Previous Versions/{VERSION}/Counter-Bot-v{VERSION}-{sys.platform.lower()}.py') # but I'm not sure about other platforms. linux for sure doesn't really have a file format specifically for executing things so...
    os.rename(f'{pathToSelf}/LICENCE.md', f'{pathToSelf}/Previous Versions/{VERSION}/LICENCE.md') # move
    os.rename(f'{pathToSelf}/README.md', f'{pathToSelf}/Previous Versions/{VERSION}/README.md') # every
    os.rename(f'{pathToSelf}/Help.txt', f'{pathToSelf}/Previous Versions/{VERSION}/Help.txt') # file
    os.rename(f'{pathToSelf}/CHANGELOG.txt', f'{pathToSelf}/Previous Versions/{VERSION}/CHANGELOG.txt')
    fileToUnpack = zipfile.ZipFile(f'Counter-Bot v{latestVersion}.zip') # set the zipfile reference
    fileToUnpack.extractall(pathToSelf) # extract all from archive to the current directory
    if sys.platform == 'win32':
        fileToStart = [f'Counter-Bot-v{latestVersion}-x{osBitVersion}.exe']
    else:
        fileToStart = [f'python{sys.version_info[0]}.{sys.version_info[1]}', f'Counter-Bot-v{latestVersion}-{sys.platform.lower}.py']
    subprocess.Popen(fileToStart)
    sys.exit()
    #https://github.com/16-ATLAS-16/Twitch-Counter-Bot/releases/download/v2.1.1/Counter-Bot-v2.1.0-x64.zip

if latestVersion > VERSION and selfCheck(os.getcwd()) == False:
    if sys.platform == 'win32':
        WIDGETS = initialize({'name':'Update Available', 'geometry':'470x100'}, 'dark', [
                            {'label':{
                                'font':('TkDefaultFont', 18),
                                'placemode':'place',
                                'fg':'white',
                                'pos':{'x':25, 'y':20},
                                'text':f'Version {latestVersion} is Available. Download?'
                                }},
                            {'button':{
                                'fg':'black',
                                'bg':'green',
                                'text':'Yes',
                                'placemode':'place',
                                'pos':{'x':25, 'y':60},
                                'width':20,
                                'command':update
                                }},
                            {'button':{
                                'fg':'black',
                                'bg':'red',
                                'text':'No',
                                'placemode':'place',
                                'pos':{'x':290, 'y':60},
                                'width':20
                                }}
                            ])
    else:
        WIDGETS = initialize({'name':'Update Available', 'geometry':'500x100'}, 'dark', [
                    {'label':{
                        'font':('TkDefaultFont', 18),
                        'placemode':'place',
                        'fg':'white',
                        'pos':{'x':25, 'y':20},
                        'text':'Version '+str(latestVersion)+' is Available. Download?'
                        }},
                    {'button':{
                        'fg':'black',
                        'bg':'green',
                        'text':'Yes',
                        'placemode':'place',
                        'pos':{'x':25, 'y':60},
                        'width':20,
                        'command':update
                        }},
                    {'button':{
                        'fg':'black',
                        'bg':'red',
                        'text':'No',
                        'placemode':'place',
                        'pos':{'x':290, 'y':60},
                        'width':20
                        }}
                    ])
    WIDGETS[0][0].protocol("WM_DELETE_WINDOW", sys.exit)
    createToolTip(WIDGETS[1][1], 'Download the latest update.\nMay take up to a minute.', [0, 30])
    createToolTip(WIDGETS[1][2], 'Skip downloading the latest update.\nContinue running this version.', [0, 30])
    WIDGETS[1][2].configure(command=WIDGETS[0][0].destroy)

    WIDGETS[0][0].mainloop()
        
#INITIAL SETUP CODE FOR FIRST TIME RUN
try:
    a = open(".env", 'r')
    a.close()
except FileNotFoundError:
    while 1:
        try:
            global TEMPORARY
            TEMPORARY = None
            def chooseFile3():
                filetypes = (
                    ('Environment Variables Files', '*.txt'),
                    ('Environment Variables Files', '*.env'),
                    ('Environment Variable Backups', '*.bkp')
                )

                filenames = fd.askopenfilenames(
                    title='Select a settings file',
                    initialdir=os.getcwd(),
                    filetypes=filetypes)

                selfPath = os.getcwd().replace('\\', '/')
                exec('global TEMPORARY\nTEMPORARY=filenames')

            def CPF(): # So uhm... I may or may not have fucked something up and had to solve it by copying and pasting functions and giving them minor changes. This will be cleaned up later but for now I need to get this version released as I'm busy but still want to help yall
                errs = []
                bList = []
                ERRS = []

                def add_g(index, offsetX=0, offsetY=0): # function used during setup to add a greeter.
                    clear = True
                    name = WIDGETS[-2][index].get()
                    P = True
                    for char in name: # check every character for non-alphanumeric characters. 
                        if not char.isalnum():
                            if char == '_': # the only exception is _ because twitch allows it idk why
                                pass
                            else:
                                P = False
                                break
                    if not P:
                        newstuff = []
                        for x in errs:
                                
                            if WIDGETS[-2][index] == x[1]:
                                delAllErrors(errs, errs.index(x))
                                    
                            else:
                                newstuff.append(x)
                                    
                        exec("errs=newstuff")
                        spawnError('Only alphanumeric characters are permitted', [WIDGETS[-2][index].winfo_x()+offsetX, WIDGETS[-2][index].winfo_y()+offsetY], errs, WIDGETS[-2][index], WIDGETS[0][0])
                        clear = False

                    if len(WIDGETS[-2][index].get()) == 0:
                        clear = False
                        newstuff = []
                        
                        for x in errs:
                            
                            if WIDGETS[-2][index] == x[1]:
                                delAllErrors(errs, errs.index(x))
                                
                            else:
                                newstuff.append(x)
                                
                        exec("errs=newstuff")
                        spawnError('Can\'t add blank item.', [WIDGETS[-2][index].winfo_x()+offsetX, WIDGETS[-2][index].winfo_y()+offsetY], errs, WIDGETS[-2][index], WIDGETS[0][0])

                    if clear == True: # if we passed the previous checks...
                        
                        if not WIDGETS[-2][index].get() in greeters: # add the greeter and delete any errors related to this step
                            greeters.append(WIDGETS[-2][index].get().lower())
                            WIDGETS[-2][index].delete(0,END)
                            WIDGETS[1][10].set_menu(WIDGETS[-1][0][0].get(), *greeters)
                            newstuff = []
                            for x in errs:
                                if WIDGETS[-2][index] == x[1]:
                                    delAllErrors(errs, errs.index(x))
                                else:
                                    newstuff.append(x)
                            exec("errs=newstuff")
                            
                        else: # don't add the same greeter multiple times
                            spawnError('Greeter already in list.', [WIDGETS[-2][index].winfo_x()+offsetX, WIDGETS[-2][index].winfo_y()+offsetY], errs, WIDGETS[-2][index], WIDGETS[0][0])
                            #print([WIDGETS[-2][index].winfo_x(), WIDGETS[-2][index].winfo_y()])
                            
                def spawnError(T, coords, errors, associate, root):

                    X = coords[0]
                    Y = coords[1]

                    #print(errs)
                    #input()
                    
                    a=Label(master=root, fg='red', text=T, bg='#323232')
                    a.place(x=X, y=Y)
                    #ERR[0][0].after(0, ERR[0][0].quit())
                    #ERR[0][0].mainloop()
                    errors.append([a, associate])
                    ERRS.append(a)

                def writePROFILE(*args):
                    import time
                    spawnError(2,100,'my ass',WIDS[0][0])
                    #for x in errs:
                    #    x.destroy()

                def reset():
                    errs = []

                def cancel(source):

                    for widget in source[1]:
                        widget.destroy()

                    for widget in ERRS:
                        widget.destroy()
                        
                    for widget in range(len(WIDS[1])):
                        #print(places, places[widget])
                        wid = WIDS[1][widget]
                        wid.place(x=places[widget][0], y=places[widget][1])

                def addToBlacklist(source=None, List=None, errList=None, SRC=None, INIT=None, reset=False): # adds a new entry to the blacklisted words

                    if reset:
                        setBlacklistButton(INIT, List)
                    else:
                        if not source.get() in List and len(source.get()) > 0:
                            cont = True
                            count = 0
                            asd = len(source.get())
                            errs = errList
                            WIDGETS = SRC
                            for x in source.get().split(' '):
                                if len(x) == 0:
                                    count += 1
                                    print(count, asd)

                            if count >= asd:
                                cont = False
                                newstuff = []
                                for x in errs:
                                    if WIDGETS[1][WIDGETS[1].index(source)] == x[1]:
                                        delAllErrors(errs, errs.index(x))
                                    else:
                                        newstuff.append(x)

                                exec("errs=newstuff")
                                spawnError('Spaces only can\'t be\nblacklisted', [source.winfo_x()+15, source.winfo_y()+20], errs, source, SRC[0][0])

                            if cont == True:
                                List.append(source.get())
                                setBlacklistButton(INIT, List)
                                newstuff = []
                                for x in errs:
                                    if WIDGETS[1][WIDGETS[1].index(source)] == x[1]:
                                        delAllErrors(errs, errs.index(x))
                                    else:
                                        newstuff.append(x)

                                WIDGETS[1][WIDGETS[1].index(source)].delete(0,END)

                                exec("errs=newstuff")

                        else:
                            errs = errList
                            WIDGETS = SRC
                            newstuff = []
                            for x in errs:
                                if WIDGETS[1][WIDGETS[1].index(source)] == x[1]:
                                    delAllErrors(errs, errs.index(x))
                                else:
                                    newstuff.append(x)

                            exec("errs=newstuff")
                            
                            if source.get() in List:
                                spawnError('Already in blacklist', [source.winfo_x()+20, source.winfo_y()+30], errs, source, SRC[0][0])

                            elif len(source.get()) == 0:
                                spawnError('Can\'t add blank to list', [source.winfo_x()+15, source.winfo_y()+30], errs, source, SRC[0][0])

                def BEGIN(ERR): # this function ends the setup
                    a=WIDGETS[1][1] # entry (channel name)
                    b=WIDGETS[1][3] # entry (follow only time)
                    d=WIDGETS[1][7] # entry (bot cap)
                    e=WIDGETS[1][10] # optionMenu
                    f=WIDGETS[1][16] # optionMenu
                    g=WIDGETS[1][18] # optionMenu
                    h=WIDGETS[1][5] # boolButton

                    newstuff = []
                    rem = []
                    errs = ERR
                    for x in ERRS:
                        x.destroy()
##                        if a == x[1] or b == x[1] or d == x[1] or e == x[1] or f == x[1] or g == x[1]:
##                            print("YEP")
##                            rem.append(x)
##                            x[0].destroy()
##                        else:
##                            print("NOPE")
##                            newstuff.append(x)
##                            print("AS", newstuff)
##                    print(newstuff)
##                    reset()
                    
                    
                    exec("global errs\nerrs = newstuff")
                    #print(errs)

                    allgood = True

                    if len(a.get()) == 0:
                        allgood = False
                        spawnError('Can\'t leave blank', [a.winfo_x()+14, a.winfo_y()+19], errs, a, WIDGETS[0][0])

                    for char in a.get():
                        if not char.isalnum():
                            if char == '_':
                                pass
                            else:
                                allgood = False
                                spawnError('Only alphanumeric characters are permitted.', [a.winfo_x()-115, a.winfo_y()+19], errs, a, WIDGETS[0][0])
                                break

                    if len(b.get()) == 0:
                        allgood = False
                        spawnError('Can\'t leave blank', [b.winfo_x()+14, b.winfo_y()+19], errs, b, WIDGETS[0][0])

                    elif len(b.get()) > 0:

                        try:
                            int(b.get())
                        except ValueError:
                            allgood = False
                            spawnError('Only integers are permitted.', [b.winfo_x()-25, b.winfo_y()+19], errs, b, WIDGETS[0][0])

                    if len(d.get()) == 0:
                        allgood = False
                        spawnError('Can\'t leave blank', [d.winfo_x()+14, d.winfo_y()+19], errs, d, WIDGETS[0][0])

                    elif len(d.get()) > 0:

                        try:
                            int(d.get())
                        except ValueError:
                            allgood = False
                            spawnError('Only integers are permitted.', [d.winfo_x()-25, d.winfo_y()+19], errs, d, WIDGETS[0][0])

                    for var, owner in WIDGETS[-1]:
                        if owner == f:
                            if len(var.get()) == 0:
                                allgood = False
                                spawnError('Can\'t leave blank', [f.winfo_x()+14, f.winfo_y()+24], errs, f, WIDGETS[0][0])
                        if owner == g:
                            if len(var.get()) == 0:
                                allgood = False
                                spawnError('Can\'t leave blank', [g.winfo_x()+14, g.winfo_y()+24], errs, g, WIDGETS[0][0])

                    if allgood == True:
                        #print("ALL OPTS GOOD")
                        channel = a.get()
                        duration = int(b.get())
                        
                        botcap = int(d.get())
                        for var, owner in WIDGETS[-1]:
                            if owner == e:
                                greeter = var.get()
                                break
                        for var, owner in WIDGETS[-1]:
                            if owner == f:
                                tempList = []
                                for x in range(f['menu'].index('end')+1):
                                    tempList.append(f['menu'].entrycget(x, 'label'))
                                word_index = tempList.index(var.get())
                                break
                        for var, owner in WIDGETS[-1]:
                            if owner == g:
                                welcome_marker = var.get()
                                break
                        blacklist = h.value
                        blacklisted_phrases = bList

                        #print([channel, botcap, blacklist, blacklisted_phrases, greeter, word_index, welcome_marker, duration, tkn])

                        writePF([channel, botcap, blacklist, blacklisted_phrases, greeter, word_index, welcome_marker, duration])

                        for widget in WIDGETS[1]:
                            widget.destroy()

                        for widget in range(len(WIDS[1])):
                            #print(places, places[widget])
                            wid = WIDS[1][widget]
                            wid.place(x=places[widget][0], y=places[widget][1])
                        
                    
                places=[]
                for x in WIDS[1]:
                    places.append((x.winfo_x(), x.winfo_y()))
                    x.place(x=10000000, y=10000000)
                WIDGETS = initialize(style='dark', Master=WIDS[0][0], widgets=[
                {'label':{
                    'text':'Twitch Name:',
                    'placemode':'place',
                    'pos':{'x':20,'y':8}
                    }},
                {'entry':{
                    'placemode':'place',
                    'pos':{'x':120,'y':10}
                    }},
                {'label':{
                    'text':'Followers-Only Time:',
                    'placemode':'place',
                    'pos':{'x':0,'y':48}
                    }},
                {'entry':{
                    'placemode':'place',
                    'pos':{'x':120,'y':50}
                    }},
                {'label':{
                    'text':'Blacklist bot spam phrases?',
                    'placemode':'place',
                    'pos':{'x':2,'y':90}
                    }},
                {'boolButton':{
                    'states':{'off':{'text':'off','bg':'red','fg':'black'},
                              'on':{'text':'on','bg':'green','fg':'black'}},
                    'placemode':'place',
                    'pos':{'x':160,'y':88},
                    'defaultValue':True
                    }},
                {'label':{
                    'text':'# of bot follows to trigger:',
                    'placemode':'place',
                    'pos':{'x':280,'y':8}
                    }},
                {'entry':{
                    'width':20,
                    'placemode':'place',
                    'pos':{'x':440,'y':10}
                    }},
                {'label':{
                    'placemode':'place',
                    'pos':{'x':280, 'y':58},
                    'text':'Select and add a greeter:'
                    }},
                {'entry':{
                    'placemode':'place',
                    'pos':{'x':440, 'y':100}
                    }},
                {'optionMenu':{
                    'placemode':'place',
                    'pos':{'x':440,'y':58},
                    'values':greeters,
                    'default':greeters[0],
                    'width':124,
                    'height':24
                    }},
                {'button':{
                    'placemode':'place',
                    'pos':{'x':280,'y':96},
                    'text':'Add Greeter',
                    'width':20,
                    'command': lambda: add_g(9, -140, 22)
                    }},
                {'label':{
                    'text':'Paste follower greeting message here:',
                    'placemode':'place',
                    'pos':{'x':280, 'y':140}
                    }},
                {'entry':{
                    'width':35,
                    'placemode':'place',
                    'pos':{'x':280, 'y':160}
                    }},
                {'button':{
                    'placemode':'place',
                    'pos':{'x':500, 'y':158},
                    'text':'Refresh Options',
                    'command':lambda: refreshOpts({'buttons':[WIDGETS[1][16], WIDGETS[1][18]],
                                                   'source':WIDGETS[1][13]},
                                                  WIDGETS[-1])
                    }},
                {'label':{
                    'text':'Word containing follower name:',
                    'placemode':'place',
                    'pos':{'x':280, 'y':200}
                    }},
                {'optionMenu':{
                    'placemode':'place',
                    'pos':{'x':460, 'y':200},
                    'values':[],
                    'default':[],
                    'width':134,
                    'height':24
                    }},
                {'label':{
                    'placemode':'place',
                    'pos':{'x':280, 'y':250},
                    'text':'Follow event distinguishing word:'
                    }},
                {'optionMenu':{
                    'placemode':'place',
                    'pos':{'x':470, 'y':250},
                    'values':[],
                    'default':[],
                    'width':124,
                    'height':24
                    }},
                {'entry':{
                    'placemode':'place',
                    'pos':{'x':2, 'y':122},
                    'width':24
                    }},
                {'button':{
                    'text':'Add to Blacklist',
                    'placemode':'place',
                    'pos':{'x':160, 'y':120},
                    'command':lambda: addToBlacklist(WIDGETS[1][19], bList, errs, WIDGETS, WIDGETS[1][21])
                    }},
                {'optionMenu':{
                    'placemode':'place',
                    'pos':{'x':160, 'y':150},
                    'values':['bigfollows'],
                    'default':['Blacklist'][0],
                    'width':93,
                    'height':24,
                    'command':lambda dummy: WIDGETS[1][21].set_menu(['Blacklist'][0], *bList)
                    }},
                {'button':{
                    'placemode':'place',
                    'pos':{'x':2, 'y':208},
                    'text':'All Set! Create Profile!',
                    'width':20,
                    'command':lambda: BEGIN(errs)#lambda: writePROFILE(WIDGETS[1][1], WIDGETS[1][3], WIDGETS[1][7], WIDGETS[1][10], WIDGETS[1][16], WIDGETS[1][18], WIDGETS[1][5], WIDGETS)
                    }},
                {'button':{
                    'text':'Cancel',
                    'bg':'red',
                    'fg':'black',
                    'placemode':'place',
                    'pos':{'x':160, 'y':208},
                    'width':8,
                    'command':lambda: cancel(WIDGETS)
                    }}
                ])

                errs = []
                bList = []
                WIDGETS[1][3].insert(END, '10')
                WIDGETS[1][7].insert(END, '20')
                #WIDGETS[0][0].mainloop()

            def spawnError(T, coords, errors, associate, root):

                    X = coords[0]
                    Y = coords[1]

                    #print(errs)
                    #input()
                    
                    a=Label(master=root, fg='red', text=T, bg='#323232')
                    a.place(x=X, y=Y)
                    #ERR[0][0].after(0, ERR[0][0].quit())
                    #ERR[0][0].mainloop()
                    errors.append([a, associate])
                    ERRS.append(a)

            SECRETS = {}

            def loadChannels(target):

                filetypes = (
                    ('Channel Profiles', '*.pf'),
                    ('Channel Profiles', '*.pf')
                )

                files = fd.askopenfilenames(title='Load Channels',
                                            initialdir=os.getcwd(),
                                            filetypes=filetypes)

                
                for profile in files:
                    try:
                        sett = settings.profileLoad(profile, True)
                        a=target.get(0, END)
                        if sett['Channel'] not in a:
                            target.insert(END, sett['Channel'])
                            SECRETS.update({sett['Channel']:sett})

                    except Exception as e:
                        print(e)

            
            def getSelection(target):
                PFS = []

                selected = target.curselection()

                sel = []
                for x in selected:
                    sel.append(target.get(x))
                    PFS.append(SECRETS[target.get(x)])

                return PFS, sel

            def STARTITALL():

                a=WIDS[1][4]
                b=WIDS[1][8]
                allgood = True

                for x in ERRS:
                    x.destroy()

                if len(a.get()) == 0:
                    spawnError('Cannot leave blank', [a.winfo_x()+130, a.winfo_y()+20], errs, a, WIDS[0][0])
                    allgood = False

                else:
                    
                    try:
                        if len(a.get().split('/')[3].split('=')[1].split('&')[0]) != 30:
                            allgood = False
                            spawnError('Invalid URL provided', [a.winfo_x()+130, a.winfo_y()+20], errs, a, WIDS[0][0])
                    except IndexError:
                        allgood = False
                        spawnError('Invalid URL provided', [a.winfo_x()+130, a.winfo_y()+20], errs, a, WIDS[0][0])

                if len(b.curselection()) == 0:
                    spawnError('Must Select at least 1 Profile', [210, 256], errs, b, WIDS[0][0])
                    allgood = False

                if allgood:
                    tkn = a.get().split('/')[3].split('=')[1].split('&')[0]
                    setts, chns = getSelection(WIDS[1][8])
                    LIST = []
                    for x in setts:
                        LIST.append(x['Path To Source'])

                    asd = open('.env', 'w')
                    asd.write(f'TKN={tkn}\nCHNS={LIST}')
                    asd.close()
                    WIDS[0][0].destroy()
            
            if sys.platform == 'win32':
                WIDS = initialize({'name':f'Twitch Counter-Bot v{VERSION} - Setup', 'geometry':'600x340'}, 'dark', [
                    {'label':{'text':'Step 1: Create a profile\n(can create multiple for other channels too)',
                              'placemode':'place',
                              'pos':{'x':2, 'y':5}
                              }
                     },
                    {'button':{'text':'Create Profile',
                               'placemode':'place',
                               'pos':{'x':260, 'y':10},
                               'command':CPF,
                               'width':14
                               }
                     },
                    {'label':{'text':'Step 2: Obtain a token\n(paste the redirect link into the field below)',
                              'placemode':'place',
                              'pos':{'x':2, 'y':40}
                              }
                     },
                    {'button':{
                              'text':'Get token link',
                              'command':lambda: openLink('https://id.twitch.tv/oauth2/authorize?client_id=7583ak4tqsqbnpbdoypfpg2h0ie4tu&redirect_uri=http://localhost&response_type=token+id_token&scope=openid+channel:read:editors+moderator:manage:automod+channel:read:hype_train+channel:read:polls+channel:read:predictions+channel:read:redemptions+channel:read:subscriptions+moderation:read+user:edit+user:read:broadcast+user:read:email+user:read:follows+user:read:subscriptions+channel:moderate+chat:edit+chat:read+whispers:read+whispers:edit+channel:manage:polls'),
                              'placemode':'place',
                              'pos':{'x':260,'y':45},
                              'width':14
                              }
                     },
                    {'entry':{
                              'width':60,
                              'pos':{'x':2,'y':80},
                              'placemode':'place',
                              'show':'*'
                              }
                     },
                    {'label':{
                              'text':'Step 3: Load Profiles\n(this will be made easier in the future)',
                              'placemode':'place',
                              'pos':{'x':2, 'y':120}
                              }
                     },
                    {'button':{
                              'text':'Load Profiles',
                              'placemode':'place',
                              'pos':{'x':260, 'y':125},
                              'width':14,
                              'command':lambda: loadChannels(WIDS[1][8])
                              }
                     },
                    {'frame':{
                        'placemode':'place',
                        'pos':{'x':2, 'y':160}
                        }
                     },
                    {'listbox':{
                        'master':{'widgetIndex':7},
                        'placemode':'pack',
                        'side':LEFT,
                        'bg':'#484848',
                        'fg':'white',
                        'bd':0,
                        'relief':FLAT,
                        'selectmode':EXTENDED,
                        'width':30
                        }
                     },
                    {'scrollbar':{
                        'master':{'widgetIndex':7},
                        'placemode':'pack',
                        'side':LEFT,
                        'ipady':56,
                        }
                     },
                    {'label':{
                        'text':'Step 4: Select Profiles (left)\n(used as default, can be changed later)\nCLICK = Select (single)',
                        'fg':'white',
                        'placemode':'place',
                        'pos':{'x':210, 'y':160},
                        'justify':LEFT
                        }
                     },
                    {'label':{
                        'text':'SHIFT CLICK = Select (multiple, all between selection 1 and 2)',
                        'fg':'orange', ##03fc90
                        'placemode':'place',
                        'pos':{'x':210, 'y':210}
                        }
                     },
                    {'label':{
                        'text':'CTRL CLICK = Select (preserve selection/multiple select) | Deselect',
                        'fg':'#03fc90',
                        'placemode':'place',
                        'pos':{'x':210, 'y':230}
                        }
                     },
                    {'label':{
                        'text':'Yeah, the UI is a mess. Will fix\nin the full release.',
                        'fg':'white',
                        'placemode':'place',
                        'pos':{'x':260, 'y':290}
                        }
                     },
                    {'button':{
                        'text':'All Set, Start Bot!',
                        'placemode':'place',
                        'pos':{'x':480, 'y':290},
                        'command':STARTITALL, #lambda: getSelection(WIDS[1][8]),
                        'bg':'green'
                        }
                     }


                    ]
                                  )
                def dead():
                    WIDS[0][0].destroy()
                    sys.exit()

                errs = []
                ERRS = []
                WIDS[1][8].configure(yscroll=WIDS[1][9].set)
                WIDS[1][9].configure(command=WIDS[1][8].yview)
                WIDS[0][0].protocol('WM_DELETE_WINDOW', dead)
                WIDS[0][0].mainloop()

            else:
                WIDS = initialize({'name':f'Twitch Counter-Bot v{VERSION} - Setup', 'geometry':'600x340'}, 'dark', [
                    {'label':{'text':'Step 1: Create a profile\n(can create multiple for other channels too)',
                              'placemode':'place',
                              'pos':{'x':2, 'y':5}
                              }
                     },
                    {'button':{'text':'Create Profile',
                               'placemode':'place',
                               'pos':{'x':260, 'y':10},
                               'command':CPF,
                               'width':14
                               }
                     },
                    {'label':{'text':'Step 2: Obtain a token\n(paste the redirect link into the field below)',
                              'placemode':'place',
                              'pos':{'x':2, 'y':40}
                              }
                     },
                    {'button':{
                              'text':'Get token link',
                              'command':lambda: openLink('https://id.twitch.tv/oauth2/authorize?client_id=7583ak4tqsqbnpbdoypfpg2h0ie4tu&redirect_uri=http://localhost&response_type=token+id_token&scope=openid+channel:read:editors+moderator:manage:automod+channel:read:hype_train+channel:read:polls+channel:read:predictions+channel:read:redemptions+channel:read:subscriptions+moderation:read+user:edit+user:read:broadcast+user:read:email+user:read:follows+user:read:subscriptions+channel:moderate+chat:edit+chat:read+whispers:read+whispers:edit+channel:manage:polls'),
                              'placemode':'place',
                              'pos':{'x':260,'y':45},
                              'width':14
                              }
                     },
                    {'entry':{
                              'width':60,
                              'pos':{'x':2,'y':80},
                              'placemode':'place',
                              'show':'*'
                              }
                     },
                    {'label':{
                              'text':'Step 3: Load Profiles\n(this will be made easier in the future)',
                              'placemode':'place',
                              'pos':{'x':2, 'y':120}
                              }
                     },
                    {'button':{
                              'text':'Load Profiles',
                              'placemode':'place',
                              'pos':{'x':260, 'y':125},
                              'width':14,
                              'command':lambda: loadChannels(WIDS[1][8])
                              }
                     },
                    {'frame':{
                        'placemode':'place',
                        'pos':{'x':2, 'y':160}
                        }
                     },
                    {'listbox':{
                        'master':{'widgetIndex':7},
                        'placemode':'pack',
                        'side':LEFT,
                        'bg':'#484848',
                        'fg':'white',
                        'bd':0,
                        'relief':FLAT,
                        'selectmode':EXTENDED,
                        'width':30
                        }
                     },
                    {'scrollbar':{
                        'master':{'widgetIndex':7},
                        'placemode':'pack',
                        'side':LEFT,
                        'ipady':56,
                        }
                     },
                    {'label':{
                        'text':'Step 4: Select Profiles (left)\n(used as default, can be changed later)\nCLICK = Select (single)',
                        'fg':'white',
                        'placemode':'place',
                        'pos':{'x':210, 'y':160},
                        'justify':LEFT
                        }
                     },
                    {'label':{
                        'text':'SHIFT CLICK = Select (multiple, all between selection 1 and 2)',
                        'fg':'orange', ##03fc90
                        'placemode':'place',
                        'pos':{'x':210, 'y':210}
                        }
                     },
                    {'label':{
                        'text':'CTRL CLICK = Select (preserve selection/multiple select) | Deselect',
                        'fg':'#03fc90',
                        'placemode':'place',
                        'pos':{'x':210, 'y':230}
                        }
                     },
                    {'label':{
                        'text':'Yeah, the UI is a mess. Will fix\nin the full release.',
                        'fg':'white',
                        'placemode':'place',
                        'pos':{'x':260, 'y':290}
                        }
                     },
                    {'button':{
                        'text':'All Set, Start Bot!',
                        'placemode':'place',
                        'pos':{'x':480, 'y':290},
                        'command':STARTITALL, #lambda: getSelection(WIDS[1][8]),
                        'bg':'green'
                        }
                     }


                    ]
                                  )
                def dead():
                    WIDS[0][0].destroy()
                    sys.exit()

                errs = []
                ERRS = []
                WIDS[1][8].configure(yscroll=WIDS[1][9].set)
                WIDS[1][9].configure(command=WIDS[1][8].yview)
                WIDS[0][0].protocol('WM_DELETE_WINDOW', dead)
                WIDS[0][0].mainloop()
                
##            else:
##                WIDGETS = initialize({f'name':'Twitch Counter-Bot v{VERSION} - Setup', 'geometry':'700x400'}, 'dark', [
##                {'label':{
##                    'text':'Twitch Name:',
##                    'placemode':'place',
##                    'pos':{'x':20,'y':8}
##                    }},
##                {'entry':{
##                    'placemode':'place',
##                    'pos':{'x':140,'y':10}
##                    }},
##                {'label':{
##                    'text':'Followers-Only Time:',
##                    'placemode':'place',
##                    'pos':{'x':0,'y':48}
##                    }},
##                {'entry':{
##                    'placemode':'place',
##                    'pos':{'x':140,'y':50}
##                    }},
##                {'button':{
##                    'text':'Get token link',
##                    'command':lambda: openLink('https://id.twitch.tv/oauth2/authorize?client_id=7583ak4tqsqbnpbdoypfpg2h0ie4tu&redirect_uri=http://localhost&response_type=token+id_token&scope=openid+channel:read:editors+moderator:manage:automod+channel:read:hype_train+channel:read:polls+channel:read:predictions+channel:read:redemptions+channel:read:subscriptions+moderation:read+user:edit+user:read:broadcast+user:read:email+user:read:follows+user:read:subscriptions+channel:moderate+chat:edit+chat:read+whispers:read+whispers:edit+channel:manage:polls'),
##                    'placemode':'place',
##                    'pos':{'x':2,'y':98},
##                    'width':14
##                    }},
##                {'label':{
##                    'text':'Paste redirect URL here:',
##                    'placemode':'place',
##                    'pos':{'x':145,'y':100}
##                    }},
##                {'entry':{
##                    'width':37,
##                    'pos':{'x':2,'y':125},
##                    'placemode':'place'}},
##                {'label':{
##                    'text':'Blacklist bot spam phrases?',
##                    'placemode':'place',
##                    'pos':{'x':2,'y':170}
##                    }},
##                {'boolButton':{
##                    'states':{'off':{'text':'off','bg':'red','fg':'black'},
##                              'on':{'text':'on','bg':'green','fg':'black'}},
##                    'placemode':'place',
##                    'pos':{'x':180,'y':168},
##                    'defaultValue':True
##                    }},
##                {'label':{
##                    'text':'# of bot follows to trigger:',
##                    'placemode':'place',
##                    'pos':{'x':320,'y':8}
##                    }},
##                {'entry':{
##                    'width':20,
##                    'placemode':'place',
##                    'pos':{'x':500,'y':10}
##                    }},
##                {'label':{
##                    'placemode':'place',
##                    'pos':{'x':320, 'y':51},
##                    'text':'Select and add a greeter:'
##                    }},
##                {'entry':{
##                    'placemode':'place',
##                    'pos':{'x':500, 'y':100}
##                    }},
##                {'optionMenu':{
##                    'placemode':'place',
##                    'pos':{'x':500,'y':51},
##                    'values':greeters,
##                    'default':greeters[0],
##                    'width':124,
##                    'height':24
##                    }},
##                {'button':{
##                    'placemode':'place',
##                    'pos':{'x':320,'y':96},
##                    'text':'Add Greeter',
##                    'width':16,
##                    'command': lambda: add_greeter(12, -140, 22)
##                    }},
##                {'label':{
##                    'text':'Paste follower greeting message here:',
##                    'placemode':'place',
##                    'pos':{'x':320, 'y':140}
##                    }},
##                {'entry':{
##                    'width':30,
##                    'placemode':'place',
##                    'pos':{'x':320, 'y':160}
##                    }},
##                {'button':{
##                    'placemode':'place',
##                    'pos':{'x':570, 'y':158},
##                    'text':'Refresh Options',
##                    'command':lambda: refreshOpts({'buttons':[WIDGETS[1][19], WIDGETS[1][21]],
##                                                   'source':WIDGETS[1][16]},
##                                                  WIDGETS[-1])
##                    }},
##                {'label':{
##                    'text':'Word containing follower name:',
##                    'placemode':'place',
##                    'pos':{'x':320, 'y':200}
##                    }},
##                {'optionMenu':{
##                    'placemode':'place',
##                    'pos':{'x':540, 'y':200},
##                    'values':[],
##                    'default':[],
##                    'width':134,
##                    'height':24
##                    }},
##                {'label':{
##                    'placemode':'place',
##                    'pos':{'x':320, 'y':250},
##                    'text':'Follow event distinguishing word:'
##                    }},
##                {'optionMenu':{
##                    'placemode':'place',
##                    'pos':{'x':540, 'y':250},
##                    'values':[],
##                    'default':[],
##                    'width':124,
##                    'height':24
##                    }},
##                {'entry':{
##                    'placemode':'place',
##                    'pos':{'x':2, 'y':202},
##                    'width':21
##                    }},
##                {'button':{
##                    'text':'Add to Blacklist',
##                    'placemode':'place',
##                    'pos':{'x':180, 'y':200},
##                    'command':lambda: addToBlacklist(WIDGETS[1][22], bList)
##                    }},
##                {'optionMenu':{
##                    'placemode':'place',
##                    'pos':{'x':180, 'y':230},
##                    'values':['bigfollows'],
##                    'default':['Blacklist'][0],
##                    'width':93,
##                    'height':24,
##                    'command':setBlacklistButton
##                    }},
##                {'button':{
##                    'placemode':'place',
##                    'pos':{'x':2, 'y':268},
##                    'text':'All Set! Start Bot!',
##                    'width':20,
##                    'command':startBot
##                    }}
##                ])
##            errs = []
##            bList = []
##            WIDS[0][0].protocol("WM_DELETE_WINDOW", sys.exit)
##            WIDS[-2][10].delete(0,END)
##            WIDGETS[-2][10].insert(0,'20')
##            WIDGETS[-2][3].delete(0,END)
##            WIDGETS[-2][3].insert(0,'10')
##            WIDGETS[0][0].mainloop()
            break
        except Exception as e:
            print(str(e))

global INSTANCE
INSTANCE = "NONESET"
 

# set up the bot
        
class Bot(commands.Bot):

    def __init__(self, textfield=None, botfield=None, bannedfield=None, window=None, settingsFile=None, dummyFileInput=None, root=None, profiles=[], tkn=None):
        self.counter = 0
        self.botlist = []
        self.safelist=[]
        self.streamerID = None

##        self.Settings = settings.Load(settingsFile) # load base settings. key names are the same as what's written to debug for the sake of not having to re-write the return value (yes I'm lazy in that way)
##        self.channelToJoin = self.Settings.get("Channel")
##        self.bot_cap = int(self.Settings.get("Bot Follow Cap"))
##        self.blacklist = bool(self.Settings.get("Auto-Blacklist Bot Spam"))
##        self.blacklisted_words = eval(self.Settings.get("Blacklisted Words/Phrases"))
##        self.greeter_name = self.Settings.get("Bot to Read Welcome From")
##        self.user_index = int(self.Settings.get("Username Index in Welcome"))
##        self.welcome_marker = self.Settings.get("Welcome Marker Word")
##        self.follow_duration = self.Settings.get("Follower Only Time Upon Bot Trigger")
        self.client_id="udejckrsxv14xdt43ut43sto8wc5c4"
        self.token = tkn
        self.scrollToBottom = True
        self.tempBlacklist = []
        self.checkedAccs = []
        
        self.streamerID = None
        #self.prevage=['0 dummy', '0 age']
        #self.prevprevage=['0 dummy', '0 age']
        #self.prevuser=''
        #self.prevprevuser=''
        #self.prevmsg=''
        #self.prevprevmsg=''
        self.PASS = False
        #self.iteratingBots = False
        #self.checkList = []
        self.reqRemoves = []
        self.CHN = ''
        self.agreed = []
        self.pendingSync = ''

        self.HIGHLIGHTS = {
            'info':{'foreground':'#4286f4'},
            'warning':{'foreground':'orange'},
            'alert':{'foreground':'red'},
            'command':{'background':'white', 'foreground':'black'},
            'setting change':{'background':'#00ffa2', 'foreground':'orange'},
            'check':{'foreground':'#00ffa2'},
            'sync add':{'background':'#ff8b00', 'foreground':'black'},
            'sync go':{'background':'#00ff00', 'foreground':'black'},
            'sync fail':{'background':'#ff4400', 'foreground':'black'},
            'critical fail':{'background':'red', 'foreground':'white'}
            }
        
        #self.TEXTFIELD = textfield
        #self.TEXTFIELD.configure(state='normal')
        #self.TEXTFIELD.insert(END, f'\nChatlog: Chat will appear here once you hit "Start Bot"')
        #self.TEXTFIELD.configure(state=DISABLED)
        self.WINDOW = window
        self.BOTSFIELD = botfield
        self.BANNED = bannedfield
        self.settingsFile = settingsFile
        self.CHANNELS = {}
        self.POSITIONS = [(0, 60), (471, 95), (703, 95), (725, 60), (515, 60)]
        self.wids = [{'frame':{
               'placemode':'place',
               'pos':{'x':0, 'y':60}
               }},
           {'text':{
               'text':'test text',
               'fg':'white',
               'bg':'#161616',
               'placemode':'pack',
               'width':56,
               'height':21,
               'master':{'widgetIndex':0},
               'side':LEFT,
               'relief':'flat'
               }},
           {'scrollbar':{
               'placemode':'pack',
               'master':{'widgetIndex':0},
               'side':LEFT,
               'ipady':145,
               'ipadx':1,
               'bg':'#323232',
               'troughcolor':'#323232'
               }},
           {'frame':{
               'placemode':'place',
               'pos':{'x':471, 'y':95}
               }},
           {'text':{
               'text':'test text',
               'fg':'orange',
               'bg':'#161616',
               'placemode':'pack',
               'width':26,
               'height':19,
               'master':{'widgetIndex':3},
               'side':LEFT,
               'relief':'flat'
               }},
           {'scrollbar':{
               'placemode':'pack',
               'master':{'widgetIndex':3},
               'side':LEFT,
               'ipady':128,
               'ipadx':1,
               'bg':'#323232',
               'troughcolor':'#323232'
               }},
           {'frame':{
               'placemode':'place',
               'pos':{'x':703, 'y':95}
               }},
           {'text':{
               'text':'test text',
               'fg':'red',
               'bg':'#161616',
               'placemode':'pack',
               'width':26,
               'height':19,
               'master':{'widgetIndex':6},
               'side':LEFT,
               'relief':'flat',
               'bd':0
               }},
           {'scrollbar':{
               'placemode':'pack',
               'master':{'widgetIndex':6},
               'side':LEFT,
               'ipady':125,
               'ipadx':1,
               'bg':'#323232',
               'troughcolor':'#323232',
               'height':20
               }},
           {'label':{
               'placemode':'place',
               'pos':{'x':725, 'y':60},
               'text':'Banned Users/Bots:',
               'fg':'red',
               'font':('TkDefaultFont', 14)
               }},
           {'label':{
               'placemode':'place',
               'pos':{'x':515, 'y':60},
               'text':'Suspected Bots:',
               'fg':'orange',
               'font':('TkDefaultFont', 14)
               }}]
        self.JOINS = []
        for chn in profiles:
            profile = settings.profileLoad(chn)

            self.WIDSS = initialize(Master=root, style='dark', widgets=self.wids)
            
            self.WIDSS[1][1].configure(yscroll=self.WIDSS[1][2].set)
            self.WIDSS[1][2].configure(command=self.WIDSS[1][1].yview)
            self.WIDSS[1][4].configure(yscroll=self.WIDSS[1][5].set)
            self.WIDSS[1][5].configure(command=self.WIDSS[1][4].yview)
            self.WIDSS[1][7].configure(yscroll=self.WIDSS[1][8].set)
            self.WIDSS[1][8].configure(command=self.WIDSS[1][7].yview)
            
            self.CHANNELS.update({profile.get('Channel'): {'SETTINGS':profile,
                                                           'WIDGETS':self.WIDSS,
                                                           'HISTORY':('prevuser', 'prevprevuser', 'prevmsg', 'prevprevmsg', ['0 prev', '0 age'], ['0 prevprev', '0 age']),
                                                           'SYNCS':[],
                                                           'CHANNEL':None,
                                                           'CHID':None
                                                           }})
            self.JOINS.append(f'#{profile.get("Channel")}')

        def signal(self, a):
            self.change_channel(a[1][0], a)

        OPTS = initialize(Master=root, style='dark', widgets=[
            {'optionMenu':{
                'values':list(self.CHANNELS.keys()),
                'default':list(self.CHANNELS.keys())[-1],
                'placemode':'place',
                'pos':{'x':350, 'y':60},
                'command':lambda *args:self.change_channel(callingMenu=OPTS[1][0], widgetsList=OPTS)
                }}
             ]
            )

        self.SEL_CHANNEL = OPTS[-1][0][0]

        print(OPTS[1][0])

        print(self.CHANNELS)
        
        super().__init__(
    token=f"{self.token}",
    client_id="7583ak4tqsqbnpbdoypfpg2h0ie4tu",
    nick="crimsoneye16",
    prefix="<prefix goes here>",
    initial_channels=self.JOINS
)
            
        
        #print(self.settingsFile)

        for channel in self.CHANNELS:
            #print(channel)
            self.TEXTFIELD = self.CHANNELS.get(channel).get('WIDGETS')[1][1]
            self.TEXTFIELD.configure(state='normal')
            self.TEXTFIELD.insert(END, f'\nStarting Bot: Attempting Connection')
            self.TEXTFIELD.insert(END, f'\nBot Start: SUCCESS\nConnected to channel: {self.CHANNELS[channel]["SETTINGS"]["Channel"]}\nDEBUG: RAW SETTINGS : {self.CHANNELS[channel]["SETTINGS"]}')
            self.TEXTFIELD.insert(END, f'\n\n <====== CHAT LOG BEGINS HERE ======>\n')
            self.TEXTFIELD.configure(state=DISABLED)
            print(self.CHANNELS[channel])
            self.CHANNELS[channel].update({'BOTSBANS':[ [],[],[],[], 0, False, [] ]}) # BOTS, BANNED, CHECKED, CHECKLIST, COUNTER, ITERATING BOTS, REQUEST REMOVES (CHECKLIST)

            newThread = threading.Thread(target=lambda: self.userTick(channel), daemon=True)
            newThread.start()

            for highlight in self.HIGHLIGHTS:
                self.TEXTFIELD.tag_add(highlight, '0.0', '0.0')
                self.TEXTFIELD.tag_config(highlight,
                                          background=self.HIGHLIGHTS[highlight].get('background'),
                                          bgstipple=self.HIGHLIGHTS[highlight].get('bgstipple'),
                                          borderwidth=self.HIGHLIGHTS[highlight].get('borderwidth'),
                                          fgstipple=self.HIGHLIGHTS[highlight].get('fgstipple'),
                                          font=self.HIGHLIGHTS[highlight].get('font'),
                                          foreground=self.HIGHLIGHTS[highlight].get('foreground'),
                                          justify=self.HIGHLIGHTS[highlight].get('justify'),
                                          lmargin1=self.HIGHLIGHTS[highlight].get('lmargin1'),
                                          lmargin2=self.HIGHLIGHTS[highlight].get('lmargin2'),
                                          offset=self.HIGHLIGHTS[highlight].get('offset'),
                                          overstrike=self.HIGHLIGHTS[highlight].get('overstrike'),
                                          relief=self.HIGHLIGHTS[highlight].get('relief'),
                                          rmargin=self.HIGHLIGHTS[highlight].get('rmargin'),
                                          spacing1=self.HIGHLIGHTS[highlight].get('spacing1'),
                                          spacing2=self.HIGHLIGHTS[highlight].get('spacing2'),
                                          spacing3=self.HIGHLIGHTS[highlight].get('spacing3'),
                                          tabs=self.HIGHLIGHTS[highlight].get('tabs'),
                                          underline=self.HIGHLIGHTS[highlight].get('underline'),
                                          wrap=self.HIGHLIGHTS[highlight].get('wrap')
                                          )

        if dummyFileInput != None:
            
            FILE = open(dummyFileInput).readlines()

            for channel in self.CHANNELS:

                OBJ = self.CHANNELS[channel]
                BOTS = OBJ['BOTSBANS'][0]
                COUNTER = OBJ['BOTSBANS'][4]
                CHECKLIST = OBJ['BOTSBANS'][3]
                BOTSWINDOW = OBJ['WIDGETS'][1][4]
                
                for user in FILE:
                    
                    BOTS.append(f'{user.split(" ")[0]}')
                    COUNTER += 1
                    
                    print(f"{user} was added to list")

                BOTSWINDOW.configure(state='normal')
                for botuser in BOTS:
                    BOTSWINDOW.insert(END, f"{botuser}")
                    CHECKLIST.append({botuser:'inf'})

                BOTSWINDOW.configure(state=DISABLED)

        print(self.CHANNELS)

    def change_channel(self, callingMenu, widgetsList):

        targetVar = None

        print(callingMenu, widgetsList)

        for var, owner in widgetsList[-1]:
            if owner == callingMenu:
                targetVar = var
                break

        self.SEL_CHANNEL = targetVar

        #print("HI")

        if targetVar:
            for user in self.CHANNELS:
                wids = self.CHANNELS[user]['WIDGETS'][1]
                if user != targetVar.get():
                    wids[0].place(x=100000,y=100000)
                    wids[3].place(x=100000,y=100000)
                    wids[6].place(x=100000,y=100000)
                    wids[9].place(x=100000,y=100000)
                    wids[10].place(x=100000,y=100000)
                    
                else: 
                    wids[0].place(x=self.POSITIONS[0][0],y=self.POSITIONS[0][1])
                    wids[3].place(x=self.POSITIONS[1][0],y=self.POSITIONS[1][1])
                    wids[6].place(x=self.POSITIONS[2][0],y=self.POSITIONS[2][1])
                    wids[9].place(x=self.POSITIONS[3][0],y=self.POSITIONS[3][1])
                    wids[10].place(x=self.POSITIONS[4][0],y=self.POSITIONS[4][1])
                    
    def update_window(self):
        while True:
            try:
                self.WINDOW.update()
            except:
                break

    def updateScroll(self, value):
        self.scrollToBottom = value
        print(self.scrollToBottom)

    def banBotsFromFile(file):
        FILE = open(file).readlines()
        for user in FILE:
            self.checkList.append({user:'inf'})
            self.counter += 1

    async def TickUsers(self, CHN=None):
        print(f"HEY {CHN}")
        if CHN:
            removed = []
            while 1:
                try:
                    OBJ = self.CHANNELS[CHN]
                    BANWINDOW = OBJ['WIDGETS'][1][7]
                    BOTSWINDOW = OBJ['WIDGETS'][1][4]
                    MAINWINDOW = OBJ['WIDGETS'][1][1]
                    REQREMOVES = OBJ['BOTSBANS'][6]
                    BOTS = OBJ['BOTSBANS'][0]
                    #print(BOTS)
                    BANNED = OBJ['BOTSBANS'][1]
                    CHECKLIST = OBJ['BOTSBANS'][3]
                    #print((CHECKLIST, CHN))
                    newlist = []
                    pastList = self.CHANNELS[CHN].get('BOTSBANS')[0]
                    await asyncio.sleep(1)
                    #print(CHECKLIST, REQREMOVES)
                    
                    for user in CHECKLIST:
                        if list(user.keys())[0] in REQREMOVES:
                            try:
                                REQREMOVES.remove(list(user.keys())[0])
                            except:
                                pass
                            removed.append(list(user.keys())[0])
                            #print("HEY THIS IS IT ", removed)
                        
                        if list(user.keys())[0] not in removed:
                            time = user[list(user.keys())[0]]
                            if time != 'inf':
                                time -= 1
                                
                                if time > 0:
                                    newlist.append({list(user.keys())[0]:time})

                            else:
                                newlist.append(user)
                #            print(f"Added {user}")

                    tempL=[]    
                    for item in newlist:
                        #print(f"Added {list(item.keys())[0]}")
                        tempL.append(list(item.keys())[0])

                    OBJ['BOTSBANS'][0] = tempL
                    #print(OBJ['BOTSBANS'][0], BOTS)
                    BOTSWINDOW.configure(state='normal')
                    BOTSWINDOW.delete('1.0', END)
                    OBJ['BOTSBANS'][3] = newlist
                                        
                    for botuser in BOTS:
                        BOTSWINDOW.insert(END, f"\n{botuser}")

                    BOTSWINDOW.configure(state=DISABLED)
                except:
                    break

        if not CHN:
            print("YOU SUCK")

    def TickSync(self, CHN=None):
        if CHN:
            OBJ = self.CHANNELS[CHN.name]
            SYNCS = OBJ['SYNCS']

            new=[]

            for sync in SYNCS:
                initiator = sync[0]
                link = sync[1]
                timeLeft = sync[2]
                agreed = sync[3]

                if timeLeft > 0:
                    timeLeft -= 1

                    new.append((initiator, timeLeft))

            SYNCS = new
    
    def userTick(self, chann):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.TickUsers(chann))
            
    async def event_ready(self):
        print("good to go")
        #try:
        #    await self.get_channel(self.channelToJoin).send("Bot Ready!") <- optional and doesn't always work
        #except Exception as e:
        #    print(str(e))

        debug.write("====CHAT: LOG BEGIN====")

    async def reloadSettings(self):
        self.Settings = settings.silentLoad(settingsFile)
        self.channelToJoin = self.Settings.get("Channel")
        self.bot_cap = int(self.Settings.get("Bot Follow Cap"))
        self.blacklist = bool(self.Settings.get("Auto-Blacklist Bot Spam"))
        self.blacklisted_words = eval(self.Settings.get("Blacklisted Words/Phrases"))
        self.greeter_name = self.Settings.get("Bot to Read Welcome From")
        self.user_index = int(self.Settings.get("Username Index in Welcome"))
        self.welcome_marker = self.Settings.get("Welcome Marker Word")
        self.follow_duration = self.Settings.get("Follower Only Time Upon Bot Trigger")
        self.client_id="udejckrsxv14xdt43ut43sto8wc5c4"

    async def detectFollowBot(self, MESSAGE=None, DATA=None):
    
        if MESSAGE and MESSAGE != '..{BANALL}..':
            OBJ = self.CHANNELS[MESSAGE.channel.name]
            
        elif DATA:
            OBJ = self.CHANNELS[DATA[1].name]

        elif not DATA and MESSAGE == '..{BANALL}..':
            OBJ = self.CHANNELS[self.SEL_CHANNEL.get()]

        Settings = OBJ.get("SETTINGS")
        channelToJoin = Settings.get("Channel")
        bot_cap = int(Settings.get("Bot Follow Cap"))
        blacklist = bool(Settings.get("Auto-Blacklist Bot Spam"))
        blacklisted_words = eval(Settings.get("Blacklisted Words/Phrases"))
        greeter_name = Settings.get("Bot to Read Welcome From")
        user_index = int(Settings.get("Username Index in Welcome"))
        welcome_marker = Settings.get("Welcome Marker Word")
        follow_duration = Settings.get("Follower Only Time Upon Bot Trigger")

        BANWINDOW = OBJ['WIDGETS'][1][7]
        BOTSWINDOW = OBJ['WIDGETS'][1][4]
        MAINWINDOW = OBJ['WIDGETS'][1][1]
        BOTS = OBJ['BOTSBANS'][0]
        BANNED = OBJ['BOTSBANS'][1]
        CHECKED = OBJ['BOTSBANS'][2]
        CHECKLIST = OBJ['BOTSBANS'][3]
        COUNTER = OBJ['BOTSBANS'][4]
        ITER_BOTS = OBJ['BOTSBANS'][5]
        REQREMOVES = OBJ['BOTSBANS'][6]

        PREVUSER = OBJ['HISTORY'][0]
        PREVPREVUSER = OBJ['HISTORY'][1]
        PREVMSG = OBJ['HISTORY'][2]
        PREVPREVMSG = OBJ['HISTORY'][3]
        PREVAGE = OBJ['HISTORY'][4]
        PREVPREVAGE = OBJ['HISTORY'][5]

        CHID = OBJ['CHID']

        print("THREAD START")

        print(f'\nThere are {len(threading.enumerate())} threads running.')

        if DATA == None and MESSAGE != '..{BANALL}..':

            words = MESSAGE.content.split(' ')
            author = MESSAGE.author
            channel = MESSAGE.channel
            self.sendChannel = channel
                        #print(self.sendChannel)
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
                
            print("AND SO DOES THIS") # this is what happens when you do coding at midnight. imma leave it in for the laugh because I'll update the source code in a couple days anyways XD (turns out I never removed this. this is now an easter egg I guess lol)
            debug.write("~~~~User Follow Triggered~~~~") # yeah I've copy-pasted code to move it. I *am* rewriting it but it doesn't make me any less lazy XD

            user=words[int(user_index)]
            if '!' in user:
                user=user[:-1]

        elif DATA:
            user = DATA[0]
            channel = DATA[1]
            OBJ['CHANNEL'] = channel

        else:
            user = CHECKED[0]
            channel = OBJ['CHANNEL']

        if MESSAGE != '..{BANALL}..':

            print(user)
            cont = False

            if user not in CHECKED:
                
                while 1:
                    
                    RESP = get(f"https://decapi.me/twitch/accountage/{user}")
                    accAge = RESP.content.decode()
                    
                    print(f'User: {user} | RESP: {RESP.status_code}')
                    
                    if RESP.status_code == 200:
                        break
                    
                if accAge.split(' ')[-1] == 'unavailable' or accAge.split(' ')[-1] == 'found.':
                    
                    BOTS.append(user)
                    CHECKLIST.append({user:300})
                    COUNTER += 1
                    cont = True
                    
                if (accAge.split(' ')[-1] != 'unavailable' and accAge.split(' ')[-1] != 'found.') or cont:
                   
                    if accAge.split(' ')[-1] != 'unavailable' and accAge.split(' ')[-1] != 'found.':
                        
                        newList = accAge.split(',')
                        debug.write(f"| - > Username |> {user} | User Age |> {newList}", False)
                        curAge=newList
                        
                        print(f"============================> new follow {curAge}")
                        
                        MAINWINDOW.configure(state='normal')
                        MAINWINDOW.insert(END, f"\n<===== Account Seen =====>\nUsername: {user} | Account Age {accAge}", ('check'))
                        MAINWINDOW.configure(state=DISABLED)
                        
                    else:
                        
                        MAINWINDOW.configure(state='normal')
                        MAINWINDOW.insert(END, f"\n<===== Account Seen =====>\nUsername: {user} | Account Age <unavailable> (account suspended?)", ('check'))
                        MAINWINDOW.configure(state=DISABLED)
                        
                        debug.write(f"| - > Username |> {user} | User Age |> [UNAVAILABLE]", False)
                        curAge = None
                                

                                #print(f"{self.prevage}, {curAge}")
                    if curAge != None:
                                    
                        if curAge[0] == PREVAGE[0] and curAge[0] == PREVPREVAGE[0] and curAge[1].split(' ')[1] == PREVAGE[1].split(' ')[1] and curAge[1].split(' ')[1] == PREVPREVAGE[1].split(' ')[1]:
                                                
                            if user not in BOTS and user not in self.safelist:
                                
                                BOTS.append(user)
                                CHECKLIST.append({user:300})
                                
                                debug.write(f"| - > Added {user} to botlist, user will be banned on bot raid trigger.", False)
                                
                                COUNTER += 1
                                
                                MAINWINDOW.configure(state='normal')
                                MAINWINDOW.insert(END, f"\n > > > > Account age match detected. Added {user} to botlist, ban on raid trigger.", ('warning'))
                                MAINWINDOW.configure(state=DISABLED)
                                                
                            if PREVUSER not in BOTS and PREVUSER not in self.safelist:
                                
                                BOTS.append(PREVUSER)
                                CHECKLIST.append({PREVUSER:300})
                                
                                debug.write(f"| - > Added {PREVUSER} to botlist, user will be banned on bot raid trigger.", False)
                                
                                COUNTER += 1
                                
                                MAINWINDOW.configure(state='normal')
                                MAINWINDOW.insert(END, f"\n > > > > Added {PREVUSER} to botlist, ban on raid trigger.", ('warning'))
                                MAINWINDOW.configure(state=DISABLED)

                            if PREVPREVUSER not in BOTS and PREVPREVUSER not in self.safelist:
                                
                                BOTS.append(PREVPREVUSER)
                                CHECKLIST.append({PREVPREVUSER:300})
                                
                                debug.write(f"| - > Added {PREVPREVUSER} to botlist, user will be banned on bot raid trigger.", False)
                                
                                COUNTER += 1
                                
                                MAINWINDOW.configure(state='normal')
                                MAINWINDOW.insert(END, f"\n > > > > Added {PREVPREVUSER} to botlist, ban on raid trigger.", ('warning'))
                                MAINWINDOW.configure(state=DISABLED)

                            BOTSWINDOW.configure(state='normal')
                            BOTSWINDOW.delete('1.0', END)
                                        
                            for botuser in BOTS:
                                BOTSWINDOW.insert(END, f"\n{botuser}")

                            BOTSWINDOW.configure(state=DISABLED)

                        if PREVAGE != PREVPREVAGE and PREVAGE != None and PREVPREVAGE != None:
                            try:
                                BOTS.remove(f"{user}")
                                
                                for item in CHECKLIST:
                                    if list(item.keys())[0] == user:
                                        CHECKLIST.remove(CHECKLIST.index(item))
                                        
                                BOTSWINDOW.configure(state='normal')
                                BOTSWINDOW.delete('1.0', END)
                                                
                                for botuser in BOTS:
                                    BOTSWINDOW.insert(END, f"\n{botuser}")

                                BOTSWINDOW.configure(state=DISABLED)
                                            
                            except ValueError:
                                pass

                if len(BOTS) >= int(bot_cap) and ITER_BOTS == False:
                    ITER_BOTS = True
                    debug.write("<<<<BOT RAID DETECTED>>>>")
                                                    
                    await channel.send(f"/followers {follow_duration}")
                    debug.write(">> Enabled 10 minute Followers-Only Mode.", False)
                    await channel.send("/clear")
                    debug.write(">> Cleared Chat to remove any other messages.", False)
                    BANWINDOW.configure(state='normal')

                    async def ban(chn, user):
                        await chn.send(f'{user} should be banned but I am dumb')

                    await channel.send(f'BEGONE BOTS! Banning {len(BOTS)} bots')

                    templist = []
                    count = 1
                    AAAAAAA = len(BOTS)

                    while 1:
                        if len(BOTS) != 0:
                            print("ACTIVE")
                            try:
                                if count <= 10:
                                    UN = BOTS[0].split('\n')[0]
                                    asd = f'/ban {UN} bot follower'
                                    print(asd)
                                    await channel.send(asd)
                                    print(f"Banned {BOTS[0]}")
                                    debug.write(f">> BOT RAID: BANNED |> {BOTS[0]}", False)
                                    BANWINDOW.insert(END, f"\n{BOTS[0]}")
                                    templist.append(BOTS[0])
                                            
                                    for item in CHECKLIST:
                                        if list(item.keys())[0] == BOTS[0]:
                                            #print(f'Removing {item} from {self.checkList}')
                                            CHECKLIST.remove(item)
                                                    
                                    COUNTER -= 1
                                    count += 1
                                    REQREMOVES.append(BOTS[0])
                                    try:
                                        BOTS.remove(BOTS[0])
                                        CHECKLIST.remove(CHECKLIST[0])
                                    except:
                                        pass
                                                
                                    BOTSWINDOW.configure(state='normal')
                                    BOTSWINDOW.delete('1.0', END)
                                            
                                    for botuser in BOTS:
                                        if len(BOTS) <= 500:
                                            BOTSWINDOW.insert(END, f"\n{botuser}")

                                    BOTSWINDOW.configure(state=DISABLED)

                                    await asyncio.sleep(0.3)

                                else:
                                    await channel.send(f'{len(BOTS)} remain.')
                                    count = 1

                            except Exception as e:
                                print(str(e))
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                print(exc_tb.tb_lineno)
                                input()
                                await asyncio.sleep(1)
                        else:
                            try:
                                ITER_BOTS = False
                                await channel.send("/followersoff")
                                await channel.send(f'Done. Banned {AAAAAAA} bots.')
                                break
                            except:
                                pass
                                                
                    BANWINDOW.configure(state=DISABLED)
                    debug.write(">> Disabled Followers-Only Mode. Bot raid shut down.", False)

                if curAge != None:
                    PREVPREVAGE = PREVAGE
                    PREVAGE = curAge
                    PREVPREVUSER = PREVUSER
                    PREVUSER = user
                        
                print("THREAD END")
                        
                CHECKED.append(user)

            else:
                print(f'{user} already checked')

        else:
            print("TRIGGER")
            
            if ITER_BOTS == False:
                ITER_BOTS = True
                debug.write("<<<<BOT RAID DETECTED>>>>")
                                                        
                await channel.send(f"/followers {follow_duration}")
                debug.write(">> Enabled 10 minute Followers-Only Mode.", False)
                await channel.send("/clear")
                debug.write(">> Cleared Chat to remove any other messages.", False)
                BANWINDOW.configure(state='normal')

                async def ban(chn, user):
                    await chn.send(f'{user} should be banned but I am dumb')

                templist = []
                count = 1
                AAAAAAA = len(BOTS)

                await channel.send(f'BEGONE BOTS! Banning {len(BOTS)} bots')
                while 1:
                    if len(BOTS) != 0:
                        print("ACTIVE")
                        try:
                            if count <= 10:
                                UN = BOTS[0].split('\n')[0]
                                asd = f'/ban {UN} bot follower'
                                print(asd)
                                await channel.send(asd)
                                print(f"Banned {BOTS[0]}")
                                debug.write(f">> BOT RAID: BANNED |> {BOTS[0]}", False)
                                BANWINDOW.insert(END, f"\n{BOTS[0]}")
                                templist.append(BOTS[0])
                                count += 1 
                                                
                                for item in CHECKLIST:
                                    if list(item.keys())[0] == BOTS[0]:
                                        #print(f'Removing {item} from {self.checkList}')
                                        CHECKLIST.remove(item)
                                                        
                                COUNTER -= 1
                                REQREMOVES.append(BOTS[0])
                                try:
                                    BOTS.remove(BOTS[0])
                                    CHECKLIST.remove(CHECKLIST[0])
                                    print(CHECKLIST)
                                except:
                                    pass

                                await asyncio.sleep(0.33)

                            else:
                                count = 1
                                await channel.send(f"{len(BOTS)} remain.")
                                                
                            BOTSWINDOW.configure(state='normal')
                            BOTSWINDOW.delete('1.0', END)
                                            
                            for botuser in BOTS:
                                if len(BOTS) <= 500:
                                    BOTSWINDOW.insert(END, f"\n{botuser}")

                            BOTSWINDOW.configure(state=DISABLED)
                                            
                        except Exception as e:
                            print(str(e))
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            print(exc_tb.tb_lineno)
                            await asyncio.sleep(0.1)
                    else:
                        try:
                            self.iteratingBots = False
                            await channel.send("/followersoff")
                            await channel.send(f"Done. Banned {AAAAAAA} bots.")
                            break
                        except:
                            pass
                        
                print("THREAD END")
                BANWINDOW.configure(state=DISABLED)
                debug.write(">> Disabled Followers-Only Mode. Bot raid shut down.", False)
                        
            


    def detectBot(self, message=None, DATA=None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.detectFollowBot(message, DATA))

    async def pardon(self, users):
        while 1:
            if len(users) != 0:
                await self.CHN.send('/unban {users[0]}')
                await self.CHN.send('/unblock {users[0]}')
            else:
                break

    def Pardon(self, selection):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.pardon(selection))

    async def syncToGithub(self, link, MSG):
        print("1")
        # get(a.replace('github.com', 'raw.githubusercontent.com').replace('blob/', '')) <- github link to raw link
        if 'github.com' in link:
            link = link.replace('github.com', 'raw.githubusercontent.com').replace('blob/', '')

        resp = get(link)
        print(resp)

        names = resp.content.decode()
        print("GOT")
        CHN = MSG.channel
        OBJ = self.CHANNELS[CHN.name]
        BOTS = OBJ['BOTSBANS'][0]
        CHECKLIST = OBJ['BOTSBANS'][3]
        COUNTER = OBJ['BOTSBANS'][4]
        
        for name in names.split('\n'):
            if len(name) != 0 and name[0] != '#':
                BOTS.append(name.replace('\n', '').replace('\r', ''))
                CHECKLIST.append({name.replace('\n', '').replace('\r', ''):'inf'})
                COUNTER += 1

            
    #@bot.event
    async def event_message(self, ctx):
        print(ctx.channel.name)
        Settings = self.CHANNELS[ctx.channel.name]['SETTINGS'] # constantly updating settings via silent load allows for variables to be changed during runtime, however loading it before bot runs is crucial to make the bot run
        channelToJoin = Settings.get("Channel")
        bot_cap = int(Settings.get("Bot Follow Cap"))
        blacklist = bool(Settings.get("Auto-Blacklist Bot Spam"))
        blacklisted_words = eval(Settings.get("Blacklisted Words/Phrases"))
        greeter_name = Settings.get("Bot to Read Welcome From")
        user_index = int(Settings.get("Username Index in Welcome"))
        welcome_marker = Settings.get("Welcome Marker Word")
        follow_duration = Settings.get("Follower Only Time Upon Bot Trigger")

        OBJ = self.CHANNELS[ctx.channel.name]
        
        BANWINDOW = OBJ['WIDGETS'][1][7]
        BOTSWINDOW = OBJ['WIDGETS'][1][4]
        TEXTFIELD = OBJ['WIDGETS'][1][1]
        BOTS = OBJ['BOTSBANS'][0]
        BANNED = OBJ['BOTSBANS'][1]
        CHECKED = OBJ['BOTSBANS'][2]
        CHECKLIST = OBJ['BOTSBANS'][3]
        COUNTER = OBJ['BOTSBANS'][4]
        ITER_BOTS = OBJ['BOTSBANS'][5]

        PREVUSER = OBJ['HISTORY'][0]
        PREVPREVUSER = OBJ['HISTORY'][1]
        PREVMSG = OBJ['HISTORY'][2]
        PREVPREVMSG = OBJ['HISTORY'][3]
        PREVAGE = OBJ['HISTORY'][4]
        PREVPREVAGE = OBJ['HISTORY'][5]

        SYNCS = OBJ['SYNCS']
        CHID = OBJ['CHID']

        message = ctx
        words = message.content.split(' ')
        author = message.author
        channel = message.channel
        self.sendChannel = channel

        self.CHN = channel

        print(channel.name)
        
        #print(self.sendChannel)
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
            #print(words)
            #a=ctx.content.encode('unicode-escape').decode('unicode-escape')
            debug.write(f"{ctx.author.name}: {ctx.content}")
            TEXTFIELD.configure(state='normal')
            TEXTFIELD.insert(END, f"\n{ctx.author.name}: {ctx.content.encode('unicode-escape').decode('unicode-escape')}")
            TEXTFIELD.configure(state=DISABLED)
            if self.scrollToBottom == True:
                TEXTFIELD.yview_pickplace("end")
            
            
            if author.name in BOTS: # if any chatbot talks and they haven't been banned for whatever reason, silence them.
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

            if message.content[1:] in self.tempBlacklist:
                BOTS.append(user)
                CHECKLIST.append({user:300})
                COUNTER += 1
                TEXTFIELD.configure(state='normal')
                TEXTFIELD.insert(END, f"\n > > > > Spam Bot Account detected. Added {user} to botlist, ban on raid trigger.", ('warning'))
                TEXTFIELD.configure(state=DISABLED)
                BOTSWINDOW.configure(state='normal')
                BOTSWINDOW.delete('1.0', END)
                   
                for botuser in BOTS:
                    BOTSWINDOW.insert(END, f"\n{botuser}")

                BOTSWINDOW.configure(state=DISABLED)
            

            if len(words) > 1:
                self.PASS = len(words) == len(PREVMSG.split(' ')) and words[1:] == PREVMSG.split(' ')[1:] and words[1:] == PREVPREVMSG.split(' ')[1:] and author.name not in BOTS and author.name not in self.safelist

            if message.content == 'ab!amimod':
                await channel.send(f'{is_mod}')
                
            if is_welcome or self.PASS == True: # triggers on user follow. once twitchio has eventsub support this section will change, but until then I don't fancy writing code when I can just rely on other bots to detect follows. It was already a pain to work with the twitch API as is. #twitchdobetter

                #print("THIS TRIGGERS")
                if not is_welcome:
                    followFinder = threading.Thread(target=lambda: self.detectBot(DATA=(author.name,channel)), daemon=True, name="FOLLOWER ID")
                else:
                    if words[user_index][-1] in ['!', ',', '.', '?']:
                        N = words[user_index][:-1]
                    else:
                        N = words[user_index]
                    followFinder = threading.Thread(target=lambda: self.detectBot(DATA=(N,channel)), daemon=True, name="FOLLOWER ID")
                followFinder.start()

            if "ab!setFTime" == words[0] and is_streamer:
                if len(words) == 2:
                    try:
                        int(words[1])
                        f = channel.name
                        path = path = f"Counter-Bot Instances\\Inst{INSTANCE}\\{f}"
                        writeEnv([channelToJoin, bot_cap, blacklist, blacklisted_words, greeter_name, user_index, welcome_marker, words[1]], path)
                        await channel.send(f"Successfully set variable to: {words[1]}")
                        TEXTFIELD.configure(state='normal')
                        TEXTFIELD.insert(END, f'\nINVOKE {author.name}', ('command'))
                        TEXTFIELD.insert(END, f' invoked setFTime (Set Followers-Only Time)', ('info'))
                        TEXTFIELD.insert(END, f'\n - - - - - - - \nSettings updated:\n | - > Follower-Only Time: {follow_duration} > {words[1]}\n - - - - - - - ', ('setting change'))
                        TEXTFIELD.configure(state=DISABLED)
                        
                    except ValueError:
                        await channel.send("Usage: ab!setFTime {minutes (integer)}")

                else:
                    await channel.send("Usage: ab!setFTime {minutes (integer)}")

            if "ab!setCap" == words[0] and is_streamer:
                if len(words) == 2:
                    try:
                        int(words[1])
                        f = channel.name
                        path = path = f"Counter-Bot Instances\\Inst{INSTANCE}\\{f}"
                        writeEnv([channelToJoin, words[1], blacklist, blacklisted_words, greeter_name, user_index, welcome_marker, follow_duration], '.env')
                        await channel.send(f"Successfully set cap to: {words[1]}")
                        TEXTFIELD.configure(state='normal')
                        TEXTFIELD.insert(END, f'\nINVOKE {author.name}', ('command'))
                        TEXTFIELD.insert(END, f' invoked setCap (Set Bot Cap)', ('info'))
                        TEXTFIELD.insert(END, f'\n - - - - - - - \nSettings updated:\n | - > Bot Cap: {bot_cap} > {words[1]}\n - - - - - - - ', ('setting change'))
                        TEXTFIELD.configure(state=DISABLED)

                    except ValueError:
                        await channel.send("Usage: ab!setCap {trigger cap (integer)}")

                else:
                    await channel.send("Usage: ab!setCap {trigger cap (integer)}")

            if "ab!setGreeter" == words[0] and is_streamer:
                if len(words) == 4:
                    f = channel.name
                    path = path = f"Counter-Bot Instances\\Inst{INSTANCE}\\{f}"
                    writeEnv([channelToJoin, bot_cap, blacklist, blacklisted_words, words[1], words[2], words[3], follow_duration], path)
                    await channel.send(f"Successfully set greeter to {words[1]}, set username index to {words[2]}, and set follow event marker to {words[3]}")
                    TEXTFIELD.configure(state='normal')
                    TEXTFIELD.insert(END, f'\nINVOKE {author.name}', ('command'))
                    TEXTFIELD.insert(END, f' invoked setGreeter (Set Greeter and Greeter subsettings)', ('info'))
                    TEXTFIELD.insert(END, f'\n - - - - - - - \nSettings updated:\n | - > Greeter: {greeter_name} > {words[1]}\n | - > Username Index: {user_index} > {words[2]}\n | - > Welcome Marking Word: {welcome_marker} > {words[3]}\n - - - - - - - ', ('setting change'))
                    TEXTFIELD.configure(state=DISABLED)
                else:
                    await channel.send("Usage: ab!setGreeter {Bot/Greeter name (string)} {Username index (integer index) {Follow event marking word (string)}")
                    await channel.send("Do ab!varHelp for more.")

            if "ab!varHelp" == words[0] and is_streamer:
                await channel.send("Variable Types Help:")
                await channel.send("string: any characters you can type on a keyboard")
                await channel.send("integer: any whole number")
                await channel.send("(integer) index: integer used to determine a position in a list or dict, starts at 0 for first entry")
                await channel.send("bool: value of either true or false")
                TEXTFIELD.configure(state='normal')
                TEXTFIELD.insert(END, f'\nINVOKE {author.name}', ('command'))
                TEXTFIELD.insert(END, f' invoked varHelp (Variable Type Help Display)', ('info'))
                TEXTFIELD.configure(state=DISABLED)

            if ("ab!commands" == words[0] or "ab!help" == words[0]) and is_streamer:
                await channel.send("varHelp : Display variable types help (broadcaster only)")
                await channel.send("setGreeter : Updates follow trigger conditions (broadcaster only)")
                await channel.send("setCap : Sets the follow cap before anti-bot response is triggered (broadcaster only)")
                await channel.send("setFTime : Sets the follow only mode time in case of bot raid (broadcaster only)")
                await channel.send("commands : Displays this set of messages (broadcaster only)")
                await channel.send("help : Displays this set of messages (broadcaster only)")
                await channel.send("poll : Starts a poll. (moderator and above)")

            if "ab!poll" == words[0] and is_mod:
                arguments = message.content.split(',')
                if len(arguments) == 4 or len(arguments) == 5:
                    try:
                        title = arguments[0].split(' ')[1:]
                        choice_1 = arguments[1]
                        choice_2 = arguments[2]
                        dur = int(arguments[3])
                        if len(arguments) == 5:
                            votecost = int(arguments[4])
                        else:
                            votecost = 0

                        resp = post("https://api.twitch.tv/helix/polls", headers={"Authorization": f"Bearer {self.token}",
                                                                                 "Client-Id": f"{self.client_id}",
                                                                                 "Content-Type": "application/json"}, json={"broadcaster_id": f"{CHID}", "title": f"{title}", "choices": [{'title': choice_1}, {'title': choice_2}], "duration": dur})
                        print(resp)

                    except ValueError:
                        await channel.send("Usage: ab!poll {title (string)}, {choice 1 (string)}, {choice 2 (string)}, {duration (int)}, {channel point cost (int) [optional]}")

                else:
                    await channel.send("Usage: ab!poll {title (string)}, {choice 1 (string)}, {choice 2 (string)}, {duration (int)}, {channel point cost (int) [optional]}")

            if "ab!endpoll" == words[0] and is_mod:
                await channel.send('/endpoll')
                resp = get(f"https://api.twitch.tv/helix/polls?broadcaster_id={self.streamerID}", headers={'Authorization': f"Bearer {self.token}", 'Client-Id': f"{self.client_id}"})
                poll_id = resp.content.decode()[16:52]

                patch('https://api.twitch.tv/helix/polls', headers={"Authorization": f"Bearer {self.token}", "Client-Id": f"{self.client_id}", "Content-Type": "application/json"}, json={"broadcaster_id": f"{CHID}", "id": f"{poll_id}", "status": "TERMINATED"})

            if "ab!botFuncTest" == words[0] and is_creator:
                await channel.send("All systems functional, debug successful.")

            if "ping" == words[0] and is_creator:
                print("PONG")
                await channel.send("pong")

            if "ab!sync" == words[0] and (is_mod or is_streamer or is_creator):
                GO = True
                sel = None
                for sync in SYNCS:
                    if author.name in sync[0]:
                        GO = False
                        sel = sync
                        break
                
                print("TRIGGER")

                
                if is_creator or is_streamer:
                    await self.syncToGithub(words[1], message)

                else:
                    if GO:
                        await channel.send(f'{author.name} is attempting to sync to {words[1]}. This expires in 5 minutes. 3 Moderators (or the broadcaster) must approve this for it to sync by doing "ab!approve (initiator)" (0/3) | Use ab!syncList to view all available sync attempts')
                        OBJ['SYNCS'].append((author.name, words[1], 300, [author.name]))

                    if not GO:
                        await channel.send(f'{author.name} You already have an active sync attempt. It has {len(sel[3])}/3 approvals and will become invalid in {sel[2]} seconds. Use ab!syncCancel to cancel that sync attempt.')

            if "ab!syncCancel" == words[0]:

                sel = None
                for sync in SYNCS:
                    if author.name in sync[0]:
                        SYNCS.remove(sync)
                        sel = True
                        break

                if sel:
                    await channel.send("Sync has been cancelled successfully.")
                if not sel:
                    await channel.send("You have no ongoing sync attempts to cancel.")

            if "ab!approve" == words[0]:
                if len(words) > 1:
                    USR = words[1]

                else:
                    USR = None
                    
                AGREED = SYNCS
                sel = ''
                
                if USR:
                    for sync in SYNCS:
                        if sync[0] == USR:
                            sel = sync
                            break
                        
                    if is_streamer:
                        #print("TRUE") debug
                        while len(sel[3]) < 3:
                            sel[3].append(author.name)

                    else:
                        
                        if author.name not in sel[3] and author.name is not sel[0]:
                            
                            self.agreed.append(author.name)
                            await channel.send(f'{author.name} has approved of the sync! ({len(self.agreed)}/3)')
                            
                        else:
                            await channel.send(f'{author.name} you\'ve already approved of this sync. ({len(self.agreed)}/3)')

                    if len(sel[3]) >= 3:
                        await self.syncToGithub(sel[1], message)
                        await channel.send('Sync has been approved and processed.')

            if "JOIN" == words[0] and is_creator:
                await self.join_channels([f'#{words[1]}'])

            if "VERSION" == words[0] and is_creator:
                await channel.send(f'{VERSION} {devVersion}')

            if "TEST" == words[0]:

                TEXTFIELD.configure(state='normal')
                TEXTFIELD.insert(END, '\n')
                TEXTFIELD.insert(END, f'INVOKE |> {author.name}', ('command'))
                TEXTFIELD.insert(END, ' invoked TEST', ('info'))
                TEXTFIELD.configure(state=DISABLED)
                print(OBJ['CHID'])
                
            if blacklist == True:
                if author.name in BOTS and self.PASS:
                    self.tempBlacklist.append(message.content[1:])
                        
                    

            PREVPREVMSG=PREVMSG    
            PREVMSG=message.content
            OBJ['CHANNEL'] = channel
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            if AttributeError:
                print(f"Encountered error: {str(e)} at line {exc_tb.tb_lineno}")
                #raise(e)
                pass
            else:
                print(str(e))
                debug.write(f" |>|>|>|>|>|>|>|>|>|> Encountered error: {str(e)} at line {exc_tb.tb_lineno}", False)

    async def event_join(self, channel, user):
        #print("join event")
        print(f'{user} has joined')
        tempVal = await channel.user()
        OBJ = self.CHANNELS[channel.name]
        OBJ['CHID'] = tempVal.id
        followFinder = threading.Thread(target=lambda: self.detectBot(message=None, DATA=[user.name, channel]), daemon=True, name="FOLLOWER ID")
        followFinder.start()

    async def event_part(self, channel, user):
        print(f'{user.name} has parted')


global fail
fail=False

        

if __name__ == "__main__":
    while 1:
        try:
            if sys.platform == 'win32':
                WIDGETS = initialize({'name':f'Twitch Counter-Bot v{VERSION}', 'geometry':'940x400'}, 'dark', [
                {'label':{
                    'text':'Settings File: Default',
                    'placemode':'place',
                    'pos':{'x':210, 'y':17}
                    }},
                {'button':{
                    'text':'Override Settings',
                    'placemode':'place',
                    'pos':{'x':100, 'y':15}
                    }},
                {'label':{
                    'text':'Add Banlist',
                    'placemode':'place',
                    'pos':{'x':420, 'y':15}
                    }},
                {'button':{
                    'text':'Add Banlist',
                    'placemode':'place',
                    'pos':{'x':340, 'y':15}
                    }},
                {'button':{
                    'text':'Ban All',
                    'placemode':'place',
                    'pos':{'x':500, 'y':15}
                    }}
                ])
            else:
                WIDGETS = initialize({'name':f'Twitch Counter-Bot v{VERSION}', 'geometry':'840x400'}, 'dark', [
                {'label':{
                    'text':'Settings File: Default',
                    'placemode':'place',
                    'pos':{'x':210, 'y':17}
                    }},
                {'button':{
                    'text':'Override Settings',
                    'placemode':'place',
                    'pos':{'x':100, 'y':15}
                    }},
                {'label':{
                    'text':'Add Banlist',
                    'placemode':'place',
                    'pos':{'x':420, 'y':15}
                    }},
                {'button':{
                    'text':'Add Banlist',
                    'placemode':'place',
                    'pos':{'x':340, 'y':15}
                    }},
                {'button':{
                    'text':'Ban All',
                    'placemode':'place',
                    'pos':{'x':500, 'y':15}
                    }}
                ])
            global selFile
            selFile = None

            global dummyFile
            dummyFile = None

            global banFile
            banFile = None

            global ASD
            ASD = []

            def chooseFile(textWidget=None):
                filetypes = (
                    ('Environment Variables Files', '*.pf'),
                    ('Environment Variables Files', '*.pf'),
                    ('Environment Variable Backups', '*.pf')
                )

                filename = fd.askopenfilenames(
                    title='Select a settings file',
                    initialdir=os.getcwd(),
                    filetypes=filetypes)

                selfPath = os.getcwd().replace('\\', '/')
                qwe = []
                for x in filename:
                    qwe.append(x)
                if filename[0] == f'{selfPath}/.env':
                    filename = None

                if textWidget:
                    if filename:
                        textWidget['text'] = f'{len(qwe)} Overrides.'
                    else:
                        textWidget['text'] = f'No Overrides.'

                exec('global ASD\nASD = qwe')

            def chooseFile2(textWidget=None):
                filetypes = (
                    ('Environment Variables Files', '*.txt'),
                    ('Environment Variables Files', '*.env'),
                    ('Environment Variable Backups', '*.bkp')
                )

                filename = fd.askopenfilename(
                    title='Select a settings file',
                    initialdir=os.getcwd(),
                    filetypes=filetypes)

                selfPath = os.getcwd().replace('\\', '/')
                if filename == f'{selfPath}/.env':
                    filename = None

                if textWidget:
                    if filename:
                        textWidget['text'] = f'Settings File: {filename}'
                    else:
                        textWidget['text'] = f'Settings File: Default'

                exec('global dummyFile\ndummyFile = filename')

            def banAll(bot):
                followFinder = threading.Thread(target=lambda: bot.detectBot(message='..{BANALL}..'), daemon=True, name="FOLLOWER ID")
                followFinder.start()

            def chooseBanlist(textWidget=None):
                filetypes = (
                    ('Banlist Files', '*.txt'),
                    ('Banlist Files', '*.txt')
                )

                filename = fd.askopenfilename(
                    title='Select a settings file',
                    initialdir=os.getcwd(),
                    filetypes=filetypes)

                selfPath = os.getcwd().replace('\\', '/')
                if filename == f'{selfPath}/.env':
                    filename = None

                if textWidget:
                    if filename:
                        textWidget['text'] = f'Banlist File: {filename}'
                    else:
                        textWidget['text'] = f'Banlist File: None'

                exec('global banFile\nbanFile = filename')


            def ex(running=False):
                if running:
                    os.rename(f"Counter-Bot Instances\\Inst{INSTANCE}", "Counter-Bot Instances\\INSTANCE PURGED")
                    for root, dirs, files in os.walk("Counter-Bot Instances\\INSTANCE PURGED"):
                        for file in files:
                            os.remove(root+'\\'+file)
                    os.rmdir("Counter-Bot Instances\\INSTANCE PURGED")
                WIDGETS[0][0].destroy()
                sys.exit()
            
            def start_new_thread(btn):
                SETTS = settings.LOADNEWENV()
                PFs = eval(SETTS['CHNS'])
                PFs.extend(ASD)
                print(SETTS['TKN'])
                #input()
                TKN = SETTS['TKN']
                bot = Bot(root=WIDGETS[0][0], profiles=PFs, window=WIDGETS[0][0], tkn=TKN, dummyFileInput=banFile)#WIDGETS[1][1], WIDGETS[1][4], WIDGETS[1][7], WIDGETS[0][0], selFile, dummyFile, WIDGETS[0][0], PFs)

                def test(BOT, win):
                    try:
                        bot.run()
                    except:
                        exec("global fail\nfail=True")
                        print("THIS FIRES")
                        win.destroy()
                        
                new2 = threading.Thread(target=lambda: test(bot, WIDGETS[0][0]), daemon=True)
                new2.start()
                
                newThread = threading.Thread(target=bot.update_window, daemon=True)
                newThread.start()
                
                btn.destroy()
                WIDGETS[1][0].destroy()
                WIDGETS[1][1].destroy()
                WIDGETS[1][2].destroy()
                WIDGETS[1][3].destroy()
                #WIDGETS[1][4].destroy()
                
                pauseScroll = boolButton(states={'on':{'text':'Pause Chat Scroll', 'bg':'red', 'fg':'black'}, 'off':{'text':'Resume Chat Scroll', 'bg':'green', 'fg':'black'}}, defaultValue=True, master=WIDGETS[0][0], toggleCommand=lambda value: bot.updateScroll(pauseScroll.value))
                pauseScroll.place(x=10, y=15)
                
                stopButton = Button(text='Stop Bot', bg='red', relief='flat', command=lambda: ex(True))
                if sys.platform == 'win32':
                    stopButton.place(x=875, y=15)
                else:
                    stopButton.place(x=750, y=15)

                WIDGETS[1][-1].configure(command=lambda: banAll(bot))
                WIDGETS[0][0].protocol("WM_DELETE_WINDOW", lambda: ex(True))
                
            newButton = Button(WIDGETS[0][0], text='Start Bot', command=lambda:start_new_thread(newButton), bg='green', fg='#000000', relief='flat')
            newButton.place(x=10, y=15)
            
            #WIDGETS[1][1].configure(yscroll=WIDGETS[1][2].set)
            #WIDGETS[1][2].configure(command=WIDGETS[1][1].yview)
            
            #WIDGETS[1][4].configure(yscroll=WIDGETS[1][5].set)
            #WIDGETS[1][5].configure(command=WIDGETS[1][4].yview)
            
            #WIDGETS[1][7].configure(yscroll=WIDGETS[1][8].set)
            #WIDGETS[1][8].configure(command=WIDGETS[1][7].yview)

            #print(WIDGETS[1][1], WIDGETS[1][4], WIDGETS[1][7])
            
            #WIDGETS[1][1].configure(state=DISABLED)
            #WIDGETS[1][4].configure(state=DISABLED)
            #WIDGETS[1][7].configure(state=DISABLED)

            WIDGETS[1][1].configure(command=lambda: chooseFile(WIDGETS[1][2]))
            WIDGETS[1][3].configure(command=lambda: chooseBanlist(WIDGETS[1][2]))

            WIDGETS[0][0].protocol("WM_DELETE_WINDOW", ex)
            
            WIDGETS[0][0].mainloop()

            if fail:
                def CHECK(c, win):
                    allgood = True
                    if len(c.get()) == 0:
                        allgood = False
                        spawnErrorText('Can\'t leave blank', [c.winfo_x()+70, c.winfo_y()+19], errs, c)

                    elif len(c.get()) > 0:

                        try:
                            if len(c.get().split('/')[3].split('=')[1].split('&')[0]) != 30:
                                tkn = c.get().split('/')[3].split('=')[1].split('&')[0]
                                allgood = False
                                spawnErrorText('Invalid URL provided', [c.winfo_x()+60, c.winfo_y()+19], errs, c)
                        except IndexError:
                            allgood = False
                            spawnErrorText('Invalid URL provided', [c.winfo_x()+60, c.winfo_y()+19], errs, c)

                    if allgood:
                        print(c.get())
                        print(c.get().split('/')[3].split('=')[1].split('&')[0])
                        tkn=c.get().split('/')[3].split('=')[1].split('&')[0]
                        win.destroy()
                        a=open('.env', 'r')
                        asd=a.read()
                        a.close()
                        asd = asd.split('\n')
                        a=open('.env', 'w')
                        a.write(f'TKN={tkn}\n{asd[1]}')
                        os.startfile(__file__)
                        sys.exit()

                            
                
                WIDGETS = initialize({'name':'Token has expired.', 'geometry':f'300x200'}, 'dark', [
                {'button':{
                    'text':'Get token link',
                    'command':lambda: openLink('https://id.twitch.tv/oauth2/authorize?client_id=7583ak4tqsqbnpbdoypfpg2h0ie4tu&redirect_uri=http://localhost&response_type=token+id_token&scope=openid+channel:read:editors+moderator:manage:automod+channel:read:hype_train+channel:read:polls+channel:read:predictions+channel:read:redemptions+channel:read:subscriptions+moderation:read+user:edit+user:read:broadcast+user:read:email+user:read:follows+user:read:subscriptions+channel:moderate+chat:edit+chat:read+whispers:read+whispers:edit+channel:manage:polls'),
                    'placemode':'place',
                    'pos':{'x':20,'y':95},
                    'width':14
                    }},
                {'label':{
                    'text':'Paste redirect URL here:',
                    'placemode':'place',
                    'pos':{'x':140,'y':97}
                    }},
                {'entry':{
                    'width':37,
                    'pos':{'x':35,'y':125},
                    'placemode':'place'}},
                {'button':{
                    'text':'Set Token!',
                    'placemode':'place',
                    'pos':{'x':120,'y':165},
                    'command':lambda: CHECK(WIDGETS[1][2], WIDGETS[0][0])}
                 },
                {'label':{
                    'text':'Your token has expired and\nneeds to be renewed.',
                    'placemode':'place',
                    'pos':{'x':20,'y':20},
                    'font':('TkDefaultFont', 16),
                    'fg':'orange'}
                 }
                ])
                screen_width = WIDGETS[0][0].winfo_screenwidth()
                screen_height = WIDGETS[0][0].winfo_screenheight()
                TRUE_X = int((screen_width / 2) - (150))
                TRUE_Y = int((screen_height / 2) - (100))
                WIDGETS[0][0].geometry(f'+{TRUE_X}+{TRUE_Y}')
                #input()
                errs=[]
                WIDGETS[0][0].focus_force()
                WIDGETS[0][0].attributes("-topmost", True)
                WIDGETS[0][0].after(1, lambda: WIDGETS[0][0].attributes("-topmost", False))
                WIDGETS[0][0].protocol("WM_DELETE_WINDOW", lambda: ex(True))
                print(__file__)
                WIDGETS[0][0].mainloop()
        except Exception as e:
            while 1:
                try:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(f'Encountered Error {str(e)} at line {exc_tb.tb_lineno}')
                    input()
                except KeyboardInterrupt:
                    pass

