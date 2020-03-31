from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import List


class ActionManager(metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, message: str, players: List[Player]) -> None:
        pass

    @abstractmethod
    def pause(self, seconds: int) -> None:
        pass

    @abstractmethod
    def vote(self, player: Player, votes: List[Player]) -> None:
        pass

    @abstractmethod
    def get_most_voted(self, voting_players: List[Player]) -> List[Player]:
        pass

    @abstractmethod
    def notify_most_voted(self, most_voted: List[Player], players_to_notify: List[Player]) -> None:
        pass
