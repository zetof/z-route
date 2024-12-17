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

    def has_connection(self, index):
        if index in self._connections:
            return True
        else:
            return False

    def add_connection(self, index):
        if index not in self._connections:
            self._connections.append(index)

    def del_connection(self, index):
        if index in self._connections:
            self._connections.remove(index)
