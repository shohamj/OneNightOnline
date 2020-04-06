class State:
    def __init__(self, players, cards):
        self.players = players
        self.cards = cards
        self.center_cards = []
        self.declared_cards = []
        self.winning_cards = []
        self.dead = []
        self.votes = {}
