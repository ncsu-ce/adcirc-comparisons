import time

class Printable:

    epoch = time.time()
    name_width = 15

    def __init__(self, name):

        self._name = name

        if len(self._name) > Printable.name_width:
            Printable.name_width = len(self._name)

    def error(self, *message):

        self.message('[ERROR] ', *message)

    def message(self, *message):

        t = time.time() - Printable.epoch
        string = ' {:>' + str(Printable.name_width) + '} | {:07.1f} |'
        print(string.format(self._name, t), *message)

    def warning(self, *message):

        self.message('[WARNING] ', *message)

    def message_sameline(self, *message):

        t = time.time() - Printable.epoch
        string = ' {:>' + str(Printable.name_width) + '} | {:07.1f} |'
        print(string.format(self._name, t), *message, end='\r')

    def finish_sameline(self):

        print()

    @staticmethod
    def print_header():
        string = ' {:^' + str(Printable.name_width) + '} | {:^7} | {}'
        print(string.format('Caller', 'Time', 'Message'))