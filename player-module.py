import json
from typing import List, Dict

class Player:
    def __init__(self, user_id: int, username: str):
        """
        Initialize a player's game profile
        
        :param user_id: Discord user ID
        :param username: Discord username
        """
        self.user_id = user_id
        self.username = username
        
        # Player collection and stats
        self.collection: List[str] = []  # List of card IDs
        self.battle_tokens = 200  # Starting tokens
        
        # Battle and progression tracking
        self.battle_stats = {
            'wins': 0,
            'losses': 0,
            'total_battles': 0,
            'total_experience': 0,
            'level': 1
        }
        
        # Deck management
        self.current_deck: List[str] = []
        
        # Timestamps and cooldowns
        self.last_daily_claim = None
        self.battle_cooldown = None

    def add_card(self, card_id: str):
        """
        Add a card to player's collection
        
        :param card_id: ID of the card to add
        """
        if card_id not in self.collection:
            self.collection.append(card_id)
        
        # Update player level based on collection size
        self.update_level()

    def remove_card(self, card_id: str):
        """
        Remove a card from player's collection
        
        :param card_id: ID of the card to remove
        """
        if card_id in self.collection:
            self.collection.remove(card_id)

    def add_tokens(self, amount: int):
        """
        Add battle tokens to player's balance
        
        :param amount: Number of tokens to add
        """
        self.battle_tokens += amount

    def update_level(self):
        """
        Update player level based on collection and experience
        """
        # Simple leveling formula
        collection_size = len(self.collection)
        self.battle_stats['level'] = min(max(1, collection_size // 5), 50)

    def to_dict(self) -> Dict:
        """
        Convert player data to dictionary for saving
        
        :return: Dictionary representation of player
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'collection': self.collection,
            'battle_tokens': self.battle_tokens,
            'battle_stats': self.battle_stats,
            'current_deck': self.current_deck
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Create a player instance from saved dictionary data
        
        :param data: Dictionary containing player data
        :return: Player instance
        """
        player = cls(data['user_id'], data['username'])
        player.collection = data.get('collection', [])
        player.battle_tokens = data.get('battle_tokens', 200)
        player.battle_stats = data.get('battle_stats', {
            'wins': 0,
            'losses': 0,
            'total_battles': 0,
            'total_experience': 0,
            'level': 1
        })
        player.current_deck = data.get('current_deck', [])
        return player

class PlayerManager:
    def __init__(self, save_file: str = 'players.json'):
        """
        Initialize player management system
        
        :param save_file: File to save and load player data
        """
        self.save_file = save_file
        self.players: Dict[int, Player] = {}
        self.load_players()

    def load_players(self):
        """
        Load player data from JSON file
        """
        try:
            with open(self.save_file, 'r') as f:
                player_data = json.load(f)
                self.players = {
                    int(user_id): Player.from_dict(data) 
                    for user_id, data in player_data.items()
                }
        except FileNotFoundError:
            self.players = {}

    def save_players(self):
        """
        Save player data to JSON file
        """
        player_data = {
            str(player.user_id): player.to_dict() 
            for player in self.players.values()
        }
        
        with open(self.save_file, 'w') as f:
            json.dump(player_data, f, indent=2)

    def get_or_create_player(self, user_id: int, username: str) -> Player:
        """
        Get existing player or create a new one
        
        :param user_id: Discord user ID
        :param username: Discord username
        :return: Player object
        """
        if user_id not in self.players:
            self.players[user_id] = Player(user_id, username)
        return self.players[user_id]