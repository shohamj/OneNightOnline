from server.cards.card import Card
from server.games.one_night_game import OneNightGame


class Alien(Card):
    async def play(self, game: OneNightGame):
        aliens = [player for player in game.players if isinstance(player.card, Alien)]
        await game.action_manager.send_message("Aliens, open your eyes", aliens)
        await game.action_manager.send_message("Aliens, look at other aliens", aliens)
        await game.action_manager.send_message("Aliens, close your eyes", aliens)
