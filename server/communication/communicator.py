from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import List


class Communicator(metaclass=ABCMeta):
    @abstractmethod
    async def send_message(self, message: str, players: List[Player]) -> None:
        pass

    @abstractmethod
    async def ask_question(self, question: str, possible_answers: List[str], player: Player) -> str:
        pass

    @abstractmethod
    async def answer_question(self, question_id: str, answers_index: int) -> None:
        pass

    @abstractmethod
    def set_vote(self, player: Player, votes: List[Player]) -> None:
        pass

    @abstractmethod
    async def get_votes(self, voting_players: List[Player]) -> List[Player]:
        pass

    @abstractmethod
    async def notify_winners(self, winning_cards: List[Card], winners: List[Player],
                             players_to_notify: List[Player]) -> None:
        pass
