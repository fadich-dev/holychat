import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .buttons import ClickableButton
from audio import record
import threading


class MainWindow(Gtk.Window):
    _main_box = None
    _record = b''
    _buttons = {
        'record': dict()
    }

    __recording = False
    __input_thread = None
    __output_thread = None

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self._main_box = Gtk.Box(spacing=15)
        self._main_box.set_homogeneous(False)
        self._main_box.set_halign(Gtk.Align.CENTER)
        self._main_box.set_valign(Gtk.Align.START)

        self.add(self._main_box)

    def init(self):
        # self.set_default_size(300, 300)
        self.set_position(Gtk.WindowPosition.CENTER)

        self._init_buttons()

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

        h_box.add(self._buttons['record']['start'])
        h_box.add(self._buttons['record']['stop'])
        h_box.add(self._buttons['record']['play'])

        h_box.set_margin_top(25)
        h_box.set_margin_right(25)
        h_box.set_margin_left(25)
        h_box.set_margin_bottom(25)
        h_box.set_size_request(10, 10)

        self._main_box.add(h_box)

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

    def _on_start_record(self, widget):
        self._record = b''
        self.__recording = True
        widget.set_sensitive(False)
        self._buttons['record']['stop'].set_sensitive(True)
        self._buttons['record']['play'].set_sensitive(False)

        self.__input_thread = threading.Thread(target=self.__listen_record)
        self.__input_thread.start()

    def _on_stop_record(self, widget):
        self.__recording = False
        widget.set_sensitive(False)
        self._buttons['record']['start'].set_sensitive(True)
        self._buttons['record']['play'].set_sensitive(True)

        self._join_threads()

    def _on_play_record(self, widget):
        self.__output_thread = threading.Thread(target=self.__play_record)
        self.__output_thread.start()

        self._join_threads()

    def _join_threads(self):
        if self.__input_thread:
            self.__input_thread.join()
        if self.__output_thread:
            self.__output_thread.join()

    def __listen_record(self):
        stream = record.create_stream_in()
        while self.__recording:
            self._record += stream.read(record.RECORD_CHUNK * 10)
        stream.stop_stream()
        stream.close()

    def __play_record(self, rate=record.RECORD_RATE_IN):
        stream = record.create_stream_out(rate=rate)
        stream.write(self._record)
        stream.stop_stream()
        stream.close()

    def __del__(self):
        self._join_threads()
