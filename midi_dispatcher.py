import curses
import rtmidi
from threading import Thread
from time import sleep
from midi_port import MidiPort


class MidiDispatcher(Thread):

    def __init__(self, window):
        self._window = window
        self._midi = []
        self._midi.append(rtmidi.MidiOut())
        self._midi.append(rtmidi.MidiIn())
        self._ports = [0, 1]
        self._ports[0] = []
        self._ports[1] = []
        self._scan_delay = 1
        self._current_type = 0
        self._index = [0, 0]
        self._color1 = curses.color_pair(1)
        self._color2 = curses.color_pair(2)
        self._color3 = curses.color_pair(3)
        self._running = True
        Thread.__init__(self)

    def _scan_ports(self):
        refresh = False
        for index in range(2):
            if self._scan_midi(index):
                refresh = True
        if refresh:
            self._display()
            print("bob")

    def _scan_midi(self, index):
        # Check if midi device is already in devices list
        # If not, we add it to the list
        # Otherwise we just set the connected flag back
        refresh = False
        midi = self._midi[index]
        ports = self._ports[index]
        for i in range(midi.get_port_count()):
            found = False
            for j, port in enumerate(ports):
                if port.get_name() == midi.get_port_name(i):
                    found = True
                    break
            if not found:
                ports.append(MidiPort(i, midi.get_port_name(i)))
                refresh = True
        return refresh

    def _display_check(self, y, x, selected):
        checked = "[x]" if selected else "[ ]"
        self._window.addstr(y, x, checked, self._color3)

    def _display_port(self, index, i):
        if index == 1:
            self._display_check(i + 1, 35 * index, False)
            indent = 4
        else:
            indent = 1
        color = self._color1
        if self._current_type == index and i == self._index[index]:
            color = self._color2
        self._window.addstr(i + 1,
                            35 * index + indent,
                            self._ports[index][i].get_short_name(),
                            color)

    def _display_ports(self, index):
        ports = self._ports[index]
        for i in range(len(ports)):
            self._display_port(index, i)

    def run(self):
        while self._running:
            self._scan_ports()
            sleep(self._scan_delay)

    def stop(self):
        self._running = False

    def _display(self):
        for index in range(2):
            self._display_ports(index)

    def action(self, key):
        refresh = False
        if key == 32 and self._current_type == 1:
            if self._ports[0][self._index[0]].has_connection(self._index[1]):
                self._ports[0][self._index[0]].del_connection(self._index[1])
            else:
                self._ports[0][self._index[0]].add_connection(self._index[1])
        if key == curses.KEY_RIGHT:
            if self._current_type == 0:
                self._current_type = 1
                refresh = True
        elif key == curses.KEY_LEFT:
            if self._current_type == 1:
                self._current_type = 0
                refresh = True
        elif key == curses.KEY_UP:
            if self._index[self._current_type] > 0:
                self._index[self._current_type] -= 1
                refresh = True
        elif key == curses.KEY_DOWN:
            if (self._index[self._current_type] <
                    len(self._ports[self._current_type]) - 1):
                self._index[self._current_type] += 1
                refresh = True
        if refresh:
            self._display()
