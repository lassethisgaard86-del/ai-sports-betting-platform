"""
Confidence Scoring System
Combines all prediction factors to generate confidence ratings
"""

import math
from datetime import datetime
from database import SessionLocal
from models.database_schema import Team, Game, Prediction
from team_performance_analyzer import TeamPerformanceAnalyzer
from recent_form_calculator import RecentFormCalculator
from head_to_head_analyzer import HeadToHeadAnalyzer
from home_advantage_calculator import HomeAdvantageCalculator
from typing import Dict, List

class ConfidenceScorer:
    """Generates confidence scores for match predictions"""

    def __init__(self):
        self.db = SessionLocal()

        # Initialize all analyzers
        self.performance_analyzer = TeamPerformanceAnalyzer()
        self.form_calculator = RecentFormCalculator()
        self.h2h_analyzer = HeadToHeadAnalyzer()
        self.home_advantage_calculator = HomeAdvantageCalculator()

        # Weighting factors (from our hybrid approach)
        self.weights = {
            'team_strength': 0.30,    # 30% - ELO ratings
            'recent_form': 0.25,      # 25% - Last 5 games
            'head_to_head': 0.15,     # 15% - Historical matchups
            'home_advantage': 0.15,   # 15% - Home field advantage
            'key_players': 0.10,      # 10% - Injuries/suspensions
            'situational': 0.05       # 5% - Weather, motivation, etc.
        }

    def calculate_match_prediction(self, home_team_id: int, away_team_id: int) -> Dict:
        """Generate complete prediction with confidence score"""

        # Get team information
        home_team = self.db.query(Team).filter(Team.id == home_team_id).first()
        away_team = self.db.query(Team).filter(Team.id == away_team_id).first()

        if not home_team or not away_team:
            return {"error": "Team not found"}

        # Collect all prediction factors
        factors = self.collect_prediction_factors(home_team_id, away_team_id)

        # Calculate weighted prediction score
        prediction_score = self.calculate_weighted_score(factors)

        # Generate confidence level
        confidence = self.calculate_confidence_level(factors, prediction_score)

        # Determine prediction outcome
        prediction_outcome = self.determine_prediction_outcome(prediction_score)

        # Generate explanation
        explanation = self.generate_explanation(factors, prediction_outcome)

        return {
            'matchup': f"{home_team.name} vs {away_team.name}",
            'prediction': prediction_outcome,
            'confidence': confidence,
            'prediction_score': round(prediction_score, 3),
            'explanation': explanation,
            'factors': factors,
            'timestamp': datetime.now()
        }

    def collect_prediction_factors(self, home_team_id: int, away_team_id: int) -> Dict:
        """Collect all prediction factors from different analyzers"""

        # Team strength (ELO ratings)
        elo_ratings = self.performance_analyzer.calculate_elo_ratings()
        home_elo = elo_ratings.get(home_team_id, 1500)
        away_elo = elo_ratings.get(away_team_id, 1500)
        elo_difference = (home_elo - away_elo) / 400  # Normalize

        # Recent form
        home_form = self.form_calculator.calculate_form_score(home_team_id)
        away_form = self.form_calculator.calculate_form_score(away_team_id)
        form_difference = (home_form['form_score'] - away_form['form_score']) / 3  # Normalize to -1 to +1

        # Head-to-head
        h2h_factor = self.h2h_analyzer.get_h2h_prediction_factor(home_team_id, away_team_id)
        h2h_score = h2h_factor['h2h_factor']

        # Home advantage
        home_adv = self.home_advantage_calculator.get_home_advantage_factor(home_team_id, away_team_id)
        home_advantage_score = home_adv['home_advantage_factor']

        # Key players (simulated for now)
        key_players_factor = self.simulate_key_players_factor()

        # Situational factors (simulated)
        situational_factor = self.simulate_situational_factor()

        return {
            'team_strength': {
                'home_elo': home_elo,
                'away_elo': away_elo,
                'difference': elo_difference,
                'factor_score': max(-1, min(1, elo_difference))  # Cap at ±1
            },
            'recent_form': {
                'home_form': home_form['form_score'],
                'away_form': away_form['form_score'],
                'difference': form_difference,
                'factor_score': max(-1, min(1, form_difference))
            },
            'head_to_head': {
                'h2h_factor': h2h_score,
                'factor_score': h2h_score,
                'confidence': h2h_factor['confidence']
            },
            'home_advantage': {
                'advantage_factor': home_advantage_score,
                'factor_score': home_advantage_score
            },
            'key_players': {
                'factor_score': key_players_factor,
                'description': 'Simulated player availability impact'
            },
            'situational': {
                'factor_score': situational_factor,
                'description': 'Weather, motivation, and other factors'
            }
        }

    def calculate_weighted_score(self, factors: Dict) -> float:
        """Calculate overall weighted prediction score"""

        weighted_score = (
            factors['team_strength']['factor_score'] * self.weights['team_strength'] +
            factors['recent_form']['factor_score'] * self.weights['recent_form'] +
            factors['head_to_head']['factor_score'] * self.weights['head_to_head'] +
            factors['home_advantage']['factor_score'] * self.weights['home_advantage'] +
            factors['key_players']['factor_score'] * self.weights['key_players'] +
            factors['situational']['factor_score'] * self.weights['situational']
        )

        return weighted_score

    def calculate_confidence_level(self, factors: Dict, prediction_score: float) -> int:
        """Calculate confidence percentage based on factor agreement"""

        # Base confidence from prediction strength
        base_confidence = min(90, abs(prediction_score) * 100 + 50)

        # Check factor agreement (how many factors point in same direction)
        factor_scores = [
            factors['team_strength']['factor_score'],
            factors['recent_form']['factor_score'],
            factors['head_to_head']['factor_score'],
            factors['home_advantage']['factor_score']
        ]

        prediction_direction = 1 if prediction_score > 0 else -1
        agreeing_factors = sum(1 for score in factor_scores if (score * prediction_direction) > 0)

        # Adjust confidence based on agreement
        agreement_boost = (agreeing_factors / len(factor_scores)) * 20

        # H2H confidence factor
        h2h_confidence_bonus = factors['head_to_head']['confidence'] / 100 * 10

        final_confidence = base_confidence + agreement_boost + h2h_confidence_bonus

        return min(95, max(55, int(final_confidence)))  # Cap between 55-95%

    def determine_prediction_outcome(self, prediction_score: float) -> Dict:
        """Determine prediction outcome from score"""

        if prediction_score > 0.15:
            return {'outcome': 'Home Win', 'strength': 'Strong' if prediction_score > 0.3 else 'Moderate'}
        elif prediction_score < -0.15:
            return {'outcome': 'Away Win', 'strength': 'Strong' if prediction_score < -0.3 else 'Moderate'}
        else:
            return {'outcome': 'Draw/Close', 'strength': 'Uncertain'}

    def generate_explanation(self, factors: Dict, prediction: Dict) -> str:
        """Generate human-readable explanation"""

        explanations = []

        # Analyze strongest factors
        factor_impacts = [
            ('Team strength', factors['team_strength']['factor_score'], self.weights['team_strength']),
            ('Recent form', factors['recent_form']['factor_score'], self.weights['recent_form']),
            ('Head-to-head', factors['head_to_head']['factor_score'], self.weights['head_to_head']),
            ('Home advantage', factors['home_advantage']['factor_score'], self.weights['home_advantage'])
        ]

        # Sort by weighted impact
        factor_impacts.sort(key=lambda x: abs(x[1] * x[2]), reverse=True)

        # Explain top 2-3 factors
        for name, score, weight in factor_impacts[:3]:
            impact = abs(score * weight)
            if impact > 0.05:  # Only mention significant factors
                direction = "favors home team" if score > 0 else "favors away team"
                strength = "strongly" if impact > 0.1 else "slightly"
                explanations.append(f"{name} {strength} {direction}")

        if not explanations:
            explanations.append("Factors are evenly balanced")

        return f"Prediction: {prediction['outcome']}. " + "; ".join(explanations[:2]) + "."

    def simulate_key_players_factor(self) -> float:
        """Simulate key players availability impact"""
        import random
        # Simulate between -0.2 to +0.2 impact
        return random.uniform(-0.2, 0.2)

    def simulate_situational_factor(self) -> float:
        """Simulate situational factors"""
        import random
        # Small random factor for weather, motivation, etc.
        return random.uniform(-0.1, 0.1)

    def save_prediction_to_database(self, prediction_data: Dict, game_id: int = None):
        """Save prediction to database"""
        try:
            new_prediction = Prediction(
                game_id=game_id,
                prediction_type=prediction_data['prediction']['outcome'],
                confidence=prediction_data['confidence'],
                reasoning=prediction_data['explanation']
            )
            self.db.add(new_prediction)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error saving prediction: {e}")
            return False

    def close(self):
        """Close all connections"""
        self.performance_analyzer.close()
        self.form_calculator.close()
        self.h2h_analyzer.close()
        self.home_advantage_calculator.close()
        self.db.close()

