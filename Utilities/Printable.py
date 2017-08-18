import time

class Printable:

    epoch = time.time()

    def __init__(self, name):

        self._name = name

    def error(self, message):

        self.message('[ERROR] ' + message)

    def message(self, *message):

        t = time.time() - Printable.epoch
        print(' {:>15} | {:07.1f} |'.format(self._name, t), *message)

    @staticmethod
    def print_header():
        print(' {:^15} | {:^7} | {}'.format('Caller', 'Time', 'Message'))