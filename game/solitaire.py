import random
import json


class Card:
    """Represents a playing card with suit, rank, and visibility."""
    
    SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    def __init__(self, suit, rank, face_up=False):
        self.suit = suit
        self.rank = rank
        self.face_up = face_up
    
    @property
    def color(self):
        """Returns 'red' or 'black' based on suit."""
        return 'red' if self.suit in ['hearts', 'diamonds'] else 'black'
    
    @property
    def value(self):
        """Returns numeric value (1-13) for the card."""
        return self.RANKS.index(self.rank) + 1
    
    def to_dict(self):
        """Convert card to dictionary for JSON serialization."""
        return {
            'suit': self.suit,
            'rank': self.rank,
            'face_up': self.face_up,
            'color': self.color
        }
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"


class SolitaireGame:
    """Main game logic for Klondike Solitaire."""
    
    def __init__(self):
        self.deck = []
        self.waste = []
        self.foundations = {suit: [] for suit in Card.SUITS}
        self.tableau = [[] for _ in range(7)]
        self.setup_game()
    
    def setup_game(self):
        """Initialize and shuffle deck, deal cards to tableau."""
        # Create full deck
        self.deck = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        random.shuffle(self.deck)
        
        # Deal to tableau
        for col in range(7):
            for row in range(col + 1):
                card = self.deck.pop()
                if row == col:  # Last card in column is face up
                    card.face_up = True
                self.tableau[col].append(card)
    
    def draw_card(self):
        """Draw a card from deck to waste pile."""
        if self.deck:
            card = self.deck.pop()
            card.face_up = True
            self.waste.append(card)
            return True
        else:
            # Reset deck from waste
            self.deck = self.waste[::-1]
            for card in self.deck:
                card.face_up = False
            self.waste = []
            return True
    
    def can_move_to_foundation(self, card, foundation_pile):
        """Check if card can be moved to foundation."""
        if not foundation_pile:
            return card.rank == 'A'
        
        top_card = foundation_pile[-1]
        return (card.suit == top_card.suit and 
                card.value == top_card.value + 1)
    
    def can_move_to_tableau(self, card, tableau_pile):
        """Check if card can be moved to tableau column."""
        if not tableau_pile:
            return card.rank == 'K'
        
        top_card = tableau_pile[-1]
        return (card.color != top_card.color and 
                card.value == top_card.value - 1)
    
    def move_card(self, from_location, to_location, card_index=None):
        """
        Move card(s) from one location to another.
        Locations format: 'waste', 'tableau_0', 'foundation_hearts', etc.
        """
        # Parse source location
        if from_location == 'waste':
            if not self.waste:
                return False
            cards_to_move = [self.waste[-1]]
            source_pile = self.waste
        elif from_location.startswith('tableau_'):
            col = int(from_location.split('_')[1])
            if card_index is None or card_index >= len(self.tableau[col]):
                return False
            # Move card and all cards on top of it
            cards_to_move = self.tableau[col][card_index:]
            source_pile = self.tableau[col]
        elif from_location.startswith('foundation_'):
            suit = from_location.split('_')[1]
            if not self.foundations[suit]:
                return False
            cards_to_move = [self.foundations[suit][-1]]
            source_pile = self.foundations[suit]
        else:
            return False
        
        # Validate move
        card_to_check = cards_to_move[0]
        
        if to_location.startswith('foundation_'):
            if len(cards_to_move) > 1:
                return False
            suit = to_location.split('_')[1]
            if not self.can_move_to_foundation(card_to_check, self.foundations[suit]):
                return False
            target_pile = self.foundations[suit]
        elif to_location.startswith('tableau_'):
            col = int(to_location.split('_')[1])
            if not self.can_move_to_tableau(card_to_check, self.tableau[col]):
                return False
            target_pile = self.tableau[col]
        else:
            return False
        
        # Execute move
        for card in cards_to_move:
            source_pile.remove(card)
            target_pile.append(card)
        
        # Flip top card if needed
        if from_location.startswith('tableau_'):
            col = int(from_location.split('_')[1])
            if self.tableau[col] and not self.tableau[col][-1].face_up:
                self.tableau[col][-1].face_up = True
        
        return True
    
    def auto_move_to_foundation(self):
        """Automatically move any available cards to foundations."""
        moved = False
        
        # Try from waste
        if self.waste:
            card = self.waste[-1]
            for suit in Card.SUITS:
                if self.can_move_to_foundation(card, self.foundations[suit]):
                    self.move_card('waste', f'foundation_{suit}')
                    moved = True
                    break
        
        # Try from tableau
        for col in range(7):
            if self.tableau[col]:
                card = self.tableau[col][-1]
                if card.face_up:
                    for suit in Card.SUITS:
                        if self.can_move_to_foundation(card, self.foundations[suit]):
                            self.move_card(f'tableau_{col}', f'foundation_{suit}', 
                                         len(self.tableau[col]) - 1)
                            moved = True
                            break
                if moved:
                    break
        
        return moved
    
    def check_win(self):
        """Check if game is won (all cards in foundations)."""
        return all(len(pile) == 13 for pile in self.foundations.values())
    
    def get_state(self):
        """Get current game state as dictionary."""
        return {
            'deck_count': len(self.deck),
            'waste': [card.to_dict() for card in self.waste],
            'foundations': {
                suit: [card.to_dict() for card in pile]
                for suit, pile in self.foundations.items()
            },
            'tableau': [
                [card.to_dict() for card in pile]
                for pile in self.tableau
            ],
            'is_won': self.check_win()
        }
    
    def to_json(self):
        """Serialize game state to JSON."""
        state = {
            'deck': [{'suit': c.suit, 'rank': c.rank, 'face_up': c.face_up} for c in self.deck],
            'waste': [{'suit': c.suit, 'rank': c.rank, 'face_up': c.face_up} for c in self.waste],
            'foundations': {
                suit: [{'suit': c.suit, 'rank': c.rank, 'face_up': c.face_up} for c in pile]
                for suit, pile in self.foundations.items()
            },
            'tableau': [
                [{'suit': c.suit, 'rank': c.rank, 'face_up': c.face_up} for c in pile]
                for pile in self.tableau
            ]
        }
        return json.dumps(state)
    
    @classmethod
    def from_json(cls, json_str):
        """Deserialize game state from JSON."""
        game = cls.__new__(cls)
        state = json.loads(json_str)
        
        game.deck = [Card(c['suit'], c['rank'], c['face_up']) for c in state['deck']]
        game.waste = [Card(c['suit'], c['rank'], c['face_up']) for c in state['waste']]
        game.foundations = {
            suit: [Card(c['suit'], c['rank'], c['face_up']) for c in pile]
            for suit, pile in state['foundations'].items()
        }
        game.tableau = [
            [Card(c['suit'], c['rank'], c['face_up']) for c in pile]
            for pile in state['tableau']
        ]
        
        return game