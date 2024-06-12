import asyncio, tkinter, exceptions

class AsyncTK:

    root: tkinter.Tk
    widgets: list[tkinter.Widget]
    framerate: int = 60
    mainLoop: asyncio.AbstractEventLoop

    def __init__(self, framerate: int = 60, title: str = None, size: str|tuple[int] = None, *args, **kwargs) -> None:

        self.root = tkinter.Tk(*args, **kwargs)
        self.root.title(title)
        self.framerate = framerate
        self.mainLoop = asyncio.new_event_loop()
        if size:
            self.root.geometry(size if isinstance(size, str) else f'{size[0]}x{size[1]}')

    async def render(self) -> None:

        """
        Coro -> renders application indefinitely or until exit condition is met.
        Framerate can be adjusted via AsyncTk.framerate
        """

        while True:

            self.root.update()

            await asyncio.sleep(float(1/self.framerate))

    async def run(self) -> None:

        asyncio.set_event_loop(self.mainLoop)
        await self.mainLoop.run_until_complete(self.render)

    async def bind(self, widget: tkinter.Widget|tkinter.Tk = None, event: str = None, func: callable = None) -> tuple[str, callable, str]:
        """
        Coro -> binds a specified event to a specified function for a specified widget.
        Returns a tuple containing:
            ( event: str , func: function , binding_id: str )

        Raises:
            exceptions.MissingParameterException:
                Parameter may not have been provided or is None
        """

        if not widget:
            widget = self.root
            print("No target widget provided for BIND. Assuming root.")

        if event is None or func is None:
            raise exceptions.MissingParameterException(f"BIND expected value for parameter {'event' if event is None else 'function'} but received None.")
            
        widget.bind(event, function)