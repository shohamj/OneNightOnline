class State:
    def __init__(self, players, cards):
        self.players = players
        self.cards = cards
        self.center_cards = []
        self.declared_cards = []
        self.winners = []
        self.dead = []
        self.votes = {}
