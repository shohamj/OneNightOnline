from __future__ import annotations

from server.cards.card import Card


class Alien(Card):

    @classmethod
    async def is_winner(cls, io: GameIO, state: State) -> bool:
        return True

    @classmethod
    async def on_night(cls, io: GameIO, state: State) -> None:
        await io.send_message("Aliens wake up", [])
