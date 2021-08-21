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
import tkinter
from tkinter import *
from tkinter import ttk
import webbrowser
import threading

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

class boolButton(Button):

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

        if btn.value == True:
            btn['text'] = opts.get('off').get('text')
            btn['bg'] = opts.get('off').get('bg')
            btn['fg'] = opts.get('off').get('fg')
            btn['relief'] = 'raised'

        if btn.value == False:
            btn['text'] = opts.get('on').get('text')
            btn['bg'] = opts.get('on').get('bg')
            btn['fg'] = opts.get('on').get('fg')
            btn['relief'] = 'sunken'

        btn.value = not btn.value
        if btn.toggleCommand != None:
            btn.toggleCommand()

def findOpt(Widget=None, Style=None, styleSet=None, specificOption=None, overrides=None):

        if overrides == None or overrides.get(specificOption) == None:
            if styleSet != None and Style != None:
                if Widget != None:
                    if specificOption == None:
                        print(f"returning {styleSet.get(Style).get(Widget)}")
                        return styleSet.get(Style).get(Widget)

                    elif specificOption != None:
                        #print(f"STYLE {Style}, STYLESET {styleSet}")
                        if styleSet.get(Style).get(Widget) != None:
                            print(f"request {Widget} returning {styleSet.get(Style).get(Widget).get(specificOption)}")
                            return styleSet.get(Style).get(Widget).get(specificOption)
                        else:
                            return None

                else:
                    if specificOption != None:
                        print(f"request {Widget} returning {styleSet.get(Style).get(specificOption)}")
                        return styleSet.get(Style).get(specificOption)

                    else:
                        print(f"request {Widget} returning None")
                        return None

            elif Style == None and styleSet != None and specificOption != None:
                if Widget != None:
                    print(f"request {Widget} returning {styleSet.get(Widget).get(specificOption)}")
                    return styleSet.get(Widget).get(specificOption)

                elif Widget == None:
                    print(f"request {Widget} returning {styleSet.get(specificOption)}")
                    return styleSet.get(specificOption)

            else:
                print(f"request {Widget} returning None")
                return None
        elif overrides != None and specificOption != None:
            print(f"request {Widget} returning {overrides.get(specificOption)}")
            return overrides.get(specificOption)

        else:
            return None

def initialize(windowOptions=None, style=None, widgets=[]):

    retWidgets = []
    retVars = [] # NOTE: retVars uses tuples with structure (variable, attachedObject).

    def createWidget(Widget, widgetOpts):

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

            print(posKey, wOpts)
            
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

            

    mainWindow = Tk()
    print(windowOptions)
    mainWindow.title(findOpt(None, specificOption='name', styleSet=windowOptions))
    mainWindow['bg'] = findOpt('window', style, styleSet=styles).get('bg')
    mainWindow.geometry(findOpt(None, specificOption='geometry', styleSet=windowOptions))

    for conf in widgets:
        widget = list(conf.keys())[0]
        print(f"processing : {conf}")
        try:
            if conf.get(widget).get('master').get("widgetIndex") != None:
                master=retWidgets[int(conf.get(widget).get('master').get("widgetIndex"))]
            else:
                master=conf.get(widget).get('master')
        except:
            master=conf.get(widget).get('master')
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

        elif widget == 'boolButton':
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

        createWidget(new, conf)
        print(widget)
        retWidgets.append(new)

    mainWindow.resizable(False, False)

    return ([mainWindow, style], retWidgets, retVars)

def matchType(inObj=None, targetType=None):
    return [type(inObj) == targetType, type(inObj), targetType]

def add_greeter(index, offsetX=0, offsetY=0):
    nonANChars = ["!", "@", "#", "&", "(", ")", "–", "[", "{", "}", "]", ":", ";", "‘", ",", "?", "/", "*", "\\", ' ', '"', "'"]
    clear = True
    for char in nonANChars:
        if char in WIDGETS[-2][index].get():
            
            print("This triggers")
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

    if clear == True:
        
        if not WIDGETS[-2][index].get() in greeters:
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
            
        else:
            spawnErrorText('Greeter already in list.', [WIDGETS[-2][index].winfo_x()+offsetX, WIDGETS[-2][index].winfo_y()+offsetY], errs, WIDGETS[-2][index])
            print([WIDGETS[-2][index].winfo_x(), WIDGETS[-2][index].winfo_y()])

