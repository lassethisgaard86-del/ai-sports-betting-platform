"""
Sports Data Collector - Mock data for development
This simulates real API responses for testing our system
"""

import random
from datetime import datetime, timedelta
from database import SessionLocal
from models.database_schema import Team, Game, Odds

class SportsDataCollector:
    def __init__(self):
        self.db = SessionLocal()

    def get_mock_game_data(self, days_ahead=7):
        """Generate mock upcoming games"""
        teams = self.db.query(Team).all()
        if len(teams) < 4:
            print("Need at least 4 teams in database")
            return []

        mock_games = []

        # Generate 5 mock games over the next week
        for i in range(5):
            # Pick random teams
            home_team = random.choice(teams)
            away_team = random.choice([t for t in teams if t.id != home_team.id])

            game_data = {
                'home_team': home_team.name,
                'away_team': away_team.name,
                'home_team_id': home_team.id,
                'away_team_id': away_team.id,
                'league': home_team.league,
                'date': datetime.now() + timedelta(days=random.randint(1, days_ahead)),
                'status': 'scheduled'
            }
            mock_games.append(game_data)

        return mock_games

    def get_mock_odds_data(self, game_id):
        """Generate realistic mock betting odds"""
        # Generate realistic odds (lower = more likely)
        home_win_odds = round(random.uniform(1.5, 4.0), 1)
        draw_odds = round(random.uniform(2.8, 3.8), 1)
        away_win_odds = round(random.uniform(1.8, 5.0), 1)

        mock_odds = [
            {'bet_type': 'home_win', 'odds': home_win_odds, 'source': 'bet365'},
            {'bet_type': 'draw', 'odds': draw_odds, 'source': 'bet365'},
            {'bet_type': 'away_win', 'odds': away_win_odds, 'source': 'bet365'},
            {'bet_type': 'over_2.5', 'odds': round(random.uniform(1.4, 2.2), 1), 'source': 'bet365'},
            {'bet_type': 'under_2.5', 'odds': round(random.uniform(1.6, 3.0), 1), 'source': 'bet365'},
        ]

        return mock_odds

    def update_games_database(self):
        """Add new mock games to database"""
        mock_games = self.get_mock_game_data()
        added_games = []

        for game_data in mock_games:
            # Simple check - just add games (duplicates OK for testing)
            new_game = Game(
                home_team_id=game_data['home_team_id'],
                away_team_id=game_data['away_team_id'],
                game_date=game_data['date'],
                league=game_data['league'],
                status=game_data['status']
            )
            self.db.add(new_game)
            added_games.append(game_data)

        self.db.commit()
        return added_games

    def update_odds_database(self):
        """Add mock odds for games without odds"""
        games = self.db.query(Game).filter(Game.status == 'scheduled').all()
        updated_games = 0

        for game in games:
            # Check if game already has odds
            existing_odds = self.db.query(Odds).filter(Odds.game_id == game.id).first()

            if not existing_odds:
                mock_odds = self.get_mock_odds_data(game.id)

                for odd_data in mock_odds:
                    new_odds = Odds(
                        game_id=game.id,
                        bet_type=odd_data['bet_type'],
                        odds_value=odd_data['odds'],
                        source=odd_data['source']
                    )
                    self.db.add(new_odds)

                updated_games += 1

        self.db.commit()
        return updated_games

    def run_data_collection(self):
        """Simulate full data collection process"""
        print("Starting sports data collection...")

        # Update games
        new_games = self.update_games_database()
        print(f"Added {len(new_games)} new games")

        # Update odds
        odds_updates = self.update_odds_database()
        print(f"Added odds for {odds_updates} games")

        print("Data collection complete!")

        return len(new_games), odds_updates

    def close(self):
        self.db.close()

if __name__ == "__main__":
    collector = SportsDataCollector()
    collector.run_data_collection()
    collector.close()
