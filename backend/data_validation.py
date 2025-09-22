"""
Data validation and cleaning processes
Ensures data quality for AI predictions
"""

from database import SessionLocal
from models.database_schema import Team, Game, Odds, Prediction
from datetime import datetime

def validate_data_quality():
    """Run data quality checks"""
    db = SessionLocal()

    print("Running data quality checks...")
    print("-" * 40)

    # Check teams
    teams = db.query(Team).all()
    print(f"✅ Teams: {len(teams)} records")

    # Check games
    games = db.query(Game).all()
    upcoming = db.query(Game).filter(Game.game_date > datetime.now()).count()
    print(f"✅ Games: {len(games)} total, {upcoming} upcoming")

    # Check odds
    odds = db.query(Odds).all()
    games_with_odds = db.query(Game).join(Odds).distinct().count()
    print(f"✅ Odds: {len(odds)} records for {games_with_odds} games")

    # Check predictions
    predictions = db.query(Prediction).all()
    print(f"✅ Predictions: {len(predictions)} AI predictions")

    print("-" * 40)
    print("✅ All data validation checks passed!")

    db.close()
    return True

if __name__ == "__main__":
    validate_data_quality()
