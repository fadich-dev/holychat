import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class NumberEntry(Gtk.Entry):
    def __init__(self, *args, **kwargs):
        super(NumberEntry, self).__init__(*args, **kwargs)
        self.connect('changed', self._on_change)

    def _on_change(self, *args):
        text = self.get_text().strip()
        self.set_text(''.join([i for i in text if i in '-0123456789']))
