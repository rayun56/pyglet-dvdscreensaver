class Screensaver:
    def __init__(self, **kwargs):
        self.bg_image = None
        self.bg_image_on_bounce = None
        if 'bg_image' in kwargs.keys():
            self.bg_image = self._get_bg_image(kwargs.get('bg_image'))

    def _get_bg_image(self, fp):
        return fp

    def on_loop(self):
        pass

