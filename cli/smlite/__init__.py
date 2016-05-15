from .init_state import InitState

STATES = {
    'init': InitState()
}


def get_state(state):
    global STATES
    return STATES[state]


class SmLite(object):

    def start(self, init_state, args={}):
        keep_running = True
        current_state = init_state
        current_args = args
        while keep_running:
            result = get_state(current_state).run(current_args)

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
