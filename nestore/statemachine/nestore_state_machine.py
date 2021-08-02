from mystates import SleepState

class NestoreSM(object):
    """ 
    A simple state machine that mimics the functionality of a device from a 
    high level.
    """

    def __init__(self):
        """ Initialize the components. """

        # Start with a default state.
        self.state = SleepState()
        
  

    def on_event(self, event):

        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)
