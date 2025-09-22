from database import SessionLocal
from models.database_schema import Team, Game, Odds, Prediction
from datetime import datetime

def get_all_teams():
    """Get all teams from database"""
    db = SessionLocal()
    teams = db.query(Team).all()
    db.close()
    return teams

def get_upcoming_games(limit=10):
    """Get upcoming games"""
    db = SessionLocal()
    games = db.query(Game).filter(
        Game.game_date > datetime.now(),
        Game.status == 'scheduled'
    ).limit(limit).all()
    db.close()
    return games

def get_game_odds(game_id):
    """Get all odds for a specific game"""
    db = SessionLocal()
    odds = db.query(Odds).filter(Odds.game_id == game_id).all()
    db.close()
    return odds

def add_prediction(game_id, prediction_type, confidence, reasoning):
    """Add a new AI prediction"""
    db = SessionLocal()
    prediction = Prediction(
        game_id=game_id,
        prediction_type=prediction_type,
        confidence=confidence,
        reasoning=reasoning
    )
    db.add(prediction)
    db.commit()
    db.close()
    return prediction

if __name__ == "__main__":
    # Test the functions
    print("Testing database utilities...")

    teams = get_all_teams()
    print(f"Found {len(teams)} teams")

    games = get_upcoming_games()
    print(f"Found {len(games)} upcoming games")

    if games:
        game_odds = get_game_odds(games[0].id)
        print(f"Found {len(game_odds)} odds for first game")

        # Test adding a prediction
        add_prediction(games[0].id, "home_win", 78.5, "Strong home record and recent form")
        print("Added sample prediction")

    print("Database utilities working correctly!")
