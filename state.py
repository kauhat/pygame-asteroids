from controls import InputState


class GameState:
    def __init__(self):
        self.pending_exit = False
        self.is_paused = False

        self.input = InputState()
        self.input_previous = InputState()

        #
        self.frame_start_time = 0
        self.frame_end_time = 0

        self.show_frame_debug = False
        self.last_frame_debug = 0

    def update_input(self, input: InputState):
        if input.game_quit:
            print("Quitting...")
            self.pending_exit = True

        # Add current frame input map to state.
        self.input_previous = self.input
        self.input = input
