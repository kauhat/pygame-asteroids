import controls

class GameState:
    def __init__(self):
        self.pendingExit = False

        self.input = controls.InputState()
        self.input_previous = controls.InputState()
