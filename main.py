import sys
import curses
from time import sleep
from midi_dispatcher import MidiDispatcher


def main(window):

    # Use default colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 215, -1)
    curses.init_pair(2, curses.COLOR_BLACK, 215)
    curses.init_pair(3, 81,  -1)

    # No cursor
    curses.curs_set(0)

    # No waiting for key inputs
    window.nodelay(True)

    # Get Midi interfaces
    midi_dispatcher = MidiDispatcher(window)
    midi_dispatcher.start()

    while True:
        key = window.getch()
        if key != -1:
            if key == 113:
                midi_dispatcher.stop()
                sys.exit(0)
            else:
                midi_dispatcher.action(key)
        sleep(.1)


if __name__ == "__main__":
    curses.wrapper(main)
