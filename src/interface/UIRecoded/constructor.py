import tkinter, sys, inspect, asyncio, exceptions

def get_classes(module) -> list[str]:
    return [name for (name, obj) in inspect.getmembers(module) if inspect.isclass(obj) and name not in ['_setit', 'getdouble', 'TclError', 'getint', '_VersionInfoType']]

def get_objects(module) -> list[str]:
    return [obj for (name, obj) in inspect.getmembers(module) if inspect.isclass(obj) and name not in ['_setit', 'getdouble', 'TclError', 'getint', '_VersionInfoType']]

class TKConstructor:
    root: tkinter.Tk
    widgets: list[tkinter.Widget] = []
    # Widget -> (widget type: {settings (must include placeMode or Location, can be explicit or implicit) } )

    def __init__(self, root: tkinter.Tk, *args, **kwargs):
        self.root = root
    
    def construct(self, widgets: list[dict], root: tkinter.BaseWidget = None) -> list[tuple[tkinter.BaseWidget, tkinter.Widget, tkinter.Variable, list]]:
        """
        Construct a set of widgets provided a list.
        Returns a list of tuples:
            ( master/root, widget, variable[optional], children[optional] )
        """

        retList = []

        for widget in widgets:
            widget: str
            var: tkinter.Variable = None

            constructSettings: dict
            settings: dict
            children: list[dict]

            constructSettings, settings, children = widget['construct'], widget['settings'], widget['children'] if 'children' in widget else []
            widget = constructSettings['widget'] if 'widget' in constructSettings else None

            if widget is None:
                raise exceptions.ConstructError("Widget was not specified when constructing. Skipping.")
            
            addMode = constructSettings['addmode'] if 'addmode' in constructSettings else 'place' if 'x' in constructSettings and 'y' in constructSettings else 'grid' if 'row' in constructSettings and 'column' in constructSettings else 'pack'
            posArgs = None
            match addMode:
                case 'pack':
                    posArgs = {'side': constructSettings['side'] if 'side' in constructSettings else None, 'fill': constructSettings['fill'] if 'fill' in constructSettings else None, 'expand': constructSettings['expand'] if 'expand' in constructSettings else None}
                case 'place':
                    posArgs = {'x':constructSettings['x'], 'y':constructSettings['y']}
                case 'grid':
                    posArgs = {'row':constructSettings['row'], 'column':constructSettings['column']}

            if widget.lower() in [x.lower() for x in get_classes(tkinter)]:
                settings.update({'master': self.root if not root else root})
                newWidget: tkinter.Widget = get_objects(tkinter)[[x.lower() for x in get_classes(tkinter)].index(widget.lower())](**settings)
                match addMode:
                    case 'pack':
                        newWidget.pack(**posArgs)
                    case 'grid':
                        newWidget.grid(**posArgs)
                    case 'place':
                        newWidget.place(**posArgs)

                childs = self.construct(children, root=newWidget)

                retList.append((root if root != None else self.root, widget, var, childs))
                
        
        return retList
