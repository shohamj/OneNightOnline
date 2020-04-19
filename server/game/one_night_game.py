from __future__ import annotations

import random
from abc import abstractmethod
from collections import Counter
from typing import List, Dict

from server.exceptions.one_night_exception import OneNightException
from server.game.state import State

NUM_OF_CENTER_CARDS = 3


class OneNightGame:
    def __init__(self, players: List[Player], cards: List[Card], communicator: Communicator) -> None:
        if len(players) + NUM_OF_CENTER_CARDS != len(cards):
            raise OneNightException(f"Can't create a game with {len(players)} players and {len(cards)} cards")
        self._state = State(players, cards)
        self._communicator = communicator

    @property
    @abstractmethod
    def night_order(self) -> List[Card]:
        return []

    @property
    def death_order(self) -> List[Card]:
        return self.night_order

    @property
    def win_order(self) -> List[Card]:
        return self.night_order

    async def night_phase(self) -> None:
        for card in self.night_order:
            if card.should_wake_up(self._communicator, self._state):
                await card.on_night(self._communicator, self._state)

    async def voting_phase(self) -> None:
        self._state.votes = await self._communicator.get_votes(self._state.players)
        self._state.dead = self.get_most_voted_players(self._state.votes)

    async def death_phase(self) -> None:
        for dead_player in sorted(self._state.dead, key=lambda player: self.death_order.index(player.card)):
            dead_player.card.on_death(self._communicator, self._state)

    async def winning_phase(self) -> None:
        for card in self.win_order:
            if await card.is_winner(self._communicator, self._state):
                self._state.winning_cards.append(card)
                await card.on_win(self._communicator, self._state)
        winners = [player for player in self._state.players if player.card in self._state.winning_cards]
        await self._communicator.notify_winners(self._state.winning_cards, winners, self._state.players)

    async def hand_out_cards(self) -> None:
        random.shuffle(self._state.cards)
        self._state.center_cards = self._state.cards[:NUM_OF_CENTER_CARDS]
        players_cards = self._state.cards[NUM_OF_CENTER_CARDS:]
        for player, card in zip(self._state.players, players_cards):
            player.set_card(card)

    @staticmethod
    def get_most_voted_players(votes: Dict[Player, List[Players]]):
        if not votes:
            return []
        counted_votes = Counter(votes)
        ordered_counted_votes = counted_votes.most_common(len(counted_votes))
        # Each element is a tuple of (Player, total_votes) and the first has the highest number of votes
        highest_votes = ordered_counted_votes[0][1]
        # Return all the players with the highest number of votes
        return [player for player, total_votes in ordered_counted_votes if total_votes == highest_votes]

    def answer(self, question_id: str, answer_index: int) -> None:
        self._communicator.answer_question(question_id, answer_index)

    def vote(self, player: Player, votes: List[Player]) -> None:
        self._communicator.set_vote(player, votes)

    async def run(self) -> None:
        await self.hand_out_cards()
        await self.night_phase()
        await self.voting_phase()
        await self.death_phase()
        await self.winning_phase()
