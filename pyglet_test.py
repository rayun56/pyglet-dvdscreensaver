import pyglet
from PIL import Image

window = pyglet.window.Window(fullscreen=True)

label = pyglet.text.Label('Hello, world!',
                          font_name='Consolas',
                          font_size=26,
                          x=window.width // 2,
                          y=window.height // 2,
                          anchor_x='center',
                          anchor_y='center')

# pil_image = Image.open(r'Images\dvdlogo-00.png')
# image = pyglet.image.ImageData(pil_image.width, pil_image.height, 'RGBA', pil_image.tobytes(), pitch=-pil_image.width * 4)

media = pyglet.media.load(r'Images\test.webm')
player = pyglet.media.Player()
player.queue(media)
player.play()

sequence = pyglet.resource.animation(r'Images/3d-saul-saul-goodman.gif')
sequence_sprite = pyglet.sprite.Sprite(img=sequence)

slider_base = pyglet.image.load(r'Images\Builtin\slider_base.png')
slider_knob = pyglet.image.load(r'Images\Builtin\slider_knob.png')
slider_knob.anchor_y = 10

slider = pyglet.gui.Slider(50, 50, slider_base, slider_knob, edge=0)



@window.event
def on_draw():
    print('loop')
    window.clear()
    # pyglet.gl.glEnable(pyglet.gl.GL_BLEND)

    label.draw()
    slider._base_spr.draw()
    slider._knob_spr.draw()
    # pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    i = 2
    # image.blit(0, 0, width=i * image.width, height=i * image.height)
    sequence_sprite.scale = slider.value * 0.05
    sequence_sprite.x = window.width // 2 - sequence_sprite.width * sequence_sprite.scale_x // 2
    sequence_sprite.y = window.height // 2 - sequence_sprite.height * sequence_sprite.scale_y // 2
    # print(sequence_sprite.position)
    sequence_sprite.draw()


@window.event
def on_mouse_press(x, y, buttons, modifiers):
    slider.on_mouse_press(x, y, buttons, modifiers)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    slider.on_mouse_drag(x, y, dx, dy, buttons, modifiers)


@slider.event
def on_change(value):
    pass



pyglet.app.run()