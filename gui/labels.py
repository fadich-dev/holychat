import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class LeftLabel(Gtk.Label):
    def __init__(self, *args, **kwargs):
        super(LeftLabel, self).__init__(*args, **kwargs)
        self.set_halign(Gtk.Align.START)
        self.set_valign(Gtk.Align.START)


class InputLabel(LeftLabel):
    def __init__(self, label, *args, **kwargs):
        super(InputLabel, self).__init__(*args, **kwargs)
        self.set_markup('<b>{}:</b>'.format(label))
