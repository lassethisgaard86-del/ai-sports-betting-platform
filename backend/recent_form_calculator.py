"""
Recent Form Calculation System
Analyzes team momentum using weighted recent results
"""

import math
from datetime import datetime, timedelta
from database import SessionLocal
from models.database_schema import Team, Game
from typing import Dict, List

class RecentFormCalculator:
    """Calculates team form using exponential decay weighting"""

    def __init__(self, games_to_analyze: int = 5, decay_rate: float = 0.15):
        self.db = SessionLocal()
        self.games_to_analyze = games_to_analyze
        self.decay_rate = decay_rate  # How quickly older games lose importance

    def calculate_form_score(self, team_id: int) -> Dict:
        """Calculate weighted form score for a team"""
        # Get recent results (simulated for now)
        recent_results = self.get_recent_results(team_id)

        if not recent_results:
            return {
                'form_score': 1.5,  # Neutral form
                'form_rating': 'Unknown',
                'recent_results': [],
                'games_analyzed': 0
            }

        total_weighted_points = 0
        total_weight = 0

        # Calculate weighted score
        for i, result in enumerate(recent_results):
            # Exponential decay: recent games weighted more heavily
            weight = math.exp(-self.decay_rate * i)

            # Convert result to points (Win=3, Draw=1, Loss=0)
            if result['result'] == 'W':
                points = 3
            elif result['result'] == 'D':
                points = 1
            else:  # Loss
                points = 0

            total_weighted_points += points * weight
            total_weight += weight

        # Normalize to 0-3 scale
        form_score = total_weighted_points / total_weight if total_weight > 0 else 1.5

        return {
            'form_score': round(form_score, 2),
            'form_rating': self.classify_form(form_score),
            'recent_results': recent_results,
            'games_analyzed': len(recent_results)
        }

    def get_recent_results(self, team_id: int) -> List[Dict]:
        """Get recent match results for a team"""
        # Simulate recent results for testing
        import random

        # Generate realistic recent form
        possible_results = ['W', 'D', 'L']
        weights = [45, 25, 30]  # Slightly favor wins for testing

        recent_results = []
        for i in range(self.games_to_analyze):
            result = random.choices(possible_results, weights=weights)[0]

            # Simulate opponent and score
            opponent = f"Team {random.randint(1, 20)}"
            if result == 'W':
                goals_for = random.randint(1, 4)
                goals_against = random.randint(0, goals_for-1)
            elif result == 'D':
                goals = random.randint(0, 3)
                goals_for = goals_against = goals
            else:  # Loss
                goals_against = random.randint(1, 4)
                goals_for = random.randint(0, goals_against-1)

            recent_results.append({
                'result': result,
                'opponent': opponent,
                'goals_for': goals_for,
                'goals_against': goals_against,
                'days_ago': i * 7 + random.randint(1, 6)  # Roughly weekly games
            })

        return recent_results

    def classify_form(self, form_score: float) -> str:
        """Classify form into categories"""
        if form_score >= 2.5:
            return "Excellent"
        elif form_score >= 2.0:
            return "Good"
        elif form_score >= 1.5:
            return "Average"
        elif form_score >= 1.0:
            return "Poor"
        else:
            return "Terrible"

    def get_form_trend(self, team_id: int) -> Dict:
        """Analyze if team form is improving or declining"""
        recent_results = self.get_recent_results(team_id)

        if len(recent_results) < 3:
            return {'trend': 'Insufficient data', 'confidence': 0}

        # Compare first half vs second half of recent games
        mid_point = len(recent_results) // 2
        recent_half = recent_results[:mid_point]  # Most recent games
        older_half = recent_results[mid_point:]   # Older games

        def results_to_avg_points(results):
            total = sum(3 if r['result'] == 'W' else 1 if r['result'] == 'D' else 0 for r in results)
            return total / len(results) if results else 0

        recent_avg = results_to_avg_points(recent_half)
        older_avg = results_to_avg_points(older_half)

        difference = recent_avg - older_avg

        if difference > 0.5:
            trend = "Improving"
            confidence = min(abs(difference) * 50, 100)
        elif difference < -0.5:
            trend = "Declining"
            confidence = min(abs(difference) * 50, 100)
        else:
            trend = "Stable"
            confidence = 100 - abs(difference) * 50

        return {
            'trend': trend,
            'confidence': round(confidence, 1),
            'recent_avg': round(recent_avg, 2),
            'older_avg': round(older_avg, 2)
        }

    def analyze_all_teams_form(self) -> Dict:
        """Get form analysis for all teams"""
        teams = self.db.query(Team).all()
        team_forms = {}

        for team in teams:
            form_data = self.calculate_form_score(team.id)
            trend_data = self.get_form_trend(team.id)

            team_forms[team.name] = {
                'form_score': form_data['form_score'],
                'form_rating': form_data['form_rating'],
                'trend': trend_data['trend'],
                'games_analyzed': form_data['games_analyzed']
            }

        return team_forms

    def close(self):
        self.db.close()

if __name__ == "__main__":
    calculator = RecentFormCalculator()

    print("RECENT FORM ANALYSIS")
    print("=" * 50)

    # Analyze first few teams in detail
    teams = calculator.db.query(Team).limit(3).all()

    for team in teams:
        print(f"\n{team.name} - Recent Form Analysis")
        print("-" * 30)

        form_data = calculator.calculate_form_score(team.id)
        trend_data = calculator.get_form_trend(team.id)

        print(f"Form Score: {form_data['form_score']}/3.0 ({form_data['form_rating']})")
        print(f"Trend: {trend_data['trend']} (confidence: {trend_data['confidence']}%)")
        print(f"Games Analyzed: {form_data['games_analyzed']}")

        print("\nRecent Results:")
        for i, result in enumerate(form_data['recent_results'][:3], 1):
            print(f"  {i}. {result['result']} vs {result['opponent']} ({result['goals_for']}-{result['goals_against']}) - {result['days_ago']} days ago")

    print(f"\n{'='*50}")
    print("Recent Form Calculator ready!")

    calculator.close()
