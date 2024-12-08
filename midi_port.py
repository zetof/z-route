import re


class MidiPort:

    def __init__(self, index, name):
        self._index = index
        self._name = name
        self._short_name = re.sub(" \\d+:\\d$", "", name)
        self._connections = []

    def get_name(self):
        return self._name

    def get_short_name(self):
        return self._short_name

    def has_connections(self):
        if len(self._connections) > 0:
            return True
        else:
            return False
