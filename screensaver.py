import pyglet
import os
import random

from PIL import Image


class AnimatedText(pyglet.text.Label):
    def __init__(self, text='', font_name=None, font_size=None, bold=False, italic=False, stretch=False,
                 color=(255, 255, 255, 255),
                 x=0, y=0, width=None, height=None,
                 anchor_x='left', anchor_y='baseline',
                 align='left',
                 multiline=False, dpi=None, batch=None, group=None, **kwargs):
        self.anim_time = 2.0
        self.dt = 0
        self.x_start = 0
        self.x_end = 0
        self.y_start = 0
        self.y_end = 0
        self.move_func = self.exponential_move
        self.conclude_func = None
        self.moving = False
        self.reverse = False
        self.stationary_time = 0.0
        if 'x_start' in kwargs.keys():
            self.x_start = kwargs.get('x_start')
            self.x_end = kwargs.get('x_end')
            x = self.x_start
        if 'y_start' in kwargs.keys():
            self.y_start = kwargs.get('y_start')
            self.y_end = kwargs.get('y_end')
            y = self.y_start
        if 'anim_time' in kwargs.keys():
            self.anim_time = kwargs.get('anim_time')
        if 'conclude_func' in kwargs.keys():
            self.conclude_func = kwargs.get('conclude_func')
        super().__init__(text, font_name, font_size, bold, italic, stretch, color, x, y, width, height, anchor_x,
                         anchor_y, align, multiline, dpi, batch, group)

    def __str__(self):
        return self.text

    def start_move(self):
        self.moving = True
        self.dt = 0.0
        self.stationary_time = 0.0

    def reverse_move(self):
        self.reverse = True
        self.moving = True
        self.dt = self.anim_time
        self.stationary_time = 0.0

    def set_anim_time(self, time):
        self.anim_time = time

    def set_start_end(self, x_s, x_e, y_s, y_e):
        self.x_start = x_s
        self.x_end = x_e
        self.y_start = y_s
        self.y_end = y_e

    def set_move_func(self, func):
        self.move_func = func

    def set_text(self, text):
        self.text = text

    def get_st_time(self):
        return self.stationary_time

    def cubic_move(self):
        x_rng = self.x_end - self.x_start
        y_rng = self.y_end - self.y_start
        abs_time = self.dt / self.anim_time
        abs_prog = 1 - (1 - abs_time) ** 3
        self.x = abs_prog * x_rng + self.x_start
        self.y = abs_prog * y_rng + self.y_start

    def linear_move(self):
        x_rng = self.x_end - self.x_start
        y_rng = self.y_end - self.y_start
        abs_time = self.dt / self.anim_time
        abs_prog = abs_time
        self.x = abs_prog * x_rng + self.x_start
        self.y = abs_prog * y_rng + self.y_start

    def exponential_move(self):
        x_rng = self.x_end - self.x_start
        y_rng = self.y_end - self.y_start
        abs_time = self.dt / self.anim_time
        abs_prog = 1.0 if abs_time == 1.0 else 1 - 2 ** (-10*abs_time)
        self.x = abs_prog * x_rng + self.x_start
        self.y = abs_prog * y_rng + self.y_start

    def update_pos(self, dt):
        if self.moving:
            if self.reverse:
                self.dt -= dt
            else:
                self.dt += dt
            self.move_func()
        else:
            self.stationary_time += dt
        if self.moving and not self.reverse and self.dt >= self.anim_time:
            self.moving = False
            self.reverse = False
            self.dt = 0.0
            self.x = self.x_end
            self.y = self.y_end
        elif self.moving and self.reverse and self.dt <= 0:
            self.moving = False
            self.reverse = False
            self.dt = 0.0
            self.x = self.x_start
            self.y = self.y_start
            if self.conclude_func:
                self.conclude_func()


