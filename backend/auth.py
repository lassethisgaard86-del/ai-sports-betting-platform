"""
Basic Authentication System
Simple user management for MVP
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import Session
from models.database_schema import Base
from database import SessionLocal
from datetime import datetime, timedelta
import hashlib
import secrets

# User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=None)

# Simple token storage (in production, use JWT or Redis)
active_tokens = {}

# Security scheme
security = HTTPBearer()

def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    try:
        salt, hash_part = password_hash.split(':')
        return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part
    except:
        return False

def create_user(email: str, password: str, db: Session) -> User:
    """Create new user account"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    password_hash = hash_password(password)
    new_user = User(
        email=email,
        password_hash=password_hash
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(email: str, password: str, db: Session) -> User:
    """Authenticate user login"""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    return user

def create_access_token(user_id: int) -> str:
    """Create access token for user"""
    token = secrets.token_urlsafe(32)
    active_tokens[token] = {
        'user_id': user_id,
        'created_at': datetime.utcnow(),
        'expires_at': datetime.utcnow() + timedelta(days=7)
    }
    return token

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(lambda: SessionLocal())):
    """Get current authenticated user"""
    token = credentials.credentials

    # Check if token exists and is valid
    if token not in active_tokens:
        raise HTTPException(status_code=401, detail="Invalid token")

    token_data = active_tokens[token]

    # Check if token expired
    if datetime.utcnow() > token_data['expires_at']:
        del active_tokens[token]
        raise HTTPException(status_code=401, detail="Token expired")

    # Get user
    user = db.query(User).filter(User.id == token_data['user_id']).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    return user

# Optional: Authentication dependency for protected routes
def require_auth(user: User = Depends(get_current_user)):
    """Dependency to require authentication"""
    return user

if __name__ == "__main__":
    # Test authentication system
    from database import create_tables

    print("Testing authentication system...")
    create_tables()  # Create user table

    db = SessionLocal()

    # Test user creation
    try:
        test_user = create_user("test@example.com", "password123", db)
        print(f"✅ Created test user: {test_user.email}")

        # Test authentication
        auth_user = authenticate_user("test@example.com", "password123", db)
        if auth_user:
            token = create_access_token(auth_user.id)
            print(f"✅ Authentication successful, token: {token[:20]}...")
        else:
            print("❌ Authentication failed")

    except Exception as e:
        print(f"Note: {e}")

    db.close()
    print("Authentication system ready!")
