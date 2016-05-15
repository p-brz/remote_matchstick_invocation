class SmLite(object):
    def __init__(self):
        self.states = {}

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def get_state(self, state_name):
        return self.states[state_name]

    def start(self, init_state, args={}):
        keep_running = True
        current_state = init_state
        current_args = args
        while keep_running:
            result = self.get_state(current_state).run(current_args)

            if isinstance(result, tuple):
                r_state, r_args = result
            else:
                r_state = result
                r_args = {}

            if r_state is False:
                keep_running = False
            else:
                current_state = r_state
                current_args = r_args
