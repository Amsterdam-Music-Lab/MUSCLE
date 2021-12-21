from django.utils.translation import gettext_lazy as _
import json

class Player(object):
    ''' An object defining a single player '''
    def __init__(self, section, player_type, config=None):
        self.id = section.id
        self.url = section.absolute_url()
        self.player_type = player_type

  
    def action(self):
        return self.__dict__


class Players(object):
    ''' An array of players '''
    def __init__(self, players):
        self.players = players

    def action(self, config={}):
        serialized_players = [player.action() for player in self.players]
        self.config =  {
            'ready_time': 0,
            'decision_time': 5,
            'auto_play': True,
            'time_pass_break': False,
            'show_animation': False
        }
        self.config.update(config)
        return {
            'players': serialized_players
        }