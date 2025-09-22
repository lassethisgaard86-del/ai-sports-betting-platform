"""
Head-to-Head Historical Analysis
Analyzes how teams perform against specific opponents
"""

from datetime import datetime, timedelta
from database import SessionLocal
from models.database_schema import Team, Game
from typing import Dict, List
import random

class HeadToHeadAnalyzer:
    """Analyzes historical matchups between teams"""

    def __init__(self):
        self.db = SessionLocal()

    def get_head_to_head_record(self, home_team_id: int, away_team_id: int, games_limit: int = 10) -> Dict:
        """Get historical record between two teams"""
        # Simulate historical matchups for testing
        historical_games = self.get_simulated_h2h_games(home_team_id, away_team_id, games_limit)

        if not historical_games:
            return {
                'total_games': 0,
                'home_wins': 0,
                'draws': 0,
                'away_wins': 0,
                'home_win_percentage': 0,
                'average_goals_home': 0,
                'average_goals_away': 0,
                'recent_trend': 'No data',
                'games_analyzed': []
            }

        # Analyze results
        home_wins = sum(1 for game in historical_games if game['home_score'] > game['away_score'])
        draws = sum(1 for game in historical_games if game['home_score'] == game['away_score'])
        away_wins = sum(1 for game in historical_games if game['home_score'] < game['away_score'])

        total_games = len(historical_games)
        home_win_percentage = (home_wins / total_games * 100) if total_games > 0 else 0

        # Calculate average goals
        total_home_goals = sum(game['home_score'] for game in historical_games)
        total_away_goals = sum(game['away_score'] for game in historical_games)

        avg_home_goals = total_home_goals / total_games if total_games > 0 else 0
        avg_away_goals = total_away_goals / total_games if total_games > 0 else 0

        return {
            'total_games': total_games,
            'home_wins': home_wins,
            'draws': draws,
            'away_wins': away_wins,
            'home_win_percentage': round(home_win_percentage, 1),
            'average_goals_home': round(avg_home_goals, 2),
            'average_goals_away': round(avg_away_goals, 2),
            'recent_trend': self.analyze_recent_trend(historical_games[:3]),
            'games_analyzed': historical_games[:5]  # Show 5 most recent
        }

    def get_simulated_h2h_games(self, home_team_id: int, away_team_id: int, limit: int) -> List[Dict]:
        """Simulate historical games between two teams"""
        historical_games = []

        # Generate realistic historical matchups
        for i in range(min(limit, 8)):  # Max 8 historical games
            # Slightly favor home team (realistic)
            home_score = random.choices([0, 1, 2, 3, 4], weights=[8, 25, 35, 20, 12])[0]
            away_score = random.choices([0, 1, 2, 3, 4], weights=[12, 30, 30, 18, 10])[0]

            game_date = datetime.now() - timedelta(days=random.randint(30, 730))  # 1 month to 2 years ago

            historical_games.append({
                'home_team_id': home_team_id,
                'away_team_id': away_team_id,
                'home_score': home_score,
                'away_score': away_score,
                'date': game_date,
                'days_ago': (datetime.now() - game_date).days
            })

        # Sort by date (most recent first)
        historical_games.sort(key=lambda x: x['date'], reverse=True)

        return historical_games

    def analyze_recent_trend(self, recent_games: List[Dict]) -> str:
        """Analyze trend in recent head-to-head games"""
        if len(recent_games) < 2:
            return "Insufficient data"

        home_team_results = []
        for game in recent_games:
            if game['home_score'] > game['away_score']:
                home_team_results.append('W')
            elif game['home_score'] < game['away_score']:
                home_team_results.append('L')
            else:
                home_team_results.append('D')

        # Analyze pattern
        wins = home_team_results.count('W')
        total = len(home_team_results)

        if wins == total:
            return "Home team dominates"
        elif wins == 0:
            return "Away team dominates"
        elif wins > total / 2:
            return "Home team favored"
        elif wins < total / 2:
            return "Away team favored"
        else:
            return "Evenly matched"

    def get_h2h_prediction_factor(self, home_team_id: int, away_team_id: int) -> Dict:
        """Get head-to-head factor for prediction algorithm"""
        h2h_record = self.get_head_to_head_record(home_team_id, away_team_id)

        if h2h_record['total_games'] == 0:
            return {
                'h2h_factor': 0.0,  # Neutral
                'confidence': 0,
                'reasoning': "No historical data available"
            }

        # Convert win percentage to prediction factor
        win_percentage = h2h_record['home_win_percentage']

        # Map win percentage to factor (-1 to +1 scale)
        if win_percentage >= 70:
            h2h_factor = 0.8  # Strong home advantage
            confidence = 90
        elif win_percentage >= 60:
            h2h_factor = 0.4  # Moderate home advantage
            confidence = 75
        elif win_percentage >= 40:
            h2h_factor = 0.0  # Neutral
            confidence = 50
        elif win_percentage >= 30:
            h2h_factor = -0.4  # Moderate away advantage
            confidence = 75
        else:
            h2h_factor = -0.8  # Strong away advantage
            confidence = 90

        return {
            'h2h_factor': h2h_factor,
            'confidence': confidence,
            'reasoning': f"Home team wins {win_percentage}% of time ({h2h_record['total_games']} games)"
        }

    def analyze_matchup(self, home_team_id: int, away_team_id: int) -> Dict:
        """Complete head-to-head matchup analysis"""
        home_team = self.db.query(Team).filter(Team.id == home_team_id).first()
        away_team = self.db.query(Team).filter(Team.id == away_team_id).first()

        if not home_team or not away_team:
            return {"error": "Team not found"}

        h2h_record = self.get_head_to_head_record(home_team_id, away_team_id)
        prediction_factor = self.get_h2h_prediction_factor(home_team_id, away_team_id)

        return {
            'matchup': f"{home_team.name} vs {away_team.name}",
            'historical_record': h2h_record,
            'prediction_factor': prediction_factor
        }

    def close(self):
        self.db.close()

if __name__ == "__main__":
    analyzer = HeadToHeadAnalyzer()

    print("HEAD-TO-HEAD ANALYSIS")
    print("=" * 50)

    # Test with first few teams
    teams = analyzer.db.query(Team).limit(4).all()

    if len(teams) >= 2:
        # Analyze Arsenal vs Liverpool matchup
        home_team, away_team = teams[0], teams[1]

        print(f"\nMatchup: {home_team.name} vs {away_team.name}")
        print("-" * 30)

        analysis = analyzer.analyze_matchup(home_team.id, away_team.id)

        if 'error' not in analysis:
            record = analysis['historical_record']
            factor = analysis['prediction_factor']

            print(f"Historical Record ({record['total_games']} games):")
            print(f"  {home_team.name} wins: {record['home_wins']}")
            print(f"  Draws: {record['draws']}")
            print(f"  {away_team.name} wins: {record['away_wins']}")
            print(f"  Home win %: {record['home_win_percentage']}%")
            print(f"  Recent trend: {record['recent_trend']}")

            print(f"\nPrediction Factor: {factor['h2h_factor']} (confidence: {factor['confidence']}%)")
            print(f"Reasoning: {factor['reasoning']}")

            if record['games_analyzed']:
                print(f"\nRecent Games:")
                for i, game in enumerate(record['games_analyzed'][:3], 1):
                    print(f"  {i}. {game['home_score']}-{game['away_score']} ({game['days_ago']} days ago)")

    print(f"\n{'='*50}")
    print("Head-to-Head Analyzer ready!")

    analyzer.close()
