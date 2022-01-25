class Playback(object):
    ''' A playback wrapper for different kinds of players '''
    def __init__(self, player_type, sections, instructions, config):
        self.player_type = player_type
        self.sections = sections
        self.instuctions = instructions
        self.config = config