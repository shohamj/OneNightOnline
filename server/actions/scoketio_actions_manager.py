from __future__ import annotations

import asyncio
from collections import Counter
from typing import List, Dict

from server.actions.actions_manager import ActionManager
from server.exceptions.one_night_exception import OneNightException


class SocketIOActionManager(ActionManager):
    def __init__(self, socket_io_server: AsyncServer, socket_to_player: Dict[str, Player],
                 player_to_socket: Dict[Player, str]) -> None:
        self._socket_io_server = socket_io_server
        self._socket_to_player = socket_to_player
        self._player_to_socket = player_to_socket
        self._votes = {}
        self._votes_events = {}

    async def send_message(self, message: str, players: List[Player]) -> None:
        for player in players:
            await self._socket_io_server.emit("message", {"message": message}, room=self._player_to_socket[player])

    async def pause(self, seconds: int) -> None:
        await asyncio.sleep(seconds)

    def vote(self, player: Player, votes: List[Player]) -> None:
        if player in self._votes:
            raise OneNightException("Player has already voted")
        if len(votes) != player.card.num_of_votes:
            raise OneNightException(f"Player has {player.card.num_of_votes} votes but {len(votes)} received")
        if player in self._votes_events:
            self._votes_events[player].set()
        self._votes = {player: votes}

    async def wait_for_votes(self, voting_players: List[Player], timeout: int = None) -> None:
        for player in voting_players:
            self._votes_events[player] = asyncio.Event()
        for already_voted_player in self._votes:
            self._votes_events[already_voted_player].set()
        await asyncio.wait([event.wait() for event in self._votes_events.values()], timeout=timeout)

    async def get_most_voted(self, voting_players: List[Player]) -> List[Player]:
        await self.wait_for_votes(voting_players)
        counted_votes = Counter(self._votes)
        ordered_counted_votes = counted_votes.most_common(len(counted_votes))
        # Each element is a tuple of (Player, total_votes) and the first has the highest number of votes
        highest_votes = ordered_counted_votes[0][1]
        # Return all the players with the highest number of votes
        return [player for player, total_votes in ordered_counted_votes if total_votes == highest_votes]

    async def notify_most_voted(self, most_voted: List[Player], players_to_notify: List[Player]) -> None:
        most_voted_ids = [player.id for player in most_voted]
        await asyncio.wait([
            self._socket_io_server.emit("most_voted", {"players": most_voted_ids}, room=self._player_to_socket[player])
            for player in players_to_notify])
