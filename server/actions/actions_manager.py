from abc import ABCMeta, abstractmethod


class ActionManager(metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, message: str, players):
        pass
