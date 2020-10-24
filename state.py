from controls import InputState


class GameState:
    def __init__(self):
        self.pendingExit = False

        self.input = InputState()
        self.input_previous = InputState()

        #
        self.frame_start_time = 0
        self.frame_end_time = 0

    def update_input(self, input: InputState):
        if input.game_quit:
            print("Quitting...")
            self.pendingExit = True

        # Add current frame input map to state.
        self.input_previous = self.input
        self.input = input