def spawnErrorText(txt=None, loc=[], IDList=None, relateTo=None):
    typeTXT = matchType(txt, str)
    if not typeTXT[0]:
        raise TypeError(f"Value provided for arg <txt> is {typeTXT[1]}, required {typeTXT[2]}")

    typeLoc = matchType(loc, list)
    if not typeLoc[0]:
        raise TypeError(f"Value provided for arg <loc> is {typeLoc[1]}, required {typeLoc[2]}")

    if len(loc) != 2:
        raise IndexError(f"spawnErrorText requires a list with length 2 (posX, posY). Length given: {len(loc)}")
    
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

    if IDList != None:
        typeIDL = matchType(IDList, list)
        if not typeIDL[0]:
            raise IndexError(f"Value provided for arg <IDList> is {typeIDL[1]}, required {typeIDL[2]}")

        IDList.append([newError, relateTo])

        return IDList

def delAllErrors(ErrorMessageList=[], specificIndex=None):
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
                item.destroy()
            return []

def refreshOpts(opts, varList):
    
    for button in opts.get("buttons"):
        if type(button) == ttk.OptionMenu:
            for var, parent in varList:
                if parent == button:
                    button.set_menu(var.get(), *opts.get('source').get().split(' '))

    opts.get('source').delete(0,END)

def openLink(url):
    webbrowser.open(url)

def startBot():
    a=WIDGETS[1][1] # entry
    b=WIDGETS[1][3] # entry
    c=WIDGETS[1][6] # entry
    d=WIDGETS[1][10] # entry
    e=WIDGETS[1][13] # optionMenu
    f=WIDGETS[1][19] # optionMenu
    g=WIDGETS[1][21] # optionMenu
    h=WIDGETS[1][8] # boolButton

    newstuff = []
    for x in errs:
        if a == x[1] or b == x[1] or c == x[1] or d == x[1] or e == x[1] or f == x[1] or g == x[1]:
            delAllErrors(errs, errs.index(x))
        else:
            newstuff.append(x)

    exec("errs = newstuff")

    allgood = True

    if len(a.get()) == 0:
        allgood = False
        spawnErrorText('Can\'t leave blank', [a.winfo_x()+14, a.winfo_y()+19], errs, a)

    for char in ["!", "@", "#", "&", "(", ")", "–", "[", "{", "}", "]", ":", ";", "‘", ",", "?", "/", "*", "\\", ' ', '"', "'"]:
        if char in a.get():
            allgood = False
            spawnErrorText('Only alphanumeric characters are permitted.', [a.winfo_x()-115, a.winfo_y()+19], errs, a)

    if len(b.get()) == 0:
        allgood = False
        spawnErrorText('Can\'t leave blank', [b.winfo_x()+14, b.winfo_y()+19], errs, b)

    elif len(b.get()) > 0:

        try:
            int(b.get())
        except ValueError:
            allgood = False
            spawnErrorText('Only integers are permitted.', [b.winfo_x()-25, b.winfo_y()+19], errs, b)

    if len(c.get()) == 0:
        allgood = False
        spawnErrorText('Can\'t leave blank', [c.winfo_x()+70, c.winfo_y()+19], errs, c)

    elif len(c.get()) > 0:

        try:
            if len(c.get().split('/')[3].split('=')[1].split('&')[0]) != 30:
                allgood = False
                spawnErrorText('Invalid URL provided', [c.winfo_x()+60, c.winfo_y()+19], errs, c)
        except IndexError:
            allgood = False
            spawnErrorText('Invalid URL provided', [c.winfo_x()+60, c.winfo_y()+19], errs, c)

    if len(d.get()) == 0:
        allgood = False
        spawnErrorText('Can\'t leave blank', [d.winfo_x()+14, d.winfo_y()+19], errs, d)

    elif len(d.get()) > 0:

        try:
            int(d.get())
        except ValueError:
            allgood = False
            spawnErrorText('Only integers are permitted.', [d.winfo_x()-25, d.winfo_y()+19], errs, d)

    for var, owner in WIDGETS[-1]:
        if owner == f:
            if len(var.get()) == 0:
                allgood = False
                spawnErrorText('Can\'t leave blank', [f.winfo_x()+14, f.winfo_y()+24], errs, f)
        if owner == g:
            if len(var.get()) == 0:
                allgood = False
                spawnErrorText('Can\'t leave blank', [g.winfo_x()+14, g.winfo_y()+24], errs, g)

    if allgood == True:
        print("ALL OPTS GOOD")
        channel = a.get()
        duration = int(b.get())
        tkn = c.get().split('/')[3].split('=')[1].split('&')[0]
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

        writeEnv([channel, botcap, blacklist, blacklisted_phrases, greeter, word_index, welcome_marker, duration, tkn])
        WIDGETS[0][0].destroy()
        dotenv.load_dotenv()
        
