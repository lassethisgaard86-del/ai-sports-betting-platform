from database import SessionLocal, create_tables
from models.database_schema import Team, Game, Odds, Prediction
from datetime import datetime, timedelta

def seed_teams():
    """Add popular football teams"""
    db = SessionLocal()

    teams = [
        # Premier League
        {"name": "Arsenal", "league": "Premier League", "country": "England"},
        {"name": "Liverpool", "league": "Premier League", "country": "England"},
        {"name": "Manchester City", "league": "Premier League", "country": "England"},
        {"name": "Chelsea", "league": "Premier League", "country": "England"},

        # La Liga
        {"name": "Real Madrid", "league": "La Liga", "country": "Spain"},
        {"name": "Barcelona", "league": "La Liga", "country": "Spain"},
        {"name": "Atletico Madrid", "league": "La Liga", "country": "Spain"},

        # Serie A
        {"name": "Juventus", "league": "Serie A", "country": "Italy"},
        {"name": "AC Milan", "league": "Serie A", "country": "Italy"},
        {"name": "Inter Milan", "league": "Serie A", "country": "Italy"},
    ]

    for team_data in teams:
        team = Team(**team_data)
        db.add(team)

    db.commit()
    print(f"Added {len(teams)} teams to database")
    db.close()

def seed_games():
    """Add upcoming sample games"""
    db = SessionLocal()

    # Get some teams
    arsenal = db.query(Team).filter(Team.name == "Arsenal").first()
    liverpool = db.query(Team).filter(Team.name == "Liverpool").first()
    real_madrid = db.query(Team).filter(Team.name == "Real Madrid").first()
    barcelona = db.query(Team).filter(Team.name == "Barcelona").first()

    if arsenal and liverpool and real_madrid and barcelona:
        games = [
            {
                "home_team_id": arsenal.id,
                "away_team_id": liverpool.id,
                "game_date": datetime.now() + timedelta(days=2),
                "league": "Premier League",
                "status": "scheduled"
            },
            {
                "home_team_id": real_madrid.id,
                "away_team_id": barcelona.id,
                "game_date": datetime.now() + timedelta(days=5),
                "league": "La Liga",
                "status": "scheduled"
            }
        ]

        for game_data in games:
            game = Game(**game_data)
            db.add(game)

        db.commit()
        print(f"Added {len(games)} games to database")

    db.close()

def seed_sample_odds():
    """Add sample betting odds"""
    db = SessionLocal()

    # Get first game
    game = db.query(Game).first()

    if game:
        odds_data = [
            {"game_id": game.id, "bet_type": "home_win", "odds_value": 2.1, "source": "bet365"},
            {"game_id": game.id, "bet_type": "away_win", "odds_value": 3.5, "source": "bet365"},
            {"game_id": game.id, "bet_type": "draw", "odds_value": 3.2, "source": "bet365"},
        ]

        for odd_data in odds_data:
            odds = Odds(**odd_data)
            db.add(odds)

        db.commit()
        print(f"Added sample odds for game")

    db.close()

if __name__ == "__main__":
    # Make sure tables exist
    create_tables()

    # Add seed data
    seed_teams()
    seed_games()
    seed_sample_odds()

    print("Database seeded successfully!")
