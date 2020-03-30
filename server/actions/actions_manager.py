from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import List


class ActionManager(metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, message: str, players: List[Player]):
        pass
