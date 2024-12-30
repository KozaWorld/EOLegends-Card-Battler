# EOLegends-Card-Battler

EOLegends-Card-Battler is a Discord bot that allows users to collect cards, battle each other, and buy items from a shop. The bot is modular and can be easily extended with additional features.

## Features

- **Card Collection**: Users can collect various cards with different attributes.
- **Battles**: Users can challenge each other to card battles.
- **Shop**: Users can buy items from the shop to enhance their card collection.

## Setup

### Prerequisites

- Python 3.7+
- Discord Bot Token
- Required Python packages (listed in `requirements.txt`)

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/KozaWorld/EOLegends-Card-Battler.git
    cd EOLegends-Card-Battler
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Configure the bot**:
    - Create a `config.json` file with your bot token:
      ```json
      {
          "bot_token": "your_discord_token_here"
      }
      ```

4. **Run the bot**:
    ```sh
    python bot.py
    ```

## Usage

1. **Collect Cards**: Users can collect new cards by using the `!collect` command.
2. **Battle**: Users can challenge others to battles using the `!battle @opponent` command.
3. **Shop**: Users can buy items from the shop using commands provided by the shop system.

## Project Structure

- `bot.py`: Main bot script that initializes and runs the bot.
- `card_collection.py`: Contains the `Card` and `CardCollection` classes.
- `player.py`: Contains the `Player` class.
- `card_battle.py`: Contains the `CardBattle` class.
- `shop.py`: Contains the `Shop` and `ShopItem` classes.
- `cogs/`: Directory containing the bot's cogs (player management, battle system, shop system).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py) for the Discord API wrapper