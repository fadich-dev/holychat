import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .buttons import ClickableButton
from .entries import NumberEntry
from .labels import InputLabel
from audio import record
import threading


class MainWindow(Gtk.Window):
    _main_box = None
    _record = []
    _buttons = {
        'record': dict()
    }
    _options = {
        'record': dict()
    }

    __recording = False
    __input_thread = None
    __output_thread = None
    __stop_event = threading.Event()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self._main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self._main_box.set_homogeneous(False)
        self._main_box.set_halign(Gtk.Align.CENTER)
        self._main_box.set_valign(Gtk.Align.START)

        self._main_box.set_margin_top(25)
        self._main_box.set_margin_right(25)
        self._main_box.set_margin_left(25)
        self._main_box.set_margin_bottom(25)

        self.add(self._main_box)

    def init(self):
        # self.set_default_size(300, 300)
        self.set_position(Gtk.WindowPosition.CENTER)

        self._init_buttons()
        self._init_options()

        self.show_all()
        self.connect('destroy', Gtk.main_quit)

        Gtk.main()

    def _init_buttons(self):
        h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        h_box.set_homogeneous(False)
        h_box.set_halign(Gtk.Align.CENTER)

        self._buttons['record']['start'] = self.create_start_record_button()
        self._buttons['record']['stop'] = self.create_stop_record_button()
        self._buttons['record']['play'] = self.create_play_record_button()

        h_box.add(self._buttons.get('record').get('start'))
        h_box.add(self._buttons.get('record').get('stop'))
        h_box.add(self._buttons.get('record').get('play'))

        h_box.set_size_request(10, 10)

        self._main_box.add(h_box)

        return self

    def _init_options(self):
        wrap_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        wrap_box.set_homogeneous(False)
        wrap_box.set_halign(Gtk.Align.START)
        wrap_box.set_valign(Gtk.Align.START)

        v_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        v_box.set_halign(Gtk.Align.START)

        self._options['record']['rate'] = self.create_rate_option_entry()

        v_box.add(InputLabel('Rate'))
        v_box.add(self._options.get('record').get('rate'))

        wrap_box.add(v_box)
        wrap_box.add(self.get_reset_options_button())

        self._main_box.add(wrap_box)

        return self

    def create_start_record_button(self):
        btn = ClickableButton().init(self._on_start_record, Gtk.Label(label='Start'))
        return btn

    def create_stop_record_button(self):
        btn = ClickableButton().init(self._on_stop_record, Gtk.Label(label='Stop'))
        btn.set_sensitive(False)
        return btn

    def create_play_record_button(self):
        btn = ClickableButton().init(self._on_play_record, Gtk.Label(label='Play'))
        btn.set_sensitive(False)
        return btn

    def create_rate_option_entry(self):
        entry = NumberEntry()
        entry.set_text(str(record.RECORD_RATE_IN))
        return entry

    def get_reset_options_button(self):
        btn = ClickableButton().init(self.reset_options, Gtk.Label(label='Default'))
        return btn

    def get_options(self):
        options = dict()
        options['rate'] = int(self._options.get('record').get('rate').get_text())

        return options

    def reset_options(self, widget):
        self._options.get('record').get('rate').set_text(str(record.RECORD_RATE_IN))

        return self

    def _on_start_record(self, widget):
        self._record = []
        self.__recording = True
        widget.set_sensitive(False)
        self._buttons.get('record').get('stop').set_sensitive(True)
        self._buttons.get('record').get('play').set_sensitive(False)

        self.__input_thread = threading.Thread(target=self.__read_record)
        self.__input_thread.start()

    def _on_stop_record(self, widget):
        self.__recording = False
        widget.set_sensitive(False)
        self._buttons.get('record').get('start').set_sensitive(True)
        self._buttons.get('record').get('play').set_sensitive(True)

        self.__stop_event.set()

    def _on_play_record(self, widget):
        widget.set_sensitive(False)
        self._buttons.get('record').get('start').set_sensitive(False)
        self._buttons.get('record').get('stop').set_sensitive(True)

        self.__output_thread = threading.Thread(target=self.__play_record)
        self.__output_thread.start()

    def _join_threads(self):
        if self.__input_thread:
            self.__input_thread.join()
        if self.__output_thread:
            self.__output_thread.join()

    def __read_record(self):
        self.__stop_event = threading.Event()
        stream = record.create_stream_in()
        while self.__recording:
            self._record.append(stream.read(record.RECORD_CHUNK * 10))
            if self.__stop_event.is_set():
                break
        stream.stop_stream()
        stream.close()

    def __play_record(self):
        self.__stop_event = threading.Event()
        stream = record.create_stream_out(**self.get_options())
        for frame in self._record:
            stream.write(frame)
            if self.__stop_event.is_set():
                break
        stream.stop_stream()
        stream.close()

    def __del__(self):
        self._join_threads()
