"""
Team Performance Analysis Module
Calculates team strength ratings and performance metrics
"""

import math
from datetime import datetime, timedelta
from database import SessionLocal
from models.database_schema import Team, Game
from typing import Dict, List, Tuple

class TeamPerformanceAnalyzer:
    """Analyzes team performance using multiple metrics"""

    def __init__(self):
        self.db = SessionLocal()
        self.initial_elo = 1500  # Starting ELO rating
        self.k_factor = 32       # ELO adjustment rate

    def calculate_elo_ratings(self) -> Dict[int, float]:
        """Calculate ELO ratings for all teams"""
        # Initialize all teams with starting ELO
        teams = self.db.query(Team).all()
        elo_ratings = {team.id: self.initial_elo for team in teams}

        # Get all completed games (for now, we'll simulate some results)
        # In real app, you'd have actual match results
        completed_games = self.get_simulated_results()

        # Process games chronologically to update ELO
        for game in sorted(completed_games, key=lambda x: x['date']):
            home_id, away_id = game['home_team_id'], game['away_team_id']
            home_score, away_score = game['home_score'], game['away_score']

            # Current ELO ratings
            home_elo = elo_ratings[home_id]
            away_elo = elo_ratings[away_id]

            # Expected scores
            home_expected = 1 / (1 + math.pow(10, (away_elo - home_elo) / 400))
            away_expected = 1 - home_expected

            # Actual results (1 = win, 0.5 = draw, 0 = loss)
            if home_score > away_score:
                home_actual, away_actual = 1, 0
            elif home_score < away_score:
                home_actual, away_actual = 0, 1
            else:
                home_actual, away_actual = 0.5, 0.5

            # Update ELO ratings
            elo_ratings[home_id] += self.k_factor * (home_actual - home_expected)
            elo_ratings[away_id] += self.k_factor * (away_actual - away_expected)

        return elo_ratings

    def get_simulated_results(self) -> List[Dict]:
        """Simulate past match results for testing"""
        import random
        teams = self.db.query(Team).all()

        simulated_games = []

        # Generate 50 random past games
        for _ in range(50):
            home_team = random.choice(teams)
            away_team = random.choice([t for t in teams if t.id != home_team.id])

            # Simulate realistic score
            home_score = random.choices([0, 1, 2, 3, 4], weights=[10, 25, 30, 20, 5])[0]
            away_score = random.choices([0, 1, 2, 3, 4], weights=[15, 30, 25, 15, 5])[0]

            simulated_games.append({
                'home_team_id': home_team.id,
                'away_team_id': away_team.id,
                'home_score': home_score,
                'away_score': away_score,
                'date': datetime.now() - timedelta(days=random.randint(1, 365))
            })

        return simulated_games

    def analyze_team_performance(self, team_id: int) -> Dict:
        """Complete performance analysis for a team"""
        team = self.db.query(Team).filter(Team.id == team_id).first()

        if not team:
            return {"error": "Team not found"}

        # Get ELO rating
        elo_ratings = self.calculate_elo_ratings()

        analysis = {
            'team_name': team.name,
            'league': team.league,
            'elo_rating': round(elo_ratings.get(team_id, 1500), 1),
            'performance_tier': self.classify_performance_tier(elo_ratings.get(team_id, 1500))
        }

        return analysis

    def classify_performance_tier(self, elo_rating: float) -> str:
        """Classify team into performance tier"""
        if elo_rating >= 1700:
            return "Elite"
        elif elo_rating >= 1600:
            return "Strong"
        elif elo_rating >= 1400:
            return "Average"
        else:
            return "Weak"

    def close(self):
        self.db.close()

if __name__ == "__main__":
    analyzer = TeamPerformanceAnalyzer()

    print("TEAM PERFORMANCE ANALYSIS")
    print("=" * 40)

    # Analyze first few teams
    teams = analyzer.db.query(Team).limit(3).all()

    for team in teams:
        analysis = analyzer.analyze_team_performance(team.id)

        print(f"\n{analysis['team_name']} ({analysis['league']})")
        print(f"ELO Rating: {analysis['elo_rating']} ({analysis['performance_tier']})")

    analyzer.close()
    print("\n" + "=" * 40)
    print("Team Performance Analyzer ready!")
