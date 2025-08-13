"""
Authentication System
Handles user authentication, JWT tokens, and password management
"""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .config import settings
from .database import db_manager
from .models.database import User, UserSession

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

class AuthManager:
    """Manages user authentication and authorization"""
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            logger.warning(f"JWT token verification failed: {e}")
            return None
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password"""
        try:
            session = await db_manager.get_session_async()
            
            # Find user by username
            user = session.query(User).filter(User.username == username).first()
            
            if not user:
                return None
            
            if not self.verify_password(password, user.hashed_password):
                return None
            
            # Update last activity
            user.updated_at = datetime.utcnow()
            session.commit()
            
            return user
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None
        finally:
            await db_manager.close_session(session)
    
    async def create_user_session(self, user_id: str, session_token: str) -> bool:
        """Create a new user session"""
        try:
            session = await db_manager.get_session_async()
            
            # Set expiration time
            expires_at = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            
            # Create session record
            user_session = UserSession(
                user_id=user_id,
                session_token=session_token,
                expires_at=expires_at
            )
            
            session.add(user_session)
            session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create user session: {e}")
            return False
        finally:
            await db_manager.close_session(session)
    
    async def validate_session(self, session_token: str) -> Optional[User]:
        """Validate a user session and return the associated user"""
        try:
            session = await db_manager.get_session_async()
            
            # Find active session
            user_session = session.query(UserSession).filter(
                UserSession.session_token == session_token,
                UserSession.expires_at > datetime.utcnow()
            ).first()
            
            if not user_session:
                return None
            
            # Update last activity
            user_session.last_activity = datetime.utcnow()
            session.commit()
            
            # Get associated user
            user = session.query(User).filter(User.id == user_session.user_id).first()
            return user
            
        except Exception as e:
            logger.error(f"Session validation error: {e}")
            return None
        finally:
            await db_manager.close_session(session)
    
    async def revoke_session(self, session_token: str) -> bool:
        """Revoke a user session"""
        try:
            session = await db_manager.get_session_async()
            
            # Find and delete session
            user_session = session.query(UserSession).filter(
                UserSession.session_token == session_token
            ).first()
            
            if user_session:
                session.delete(user_session)
                session.commit()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to revoke session: {e}")
            return False
        finally:
            await db_manager.close_session(session)
    
    async def revoke_all_user_sessions(self, user_id: str) -> bool:
        """Revoke all sessions for a specific user"""
        try:
            session = await db_manager.get_session_async()
            
            # Delete all sessions for user
            deleted_count = session.query(UserSession).filter(
                UserSession.user_id == user_id
            ).delete()
            
            session.commit()
            logger.info(f"Revoked {deleted_count} sessions for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to revoke user sessions: {e}")
            return False
        finally:
            await db_manager.close_session(session)
    
    async def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions"""
        try:
            session = await db_manager.get_session_async()
            
            # Delete expired sessions
            deleted_count = session.query(UserSession).filter(
                UserSession.expires_at < datetime.utcnow()
            ).delete()
            
            session.commit()
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} expired sessions")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired sessions: {e}")
            return 0
        finally:
            await db_manager.close_session(session)
    
    def generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)

# Global auth manager instance
auth_manager = AuthManager()

# Dependency functions for FastAPI
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get the current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify JWT token
        payload = auth_manager.verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    try:
        session = await db_manager.get_session_async()
        user = session.query(User).filter(User.username == username).first()
        
        if user is None:
            raise credentials_exception
        
        return user
        
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise credentials_exception
    finally:
        await db_manager.close_session(session)

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """Get the current superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Utility functions
def create_user_credentials(username: str, email: str, password: str, full_name: Optional[str] = None) -> Dict[str, str]:
    """Create user credentials with hashed password"""
    hashed_password = auth_manager.get_password_hash(password)
    
    return {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "full_name": full_name or username
    }

async def create_user_account(user_data: Dict[str, str]) -> Optional[User]:
    """Create a new user account"""
    try:
        session = await db_manager.get_session_async()
        
        # Check if username or email already exists
        existing_user = session.query(User).filter(
            (User.username == user_data["username"]) | (User.email == user_data["email"])
        ).first()
        
        if existing_user:
            logger.warning(f"User already exists: {user_data['username']}")
            return None
        
        # Create new user
        user = User(**user_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        
        logger.info(f"Created new user account: {user_data['username']}")
        return user
        
    except Exception as e:
        logger.error(f"Failed to create user account: {e}")
        return None
    finally:
        await db_manager.close_session(session)

async def change_user_password(user_id: str, old_password: str, new_password: str) -> bool:
    """Change a user's password"""
    try:
        session = await db_manager.get_session_async()
        
        # Get user
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # Verify old password
        if not auth_manager.verify_password(old_password, user.hashed_password):
            return False
        
        # Hash new password
        user.hashed_password = auth_manager.get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        
        session.commit()
        
        # Revoke all existing sessions for security
        await auth_manager.revoke_all_user_sessions(user_id)
        
        logger.info(f"Password changed for user: {user.username}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to change password: {e}")
        return False
    finally:
        await db_manager.close_session(session)
