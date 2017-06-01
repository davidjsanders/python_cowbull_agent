import abc
import logging
from abc import ABCMeta


class AbstractAction(object):
    """An abstract class to provide an interface to action fulfillment (and slot filling) for
    API.ai webhooks.

    Concrete classes must provide implementations of do_action (fulfillment) and do_slot (slot
    filling).

    NOTE: The concrete class MUST be the same name (identical) to the API.ai action; for example,
    if the action is called NewGame then the class must be called NewGame in a file called NewGame.py.
    If it is not, then an error will be reported back to the user that the action has not been
    implemented.
    """
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def do_action(self, context, parameters):
        """Action fulfillment"""
        return

    @abc.abstractmethod
    def do_slot(self, context, parameters):
        """Slot filling"""
        return
