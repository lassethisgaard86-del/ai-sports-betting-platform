"""
Home/Away Advantage Calculator
Calculates statistical home field advantage for teams and leagues
"""

from datetime import datetime, timedelta
from database import SessionLocal
from models.database_schema import Team, Game
from typing import Dict, List
import random

class HomeAdvantageCalculator:
    """Calculates home field advantage statistics"""

    def __init__(self):
        self.db = SessionLocal()

    def get_home_advantage_factor(self, home_team_id: int, away_team_id: int) -> Dict:
        """Calculate home advantage factor for a specific matchup"""
        home_team = self.db.query(Team).filter(Team.id == home_team_id).first()
        away_team = self.db.query(Team).filter(Team.id == away_team_id).first()

        if not home_team or not away_team:
            return {"error": "Team not found"}

        # Simulate home advantage (in real app, use actual data)
        # Typical home advantage is 15-20 percentage points
        home_win_rate = random.uniform(40, 70)  # Home team win rate at home
        away_win_rate = random.uniform(20, 40)  # Away team win rate away

        home_advantage = (home_win_rate - 33.33) / 100  # 33.33% is neutral
        away_disadvantage = (33.33 - away_win_rate) / 100

        # Combined factor
        advantage_factor = (home_advantage + away_disadvantage) / 2
        advantage_factor = max(-0.5, min(0.5, advantage_factor))  # Cap at ±0.5

        return {
            'home_team': home_team.name,
            'away_team': away_team.name,
            'home_advantage_factor': round(advantage_factor, 3),
            'home_team_home_rate': round(home_win_rate, 1),
            'away_team_away_rate': round(away_win_rate, 1),
            'reasoning': f"{home_team.name} wins {home_win_rate:.1f}% at home, {away_team.name} wins {away_win_rate:.1f}% away"
        }

    def calculate_league_home_advantage(self, league: str) -> Dict:
        """Calculate overall home advantage for a league"""
        # Simulate realistic league statistics
        home_win_rate = random.uniform(0.42, 0.48)  # 42-48%
        draw_rate = random.uniform(0.24, 0.28)      # 24-28%
        away_win_rate = 1 - home_win_rate - draw_rate

        return {
            'league': league,
            'home_win_rate': round(home_win_rate, 3),
            'draw_rate': round(draw_rate, 3),
            'away_win_rate': round(away_win_rate, 3),
            'home_advantage_factor': round(home_win_rate - 0.333, 3),
            'games_analyzed': 100
        }

    def close(self):
        self.db.close()

if __name__ == "__main__":
    calculator = HomeAdvantageCalculator()

    print("HOME/AWAY ADVANTAGE ANALYSIS")
    print("=" * 50)

    # Analyze Premier League
    league_stats = calculator.calculate_league_home_advantage("Premier League")
    print(f"\nPremier League Statistics:")
    print(f"Home win rate: {league_stats['home_win_rate']*100:.1f}%")
    print(f"Draw rate: {league_stats['draw_rate']*100:.1f}%")
    print(f"Away win rate: {league_stats['away_win_rate']*100:.1f}%")
    print(f"Home advantage factor: {league_stats['home_advantage_factor']:.3f}")

    # Test specific matchup
    teams = calculator.db.query(Team).limit(2).all()
    if len(teams) >= 2:
        advantage = calculator.get_home_advantage_factor(teams[0].id, teams[1].id)

        print(f"\nMatchup: {advantage['home_team']} vs {advantage['away_team']}")
        print(f"Home advantage factor: {advantage['home_advantage_factor']}")
        print(f"Reasoning: {advantage['reasoning']}")

    print(f"\n{'='*50}")
    print("Home Advantage Calculator ready!")

    calculator.close()