if __name__ == "__main__":
    scorer = ConfidenceScorer()

    print("CONFIDENCE SCORING SYSTEM")
    print("=" * 60)

    # Test with Arsenal vs Liverpool
    teams = scorer.db.query(Team).limit(2).all()

    if len(teams) >= 2:
        home_team, away_team = teams[0], teams[1]

        print(f"\nGenerating prediction: {home_team.name} vs {away_team.name}")
        print("=" * 40)

        prediction = scorer.calculate_match_prediction(home_team.id, away_team.id)

        if 'error' not in prediction:
            print(f"Prediction: {prediction['prediction']['outcome']} ({prediction['prediction']['strength']})")
            print(f"Confidence: {prediction['confidence']}%")
            print(f"Prediction Score: {prediction['prediction_score']}")
            print(f"\nExplanation: {prediction['explanation']}")

            print(f"\nDetailed Factor Analysis:")
            print(f"• Team Strength: {prediction['factors']['team_strength']['factor_score']:+.3f}")
            print(f"• Recent Form: {prediction['factors']['recent_form']['factor_score']:+.3f}")
            print(f"• Head-to-Head: {prediction['factors']['head_to_head']['factor_score']:+.3f}")
            print(f"• Home Advantage: {prediction['factors']['home_advantage']['factor_score']:+.3f}")

    print(f"\n{'='*60}")
    print("✅ Confidence Scoring System ready!")
    print("🎯 AI can now generate predictions with confidence levels!")

    scorer.close()
