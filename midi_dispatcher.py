import curses
import rtmidi
from threading import Thread
from time import sleep
from midi_port import MidiPort


class MidiDispatcher(Thread):

    PORT_IN = 0
    PORT_OUT = 1

    def __init__(self, window):
        self._window = window
        self._midi_in = rtmidi.MidiIn()
        self._midi_out = rtmidi.MidiOut()
        self._ports_in = []
        self._ports_out = []
        self._scan_delay = 1
        self._current_type = 0
        self._input_inx = 0
        self._output_inx = 0
        self._col1 = curses.color_pair(1)
        self._col2 = curses.color_pair(2)
        self._col3 = curses.color_pair(3)
        self._running = True
        Thread.__init__(self)

    def _scan_ports(self):
        self._scan_midi(self._midi_in, self._ports_in)
        self._scan_midi(self._midi_out, self._ports_out)

    def _scan_midi(self, midi, ports):
        # Check if midi device is already in devices list
        # If not, we add it to the list
        # Otherwise we just set the connected flag back
        for i in range(midi.get_port_count()):
            found = False
            for j, port in enumerate(ports):
                if port.get_name() == midi.get_port_name(i):
                    found = True
                    break
            if not found:
                ports.append(MidiPort(i, midi.get_port_name(i)))

    def _display_check(self, y, x, state):
        if state:
            self._window.addstr(y, x, "[x]", self._col3)
        else:
            self._window.addstr(y, x, "[ ]", self._col3)

    def _display_ports(self, ports, x):
        i = 0
        for port in ports:
            self._display_check(i + 1, x, port.has_connections())
            if i == self._output_inx:
                self._window.addstr(i + 1,
                                    x + 4,
                                    port.get_short_name(),
                                    self._col2)
            else:
                self._window.addstr(i + 1,
                                    x + 4,
                                    port.get_short_name(),
                                    self._col1)
            i += 1

    def run(self):
        while self._running:
            self._scan_ports()
            sleep(self._scan_delay)

    def stop(self):
        self._running = False

    def display(self):
        self._display_ports(self._ports_in, 1)
        self._display_ports(self._ports_out, 40)

    def action(self, key):
        pass
