from __future__ import annotations

from server.cards.card import Card


class Alien(Card):
    @classmethod
    async def is_winner(cls, communicator: Communicator, state: State) -> bool:
        return True

    @classmethod
    async def on_night(cls, communicator: Communicator, state: State) -> None:
        alien_players = [player for player in state.players if cls.main_type() in player.card.get_types()]
        await communicator.send_message("Aliens wake up", alien_players)
