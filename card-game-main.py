import discord
from discord.ext import commands
import json
import random
import asyncio
from typing import List, Dict, Optional, Any

# Import the other classes and components
from card_collection import Card, CardCollection
from player import Player
from card_battle import CardBattle
from shop import Shop, ShopItem

class CardBattleBot(commands.Bot):
    def __init__(self):
        """
        Initialize the Card Battle Discord Bot
        """
        # Configure intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        # Call parent constructor
        super().__init__(
            command_prefix='!', 
            intents=intents,
            help_command=commands.DefaultHelpCommand()
        )

        # Initialize game components
        self.card_collection = CardCollection()
        self.shop = Shop()
        self.players: Dict[int, Player] = {}
        self.active_battles: Dict[int, CardBattle] = {}

    async def setup_hook(self):
        """
        Bot setup method to load cogs and prepare game
        """
        # Load game cogs
        await self.load_extension('cogs.player_management')
        await self.load_extension('cogs.battle_system')
        await self.load_extension('cogs.shop_system')
        
        print("Bot is initializing...")

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

    async def on_ready(self):
        """
        Confirm bot is ready and print connection details
        """
        print(f'Logged in as {self.user}')
        print(f'Connected to {len(self.guilds)} guilds')

def main():
    # Load bot token from a secure file or environment variable
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Initialize and run the bot
    bot = CardBattleBot()
    bot.run(config['bot_token'])

if __name__ == "__main__":
    main()