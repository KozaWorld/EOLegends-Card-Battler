import discord
from discord.ext import commands
import random
import asyncio

class BattleSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_challenges = {}

    @commands.command(name='challenge')
    async def challenge_player(self, ctx, opponent: discord.Member):
        """
        Challenge another player to a battle
        
        :param ctx: Discord command context
        :param opponent: Discord member to challenge
        """
        # Prevent self-challenge
        if ctx.author == opponent:
            await ctx.send("You can't challenge yourself!")
            return
        
        # Get players
        challenger = self.bot.get_or_create_player(ctx.author.id, ctx.author.name)
        challenged = self.bot.get_or_create_player(opponent.id, opponent.name)
        
        # Check if players have cards
        if not challenger.collection or not challenged.collection:
            await ctx.send("Both players must have cards to battle. Use !join first!")
            return
        
        # Send challenge invitation
        challenge_embed = discord.Embed(
            title="Battle Challenge!", 
            description=f"{ctx.author.name} challenges {opponent.mention} to a card battle!",
            color=discord.Color.red()
        )
        challenge_message = await ctx.send(embed=challenge_embed)
        
        # Add challenge to active challenges
        self.active_challenges[opponent.id] = {
            'challenger': ctx.author,
            'message': challenge_message
        }
        
        # Wait for response
        def check(reaction, user):
            return (user == opponent and 
                    str(reaction.emoji) in ['✅', '❌'] and 
                    reaction.message.id == challenge_message.id)
        
        # Add reaction buttons
        await challenge_message.add_reaction('✅')
        await challenge_message.add_reaction('❌')
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            
            if str(reaction.emoji) == '❌':
                await ctx.send(f"{opponent.name} declined the battle!")
                return
            
            # Start battle
            battle = CardBattle(challenger, challenged, self.bot.card_collection)
            self.bot.active_battles[ctx.channel.id] = battle
            
            winner, loser = await battle.start_battle(ctx)
            
            # Award tokens and potentially steal a card
            if loser.collection:
                stolen_card = random.choice(loser.collection)
                loser.remove_card(stolen_card)
                winner.add_card(stolen_card)
                
                # Notify about card theft
                card = self.bot.card_collection.get_card_by_id(stolen_card)
                await ctx.send(f"🏆 {winner.username} wins the battle and steals {card.name} from {loser.username}!")
            else:
                await ctx.send(f"🏆 {winner.username} wins the battle!")
        
        except asyncio.TimeoutError:
            await ctx.send(f"Battle challenge to {opponent.name} has expired.")
        finally:
            # Clean up challenge message
            await challenge_message.delete()

    @commands.command(name='mydeck')
    async def view_deck(self, ctx):
        """
        View player's current battle deck
        
        :param ctx: Discord command context
        """
        player = self.bot.get_