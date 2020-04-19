from __future__ import annotations

import asyncio
import uuid
from typing import List, Dict

from server.communication.communicator import Communicator
from server.exceptions.one_night_exception import OneNightException


class SocketIOCommunicator(Communicator):
    def __init__(self, server: AsyncServer, socket_to_player: Dict[str, Player],
                 player_to_socket: Dict[Player, str]) -> None:
        self._server = server
        self._socket_to_player = socket_to_player
        self._player_to_socket = player_to_socket
        self._questions_events = {}
        self._answered_questions = {}
        self._votes_events = {}
        self._votes = {}

    async def send_message(self, message: str, players: List[Player]) -> None:
        if not players:
            return
        emit_message_tasks = [self._server.emit("message", {"message": message}, room=self._player_to_socket[player])
                              for player in players]
        await asyncio.wait(emit_message_tasks)

    async def ask_question(self, question: str, possible_answers: List[str], player: Player) -> str:
        question_id = uuid.uuid4().hex
        self._questions_events[question_id] = asyncio.Event()
        await self._server.emit("question",
                                {"question_id": question_id,
                                 "question": question,
                                 "answers": possible_answers},
                                room=self._player_to_socket[player])
        await self._questions_events[question_id].wait()
        return self._answered_questions[question_id]

    def answer_question(self, question_id: str, answer_index: int):
        self._answered_questions[question_id] = answer_index
        self._questions_events[question_id].set()

    def set_vote(self, player: Player, votes: List[Player]) -> None:
        if player in self._votes:
            raise OneNightException("Player has already voted")
        if len(votes) != player.card.get_num_of_votes():
            raise OneNightException(f"Player has {player.card.get_num_of_votes()} votes but {len(votes)} received")
        if player in self._votes_events:
            self._votes_events[player].set()
        self._votes = {player: votes}

    async def get_votes(self, voting_players: List[Player]) -> List[Player]:
        await self.wait_for_votes(voting_players)
        return self._votes

    async def wait_for_votes(self, voting_players: List[Player], timeout: int = None) -> None:
        for player in voting_players:
            self._votes_events[player] = asyncio.Event()
        for already_voted_player in self._votes:
            self._votes_events[already_voted_player].set()
        await asyncio.wait([event.wait() for event in self._votes_events.values()], timeout=timeout)

    async def notify_winners(self, winning_cards: List[Card], winners: List[Player],
                             players_to_notify: List[Player]) -> None:
        if not players_to_notify:
            return
        winners_ids = [winner.id for winner in winners]
        winning_cards_names = [card.main_type() for card in winning_cards]
        game_over_data = {"winners": winners_ids, "winning_cards": winning_cards_names}
        notify_winners_tasks = [self._server.emit("game_over", game_over_data, room=self._player_to_socket[player])
                                for
                                player in players_to_notify]
        await asyncio.wait(notify_winners_tasks)