def setBlacklistButton(test=None):

    WIDGETS[1][24].set_menu(['Blacklist'][0], *bList)

def addToBlacklist(source, List):

    if not source.get() in List and len(source.get()) > 0:
        cont = True
        count = 0
        asd = len(source.get())
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
            spawnErrorText('Spaces only can\'t be\nblacklisted', [source.winfo_x()+15, source.winfo_y()+20], errs, source)

        if cont == True:
            List.append(source.get())
            setBlacklistButton()
            newstuff = []
            for x in errs:
                if WIDGETS[1][WIDGETS[1].index(source)] == x[1]:
                    delAllErrors(errs, errs.index(x))
                else:
                    newstuff.append(x)

            WIDGETS[1][WIDGETS[1].index(source)].delete(0,END)

            exec("errs=newstuff")

    else:
        newstuff = []
        for x in errs:
            if WIDGETS[1][WIDGETS[1].index(source)] == x[1]:
                delAllErrors(errs, errs.index(x))
            else:
                newstuff.append(x)

        exec("errs=newstuff")
        
        if source.get() in List:
            spawnErrorText('Already in blacklist', [source.winfo_x()+20, source.winfo_y()+30], errs, source)

        elif len(source.get()) == 0:
            spawnErrorText('Can\'t add blank to list', [source.winfo_x()+15, source.winfo_y()+30], errs, source)
    
greeters=['nightbot', 'streamlabs', 'streamelements']

#create a setup to write initial env variables. can be re-triggered as needed.    
        
#INITIAL SETUP CODE FOR FIRST TIME RUN
try:
    a = open(".env", 'r')
    a.close()
