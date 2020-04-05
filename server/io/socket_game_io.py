from __future__ import annotations

from typing import List

from server.io.game_io import GameIO


class SocketGameIO(GameIO):
    async def send_message(self, message: str, players: List[Player]) -> None:
        print(message)

    async def ask_question(self, question: str, possible_answers: List[str], players: List[Player]) -> str:
        return ""

    async def set_vote(self, player: Player, votes: List[Player]) -> None:
        pass

    async def get_votes(self, voting_players: List[Player]) -> List[Player]:
        return []

    async def notify_winners(self, winners: List[Player], players_to_notify: List[Player]) -> None:
        print(winners)
