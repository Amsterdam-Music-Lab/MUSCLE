from django.utils.translation import gettext_lazy as _
import json

class Player(object):
    ''' An object defining a single player '''
    def __init__(self, section, player_type, config):
        self.id = section.id
        self.url = section.absolute_url()
        self.player_type = player_type
        self.config = config
  
    def action(self):
        return self.__dict__


class Players(object):
    ''' An array of players '''
    def __init__(self, players):
        self.players = players

    def action(self):
        serialized_players = [player.action() for player in self.players]
        return {
            'players': serialized_players
        }