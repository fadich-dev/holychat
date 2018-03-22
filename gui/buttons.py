import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ClickableButton(Gtk.Button):
    on_click = None

    def init(self, on_click, *args, **kwargs):
        self.on_click = on_click
        self.add(*args, **kwargs)
        self.connect('clicked', self.on_click)

        return self
