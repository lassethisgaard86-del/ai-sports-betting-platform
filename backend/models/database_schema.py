from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    league = Column(String(50), nullable=False)  # Premier League, La Liga, etc.
    country = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    home_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    away_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    game_date = Column(DateTime, nullable=False)
    league = Column(String(50), nullable=False)
    status = Column(String(20), default='scheduled')  # scheduled, live, finished
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])

class Odds(Base):
    __tablename__ = 'odds'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    bet_type = Column(String(50), nullable=False)  # home_win, away_win, draw, over_2.5, etc.
    odds_value = Column(Float, nullable=False)
    source = Column(String(50), nullable=False)  # bet365, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship
    game = relationship("Game")

class Prediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    prediction_type = Column(String(50), nullable=False)  # home_win, away_win, etc.
    confidence = Column(Float, nullable=False)  # 0-100%
    reasoning = Column(String(1000))  # AI's explanation
    created_at = Column(DateTime, default=datetime.utcnow)
    is_correct = Column(Boolean, default=None)  # Filled after game ends

    # Relationship
    game = relationship("Game")
