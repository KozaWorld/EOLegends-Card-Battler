import json
import random
from typing import List, Dict, Optional

class Card:
    def __init__(self, card_data: Dict):
        """
        Initialize a card with comprehensive details
        
        :param card_data: Dictionary containing card details
        """
        self.id = card_data.get('id', 'unknown')
        self.name = card_data.get('name', 'Unnamed Card')
        
        # Core battle stats
        stats = card_data.get('stats', {})
        self.attack = stats.get('attack', 0)
        self.defense = stats.get('defense', 0)
        self.health = stats.get('health', 100)
        
        # Additional card attributes
        self.type = card_data.get('type', 'Generic')
        self.rarity = card_data.get('rarity', 'Common')
        self.element = card_data.get('element', 'Neutral')
        
        # Battle runtime attribute
        self.current_hp = self.health

    def to_dict(self) -> Dict:
        """
        Convert card to dictionary for serialization
        
        :return: Dictionary representation of the card
        """
        return {
            'id': self.id,
            'name': self.name,
            'stats': {
                'attack': self.attack,
                'defense': self.defense,
                'health': self.health
            },
            'type': self.type,
            'rarity': self.rarity,
            'element': self.element
        }

    def create_embed(self, ctx) -> discord.Embed:
        """
        Create a Discord embed to display card details
        
        :param ctx: Discord context for additional styling
        :return: Discord Embed object
        """
        embed = discord.Embed(
            title=f"{self.name}",
            description=f"**Type**: {self.type} | **Rarity**: {self.rarity}",
            color=self.get_rarity_color()
        )
        
        embed.add_field(name="Attack", value=self.attack, inline=True)
        embed.add_field(name="Defense", value=self.defense, inline=True)
        embed.add_field(name="Health", value=self.health, inline=True)
        
        return embed

    def get_rarity_color(self) -> discord.Color:
        """
        Assign color based on card rarity
        
        :return: Discord Color object
        """
        rarity_colors = {
            'Legendary': discord.Color.gold(),
            'Epic': discord.Color.purple(),
            'Rare': discord.Color.blue(),
            'Common': discord.Color.light_grey()
        }
        return rarity_colors.get(self.rarity, discord.Color.default())

class CardCollection:
    def __init__(self, cards_file: str = 'cards.json'):
        """
        Load card collection from a JSON file
        
        :param cards_file: Path to the JSON file containing card data
        """
        with open(cards_file, 'r') as f:
            data = json.load(f)
        
        # Convert card data to Card objects
        self.cards: List[Card] = [Card(card_data) for card_data in data.get('cards', [])]
        self.metadata = data.get('game_metadata', {})

    def get_random_cards(self, count: int = 10, rarity: Optional[str] = None) -> List[Card]:
        """
        Get a specified number of random cards, optionally filtered by rarity
        
        :param count: Number of cards to retrieve
        :param rarity: Optional rarity filter
        :return: List of Card objects
        """
        if rarity:
            filtered_cards = [card for card in self.cards if card.rarity.lower() == rarity.lower()]
        else:
            filtered_cards = self.cards
        
        return random.sample(filtered_cards, min(count, len(filtered_cards)))

    def get_card_by_id(self, card_id: str) -> Optional[Card]:
        """
        Find a card by its ID
        
        :param card_id: Unique identifier of the card
        :return: Card object or None
        """
        for card in self.cards:
            if card.id.lower() == card_id.lower():
                return card
        return None

    def get_cards_by_rarity(self, rarity: str) -> List[Card]:
        """
        Get all cards of a specific rarity
        
        :param rarity: Rarity to filter
        :return: List of Card objects
        """
        return [card for card in self.cards if card.rarity.lower() == rarity.lower()]