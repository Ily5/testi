class Logic:

    def __init__(self, name=None):
        self.name = name
        self.actions = ['playback', ' ', 'hangup', 'goto', 'recall', 'sleep', 'bridge', 'set', 'send_data', 'if', 'say',
                        'play_and_detect', 'get_initial_data']
