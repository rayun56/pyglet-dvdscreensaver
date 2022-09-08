import pyglet

from screensaver import Screensaver


class MainWindow:
    def __init__(self, window):
        self.scr = None
        self.window = window

    def start_screensaver(self, mode, **kwargs):
        self.scr = Screensaver(self.window, mode, **kwargs)

    def on_draw(self):
        self.window.clear()
        if self.scr:
            self.scr.on_draw()

    def on_key_press(self, symbol, modifiers):
        if self.scr:
            self.scr.on_key_press(symbol, modifiers)

    def update(self, dt):
        if self.scr:
            self.scr.update(dt)
