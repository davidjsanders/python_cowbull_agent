import abc
import logging
from abc import ABCMeta


class AbstractAction(object):
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def do_action(self, context, parameters):
        return

    @abc.abstractmethod
    def do_slot(self, context, parameters):
        return
