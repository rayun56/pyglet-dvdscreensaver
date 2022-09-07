import pyglet

from PIL import Image
from mainwindow import MainWindow

window = pyglet.window.Window(fullscreen=True)
win = MainWindow(window)

sequence = [r'Images\dvdlogo-00.png',
            r'Images\dvdlogo-01.png',
            r'Images\dvdlogo-02.png',
            r'Images\dvdlogo-03.png',
            r'Images\dvdlogo-04.png']
win.start_screensaver('standard', main_image_sequence=sequence)


@window.event
def on_draw():
    win.on_draw()


def update(dt, *args, **kwargs):
    win.update(dt)


pyglet.clock.schedule(update, 1/144.0)

# while True:
#     pyglet.clock.tick()
#
#     for window in pyglet.app.windows:
#         window.switch_to()
#         window.dispatch_events()
#         window.dispatch_event('on_draw')
#         window.flip()

pyglet.app.run()