from Controller.AbstractAction import AbstractAction


class GiveUp(AbstractAction):
    def __init__(self):
        super(GiveUp, self).__init__()

    def do_action(self, context, parameters):
        pass

    def do_slot(self, context, parameters):
        pass