except FileNotFoundError:
    while 1:
        try:
            WIDGETS = initialize({'name':'Twitch Counter-Bot v2.0.0 - Setup', 'geometry':'600x400'}, 'dark', [
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
                {'button':{
                    'text':'Get token link',
                    'command':lambda: openLink('https://id.twitch.tv/oauth2/authorize?client_id=7583ak4tqsqbnpbdoypfpg2h0ie4tu&redirect_uri=http://localhost&response_type=token+id_token&scope=openid+channel:read:editors+moderator:manage:automod+channel:read:hype_train+channel:read:polls+channel:read:predictions+channel:read:redemptions+channel:read:subscriptions+moderation:read+user:edit+user:read:broadcast+user:read:email+user:read:follows+user:read:subscriptions+channel:moderate+chat:edit+chat:read+whispers:read+whispers:edit+channel:manage:polls'),
                    'placemode':'place',
                    'pos':{'x':2,'y':98},
                    'width':14
                    }},
                {'label':{
                    'text':'Paste redirect URL here:',
                    'placemode':'place',
                    'pos':{'x':118,'y':100}
                    }},
                {'entry':{
                    'width':40,
                    'pos':{'x':2,'y':125},
                    'placemode':'place'}},
                {'label':{
                    'text':'Blacklist bot spam phrases?',
                    'placemode':'place',
                    'pos':{'x':2,'y':170}
                    }},
                {'boolButton':{
                    'states':{'off':{'text':'off','bg':'red','fg':'black'},
                              'on':{'text':'on','bg':'green','fg':'black'}},
                    'placemode':'place',
                    'pos':{'x':160,'y':168},
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
                    'command': lambda: add_greeter(12, -140, 22)
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
                    'command':lambda: refreshOpts({'buttons':[WIDGETS[1][19], WIDGETS[1][21]],
                                                   'source':WIDGETS[1][16]},
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
                    'pos':{'x':2, 'y':202},
                    'width':24
                    }},
                {'button':{
                    'text':'Add to Blacklist',
                    'placemode':'place',
                    'pos':{'x':160, 'y':200},
                    'command':lambda: addToBlacklist(WIDGETS[1][22], bList)
                    }},
                {'optionMenu':{
                    'placemode':'place',
                    'pos':{'x':160, 'y':230},
                    'values':['bigfollows'],
                    'default':['Blacklist'][0],
                    'width':93,
                    'height':24,
                    'command':setBlacklistButton
                    }},
                {'button':{
                    'placemode':'place',
                    'pos':{'x':2, 'y':268},
                    'text':'All Set! Start Bot!',
                    'width':20,
                    'command':startBot
                    }}
                ])
            errs = []
            bList = []
            WIDGETS[-2][10].delete(0,END)
            WIDGETS[-2][10].insert(0,'20')
            WIDGETS[-2][3].delete(0,END)
            WIDGETS[-2][3].insert(0,'10')
            WIDGETS[0][0].mainloop()
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


        file = None
        customFile = False

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
    safelist=[]
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
    scrollToBottom = True
    tempBlacklist = []

    
    streamerID = None
    prevage=''
    prevprevage=''
    prevuser=''
    prevprevuser=''
    prevmsg=''
    prevprevmsg=''

    def __init__(self, textfield, botfield, bannedfield, window):

        super().__init__(
    token=f"{self.token}",
    client_id="7583ak4tqsqbnpbdoypfpg2h0ie4tu",
    nick="crimsoneye16",
    prefix="<prefix goes here>",
    initial_channels=[f"#{self.channelToJoin}"]
)
        self.TEXTFIELD = textfield
        self.TEXTFIELD.configure(state='normal')
        self.TEXTFIELD.insert(END, f'\nChatlog: Chat will appear here once you hit "Start Bot"')
        self.TEXTFIELD.configure(state=DISABLED)
        self.WINDOW = window
        self.BOTSFIELD = botfield
        self.BANNED = bannedfield

    def update_window(self):
        while True:
            self.WINDOW.update()

    def updateScroll(self, value):
        self.scrollToBottom = value
        print(self.scrollToBottom)
            
    async def event_ready(self):
        print("good to go")
        #try:
        #    await self.get_channel(self.channelToJoin).send("Bot Ready!") <- optional and doesn't always work
        #except Exception as e:
        #    print(str(e))
        self.TEXTFIELD.configure(state='normal')
        self.TEXTFIELD.insert(END, f'\nStarting Bot: Attempting Connection')
        self.TEXTFIELD.insert(END, f'\nBot Start: SUCCESS\nConnected to channel: {self.channelToJoin}\nDEBUG: RAW SETTINGS : {self.Settings}')
        self.TEXTFIELD.insert(END, f'\n\n <====== CHAT LOG BEGINS HERE ======>\n')
        self.TEXTFIELD.configure(state=DISABLED)

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
            self.TEXTFIELD.configure(state='normal')
            self.TEXTFIELD.insert(END, f"\n{ctx.author.name}: {ctx.content}")
            self.TEXTFIELD.configure(state=DISABLED)
            if self.scrollToBottom == True:
                self.TEXTFIELD.yview_pickplace("end")
            
            
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
                
                accAge = get(f"https://decapi.me/twitch/accountage/{user}").content.decode()
                newList = accAge.split(',')
                debug.write(f"| - > User Age |> {newList}", False)
                curAge=newList[0]
                print(f"============================> new follow {curAge}")
                self.TEXTFIELD.configure(state='normal')
                self.TEXTFIELD.insert(END, f"\n<===== New Follower =====>\nUsername: {user} | Account Age {accAge}")
                self.TEXTFIELD.configure(state=DISABLED)
                

                #print(f"{self.prevage}, {curAge}")
                    
                if curAge == self.prevage and curAge == self.prevprevage:
                            
                    if user not in self.botlist and user not in self.safelist:
                        self.botlist.append(user)
                        debug.write(f"| - > Added {user} to botlist, user will be banned on bot raid trigger.", False)
                        self.counter += 1
                        self.TEXTFIELD.configure(state='normal')
                        self.TEXTFIELD.insert(END, f"\n > > > > Account age match detected. Added {user} to botlist, ban on raid trigger.")
                        self.TEXTFIELD.configure(state=DISABLED)
                            
                    if self.prevuser not in self.botlist and self.prevuser not in self.safelist:
                        self.botlist.append(self.prevuser)
                        debug.write(f"| - > Added {self.prevuser} to botlist, user will be banned on bot raid trigger.", False)
                        self.counter += 1
                        self.TEXTFIELD.configure(state='normal')
                        self.TEXTFIELD.insert(END, f"\n > > > > Added {self.prevuser} to botlist, ban on raid trigger.")
                        self.TEXTFIELD.configure(state=DISABLED)

                    if self.prevprevuser not in self.botlist and self.prevprevuser not in self.safelist:
                        self.botlist.append(self.prevprevuser)
                        debug.write(f"| - > Added {self.prevprevuser} to botlist, user will be banned on bot raid trigger.", False)
                        self.counter += 1
                        self.TEXTFIELD.configure(state='normal')
                        self.TEXTFIELD.insert(END, f"\n > > > > Added {self.prevprevuser} to botlist, ban on raid trigger.")
                        self.TEXTFIELD.configure(state=DISABLED)

                    self.BOTSFIELD.configure(state='normal')
                    self.BOTSFIELD.delete('1.0', END)
                        
                    for botuser in self.botlist:
                        self.BOTSFIELD.insert(END, f"\n{botuser}")

                    self.BOTSFIELD.configure(state=DISABLED)

                    

                if self.counter >= int(bot_cap):
                    debug.write("<<<<BOT RAID DETECTED>>>>")
                                
                    await channel.send(f"/followers {follow_duration}")
                    debug.write(">> Enabled 10 minute Followers-Only Mode.", False)
                    await channel.send("/clear")
                    debug.write(">> Cleared Chat to remove any other messages.", False)
                    self.BANNED.configure(state='normal')
                                
                    for user in self.botlist:
                                    
                        await channel.send("/ban " + user + " bot follower.")
                        debug.write(f">> BOT RAID: BANNED |> {user}", False)
                        self.BANNED.insert(END, f"{user}")

                    self.BANNED.configure(state=DISABLED)

                    self.counter = 0
                    self.botlist = []
                    await channel.send("/followersoff")
                    debug.write(">> Disabled Followers-Only Mode. Bot raid crisis averted.", False)

                    
                self.prevprevage = self.prevage
                self.prevage = curAge
                self.prevprevuser = self.prevuser
                self.prevuser=user

                if self.prevage != self.prevprevage and self.prevage != None and self.prevprevage != None:
                    try:
                        self.botlist.remove(f"{user}")
                        self.BOTSFIELD.configure(state='normal')
                        self.BOTSFIELD.delete('1.0', END)
                            
                        for botuser in self.botlist:
                            self.BOTSFIELD.insert(END, f"\n{botuser}")

                        self.BOTSFIELD.configure(state=DISABLED)
                        
                    except ValueError:
                        pass

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

            if ("ab!commands" == words[0] or "ab!help" == words[0]) and is_streamer:
                await channel.send("varHelp : Display variable types help (broadcaster only)")
                await channel.send("setGreeter : Updates follow trigger conditions (broadcaster only)")
                await channel.send("setCap : Sets the follow cap before anti-bot response is triggered (broadcaster only)")
                await channel.send("setFTime : Sets the follow only mode time in case of bot raid (broadcaster only)")
                await channel.send("commands : Displays this set of messages (broadcaster only)")
                await channel.send("help : Displays this set of messages (broadcaster only)")
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

            if "ping" == words[0] and is_creator:
                await channel.send("pong")

            #if blacklist == True:
            #    if author.name in self.botlist:
            #        self.tempBlacklist.append(message[1:])
            #        
            #    elif author.name not in self.botlist and message == self.prevmsg and message == self.prevprevmsg:
            #        
            #        self.botlist.append(author.name)
            #        self.counter += 1
            #        
            #        if self.prevuser not in self.botlist:
            #            self.botlist.append(self.prevuser)
            #            self.counter += 1
            #            
            #        if self.prevprevuser not in self.botlist:
            #            self.botlist.append(self.prevprevuser)
            #            self.counter += 1
                        
                    

            self.prevprevmsg=self.prevmsg    
            self.prevmsg=message
            
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
        WIDGETS = initialize({'name':'Twitch Counter-Bot V2.0.0', 'geometry':'940x400'}, 'dark', [
        {'button':{
            'text':'Stop Bot',
            'bg':'red',
            'placemode':'place',
            'pos':{'x':875, 'y':15},
            'command': exit
            }},
        {'frame':{
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
            'master':{'widgetIndex':1},
            'side':LEFT,
            'relief':'flat'
            }},
        {'scrollbar':{
            'placemode':'pack',
            'master':{'widgetIndex':1},
            'side':LEFT,
            'ipady':135,
            'ipadx':1,
            'bg':'#323232',
            'activebackground':'#323232',
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
            'master':{'widgetIndex':4},
            'side':LEFT,
            'relief':'flat'
            }},
        {'scrollbar':{
            'placemode':'pack',
            'master':{'widgetIndex':4},
            'side':LEFT,
            'ipady':125,
            'ipadx':1,
            'bg':'#323232',
            'activebackground':'#323232',
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
            'width':27,
            'height':19,
            'master':{'widgetIndex':7},
            'side':LEFT,
            'relief':'flat'
            }},
        {'scrollbar':{
            'placemode':'pack',
            'master':{'widgetIndex':7},
            'side':LEFT,
            'ipady':125,
            'ipadx':1,
            'bg':'#323232',
            'highlightbackground':'#323232',
            'troughcolor':'#323232'
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
            }},
        ])
        bot = Bot(WIDGETS[1][2], WIDGETS[1][-2], WIDGETS[1][-1], WIDGETS[0][0])
        
        def start_new_thread(btn):
            newThread = threading.Thread(target=bot.update_window, daemon=True)
            newThread.start()
            new2 = threading.Thread(target=bot.run, daemon=True)
            new2.start()
            btn.destroy()
            pauseScroll = boolButton(states={'on':{'text':'Pause Chat Scroll', 'bg':'red', 'fg':'black'}, 'off':{'text':'Resume Chat Scroll', 'bg':'green', 'fg':'black'}}, defaultValue=True, master=WIDGETS[0][0], toggleCommand=lambda value: bot.updateScroll(pauseScroll.value))
            pauseScroll.place(x=10, y=15)
            
        newButton = Button(WIDGETS[0][0], text='Start Bot', command=lambda:start_new_thread(newButton), bg='green', fg='#000000', relief='flat')
        newButton.place(x=10, y=15)
        WIDGETS[1][2].configure(yscroll=WIDGETS[1][3].set)
        WIDGETS[1][3].configure(command=WIDGETS[1][2].yview)
        WIDGETS[1][5].configure(yscroll=WIDGETS[1][6].set)
        WIDGETS[1][6].configure(command=WIDGETS[1][5].yview)
        WIDGETS[1][8].configure(yscroll=WIDGETS[1][9].set)
        WIDGETS[1][9].configure(command=WIDGETS[1][8].yview)
        WIDGETS[1][2].configure(state=DISABLED)
        WIDGETS[1][5].configure(state=DISABLED)
        WIDGETS[1][8].configure(state=DISABLED)
        WIDGETS[0][0].mainloop()
    except Exception as e:
        print(str(e))

debug.write("<<--Shutting Down-->>")