class Screensaver:
    def __init__(self, window: pyglet.window.Window, mode: str, **kwargs):
        self._window = window
        self.mode = mode

        self.bg_image = self._get_image(kwargs.get('bg_image')) \
            if 'bg_image' in kwargs.keys() else None
        self.bg_image_on_bounce = self._get_image(kwargs.get('bg_image_on_bounce')) \
            if 'bg_image_on_bounce' in kwargs.keys() else None
        self.bg_image_on_corner = self._get_image(kwargs.get('bg_image_on_corner')) \
            if 'bg_image_on_corner' in kwargs.keys() else None
        self.main_image = self._get_image(kwargs.get('main_image')) \
            if 'main_image' in kwargs.keys() else self._get_image('')
        self.main_image_sequence = None
        self.main_image_sequence_i = 0
        if 'main_image_sequence' in kwargs.keys():
            self.main_image_sequence = [self._get_image(x) for x in kwargs.get('main_image_sequence')]
            self.main_image = self.main_image_sequence[0]
        self.main_image.scale = kwargs.get('main_image_scale') if 'main_image_scale' in kwargs.keys() else 1

        self.main_image.x, self.main_image.y = (self._window.width // 2, self._window.height // 2)

        self.speed = (160, 160)
        self.last_bounce = 5.0
        self.corner_threshold = 0.010  # 10 milliseconds

        self.labels = []

        self.labels.append(AnimatedText('Corner Hits: 0',
                                        font_name='Bahnschrift',
                                        font_size=52,
                                        anchor_x='left',
                                        anchor_y='top',
                                        x_start=30,
                                        x_end=30,
                                        y_start=0,
                                        y_end=90,
                                        anim_time=1.0,
                                        conclude_func=self.swap_labels))
        self.labels.append(AnimatedText('Time since last corner hit: None',
                                        font_name='Bahnschrift',
                                        font_size=42,
                                        anchor_x='left',
                                        anchor_y='top',
                                        x_start=30,
                                        x_end=30,
                                        y_start=0,
                                        y_end=80,
                                        conclude_func=self.swap_labels))
        self.current_label = 0
        self.labels[0].start_move()

    def _get_image(self, fp: str):
        """
        Returns a pyglet Sprite containing the image/animation

        :param fp: filepath of the image
        :return: tuple
        """
        if not fp:
            blk = Image.new('RGB', (10, 10), (0, 0, 0))
            image = pyglet.image.ImageData(10, 10, 'RGB', blk.tobytes(), pitch=-10 * 4)
            return pyglet.sprite.Sprite(img=image)
        fext = fp[fp.rfind('.'):]
        if fext == '.gif':
            anim = pyglet.resource.animation(fp)
            anim.get_duration()
            return pyglet.sprite.Sprite(img=anim)
        elif fext in ['.png', '.jpg', '.bmp']:
            ci = self._crop_image(Image.open(fp))
            image = pyglet.image.ImageData(ci.width, ci.height, ci.mode, ci.tobytes(), pitch=-ci.width * 4)
            return pyglet.sprite.Sprite(img=image)
        else:
            raise NotImplementedError

    @staticmethod
    def _crop_image(img: Image.Image):
        """
        Crops image based on transparent pixels

        :param img: PIL Image
        :return: cropped Image
        """
        if 'A' not in img.getbands():
            return img
        abnd = img.getbands().index('A')
        xl = 0
        xr = img.width
        yt = 0
        yb = img.height
        for i in range(1, img.width):
            for j in range(1, img.height):
                if img.getpixel((i, j))[abnd] != 0:
                    xl = i
                    break
            if xl == i:
                break
        for j in range(1, img.height):
            for i in range(1, img.width):
                if img.getpixel((i, j))[abnd] != 0:
                    yt = j
                    break
            if yt == j:
                break
        x_rng = list(range(1, img.width - 1))
        x_rng.reverse()
        for i in x_rng:
            for j in range(1, img.height):
                if img.getpixel((i, j))[abnd] != 0:
                    xr = i
                    break
            if xr == i:
                break
        y_rng = list(range(1, img.height - 1))
        y_rng.reverse()
        for j in y_rng:
            for i in range(1, img.width):
                if img.getpixel((i, j))[abnd] != 0:
                    yb = j
                    break
            if yb == j:
                break
        return img.crop((xl, yt, xr, yb))

    def swap_labels(self):
        self.current_label += 1
        if self.current_label == len(self.labels):
            self.current_label = 0
        self.labels[self.current_label].start_move()

    def on_bounce(self):
        if self.bg_image_on_bounce:
            # TODO: Show bg image on bounce
            # TODO: Play sound effect on bounce
            pass
        if self.main_image_sequence:
            x, y = self.main_image.x, self.main_image.y
            i = self.main_image_sequence_i
            while self.main_image_sequence_i == i:
                self.main_image_sequence_i = random.randint(0, len(self.main_image_sequence) - 1)
            self.main_image = self.main_image_sequence[self.main_image_sequence_i]
            self.main_image.x, self.main_image.y = x, y

    def on_corner(self):
        if self.bg_image_on_corner:
            # TODO: Show bg image on corner
            # TODO: Play sound effect on corner
            pass

    def on_draw(self):
        if self.bg_image:
            self.bg_image.draw()
        self.main_image.draw()
        self.labels[self.current_label].draw()

    def update(self, dt):
        if self.mode == 'standard':
            if self.main_image.x < 0 or self.main_image.x > self._window.width - self.main_image.width:
                if self.last_bounce <= self.corner_threshold:
                    self.on_corner()
                self.speed = (-self.speed[0], self.speed[1])
                self.on_bounce()
                self.last_bounce = 0

            if self.main_image.y < 0 or self.main_image.y > self._window.height - self.main_image.height:
                if self.last_bounce <= self.corner_threshold:
                    self.on_corner()
                self.speed = (self.speed[0], -self.speed[1])
                self.on_bounce()
                self.last_bounce = 0

            self.main_image.x += self.speed[0] * dt
            self.main_image.y += self.speed[1] * dt
            self.last_bounce += dt
        if self.mode == 'insanelike':
            pass
        if self.mode == 'infuriating':
            pass

        if not self.labels[self.current_label].moving:
            if self.labels[self.current_label].stationary_time >= 5:
                self.labels[self.current_label].reverse_move()
        self.labels[self.current_label].update_pos(dt)
