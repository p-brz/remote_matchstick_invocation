import fcntl
import sys
import os
import time
import tty
import termios

from threading import Thread
from pylitinhos.model.Event import *

'''Código adaptado de: http://ballingt.com/nonblocking-stdin-in-python-3'''

class raw(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()
    def __enter__(self):
        self.original_stty = termios.tcgetattr(self.stream)
        tty.setcbreak(self.stream)
    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)

class nonblocking(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()
    def __enter__(self):
        self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)
    def __exit__(self, *args):
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)


def input_until(prompt='',call_continue=None, show_input=True):
    if prompt:
        print(prompt,end="",flush=True)

    return readline_until(call_continue, show_input)

def readline_until(call_continue=None, show_input=True):
    '''Lê de stdin até encontrar uma quebra de linha ou 'call_continue' retornar False.
        @param call_continue - um callable que recebe como entrada o que foi
            lido até então pela função e retorna se ela deve continuar a processar
        @param show_input - se True, imprime os caracteres lidos para stdout
    '''

    line = ''
    with raw(sys.stdin):
        with nonblocking(sys.stdin):
            while not call_continue or call_continue(line):
                try:
                    c = sys.stdin.read(1)
                    if c:
                        if show_input:
                            # sys.stdout.write(c)
                            print(c,end="",flush=True)
                        if c == '\n':
                            return line
                        else:
                            line += c
                    else: #No input
                        time.sleep(.1)
                except IOError: #No input - Python2
                    time.sleep(.1)

    return line

class InputAsync(Thread):
    def __init__(self, eventQueue, prompt=None):
        super(InputAsync, self).__init__()

        self.eventQueue = eventQueue
        self.prompt = prompt
        self.stopped = False

    def run(self):
        line = ''

        prompt_tmp = self.prompt
        while not line:
            line = input_until(prompt_tmp, lambda line: not self.stopped)
            #Evita usar de novo o prompt
            prompt_tmp = None

            if self.stopped:
                break

        if not self.stopped:
            self.eventQueue.put(Event(EventTypes.UserInput, line=line))

    def stop(self):
        self.stopped = True
