"""
Database Connection Manager
Handles database initialization, session management, and connection pooling
"""

import logging
from typing import Generator, Optional
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager

from .config import settings
from .models.database import Base

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and sessions"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize database connection and create tables"""
        try:
            # Create database engine
            self.engine = create_engine(
                settings.DATABASE_URL,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,  # Recycle connections every hour
                echo=settings.DEBUG  # Log SQL queries in debug mode
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Create all tables
            await self._create_tables()
            
            # Setup connection event handlers
            self._setup_event_handlers()
            
            self.is_initialized = True
            logger.info("Database manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database manager: {e}")
            raise
    
    async def _create_tables(self):
        """Create all database tables"""
        try:
            # Import all models to ensure they're registered
            from .models.database import (
                User, UserSession, DigitalTwin, Avatar, PersonalityProfile,
                HealthProfile, BehaviorLog, ConversationLog, SystemEvent, SyntheticDataset
            )
            
            # Create tables
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def _setup_event_handlers(self):
        """Setup database event handlers"""
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """Set SQLite pragmas for better performance"""
            if "sqlite" in settings.DATABASE_URL:
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=10000")
                cursor.execute("PRAGMA temp_store=MEMORY")
                cursor.close()
        
        @event.listens_for(self.engine, "checkout")
        def receive_checkout(dbapi_connection, connection_record, connection_proxy):
            """Handle connection checkout"""
            logger.debug("Database connection checked out")
        
        @event.listens_for(self.engine, "checkin")
        def receive_checkin(dbapi_connection, connection_record):
            """Handle connection checkin"""
            logger.debug("Database connection checked in")
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session with automatic cleanup"""
        if not self.is_initialized:
            raise RuntimeError("Database manager not initialized")
        
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    async def get_session_async(self) -> Session:
        """Get a database session for async operations"""
        if not self.is_initialized:
            raise RuntimeError("Database manager not initialized")
        
        return self.SessionLocal()
    
    async def close_session(self, session: Session):
        """Close a database session"""
        try:
            session.close()
        except Exception as e:
            logger.warning(f"Error closing database session: {e}")
    
    async def health_check(self) -> bool:
        """Check database health"""
        try:
            with self.get_session() as session:
                # Simple query to test connection
                session.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def get_database_info(self) -> dict:
        """Get database information and statistics"""
        try:
            with self.get_session() as session:
                # Get table counts
                table_counts = {}
                for table_name in Base.metadata.tables.keys():
                    try:
                        result = session.execute(f"SELECT COUNT(*) FROM {table_name}")
                        count = result.scalar()
                        table_counts[table_name] = count
                    except Exception as e:
                        logger.warning(f"Could not get count for table {table_name}: {e}")
                        table_counts[table_name] = "error"
                
                # Get database size (if supported)
                db_size = "unknown"
                try:
                    if "sqlite" in settings.DATABASE_URL:
                        result = session.execute("PRAGMA page_count * PRAGMA page_size")
                        db_size = f"{result.scalar()} bytes"
                    elif "postgresql" in settings.DATABASE_URL:
                        result = session.execute("""
                            SELECT pg_size_pretty(pg_database_size(current_database()))
                        """)
                        db_size = result.scalar()
                except Exception as e:
                    logger.debug(f"Could not get database size: {e}")
                
                return {
                    "status": "healthy" if await self.health_check() else "unhealthy",
                    "database_url": settings.DATABASE_URL,
                    "pool_size": self.engine.pool.size(),
                    "checked_in_connections": self.engine.pool.checkedin(),
                    "checked_out_connections": self.engine.pool.checkedout(),
                    "overflow_connections": self.engine.pool.overflow(),
                    "table_counts": table_counts,
                    "database_size": db_size
                }
                
        except Exception as e:
            logger.error(f"Failed to get database info: {e}")
            return {"status": "error", "error": str(e)}
    
    async def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old data to prevent database bloat"""
        try:
            with self.get_session() as session:
                from datetime import datetime, timedelta
                cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
                
                # Clean up old behavior logs
                deleted_logs = session.execute(
                    "DELETE FROM behavior_logs WHERE timestamp < :cutoff",
                    {"cutoff": cutoff_date}
                ).rowcount
                
                # Clean up old conversation logs
                deleted_conversations = session.execute(
                    "DELETE FROM conversation_logs WHERE timestamp < :cutoff",
                    {"cutoff": cutoff_date}
                ).rowcount
                
                # Clean up old system events
                deleted_events = session.execute(
                    "DELETE FROM system_events WHERE timestamp < :cutoff",
                    {"cutoff": cutoff_date}
                ).rowcount
                
                # Clean up expired user sessions
                deleted_sessions = session.execute(
                    "DELETE FROM user_sessions WHERE expires_at < :now",
                    {"now": datetime.utcnow()}
                ).rowcount
                
                logger.info(f"Cleaned up old data: {deleted_logs} logs, {deleted_conversations} conversations, "
                          f"{deleted_events} events, {deleted_sessions} sessions")
                
                return {
                    "deleted_logs": deleted_logs,
                    "deleted_conversations": deleted_conversations,
                    "deleted_events": deleted_events,
                    "deleted_sessions": deleted_sessions
                }
                
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")
            raise
    
    async def backup_database(self, backup_path: str) -> bool:
        """Create a database backup"""
        try:
            if "sqlite" in settings.DATABASE_URL:
                # SQLite backup
                import shutil
                shutil.copy2(settings.DATABASE_URL.replace("sqlite:///", ""), backup_path)
                logger.info(f"SQLite database backed up to: {backup_path}")
                return True
            elif "postgresql" in settings.DATABASE_URL:
                # PostgreSQL backup using pg_dump
                import subprocess
                import os
                
                # Extract connection details from URL
                url_parts = settings.DATABASE_URL.replace("postgresql://", "").split("@")
                if len(url_parts) == 2:
                    credentials, host_db = url_parts
                    username, password = credentials.split(":")
                    host, database = host_db.split("/")
                    
                    # Set environment variables for pg_dump
                    env = os.environ.copy()
                    env["PGPASSWORD"] = password
                    
                    # Run pg_dump
                    cmd = [
                        "pg_dump",
                        "-h", host,
                        "-U", username,
                        "-d", database,
                        "-f", backup_path,
                        "--format=custom"
                    ]
                    
                    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                    if result.returncode == 0:
                        logger.info(f"PostgreSQL database backed up to: {backup_path}")
                        return True
                    else:
                        logger.error(f"PostgreSQL backup failed: {result.stderr}")
                        return False
                else:
                    logger.error("Invalid PostgreSQL connection string format")
                    return False
            else:
                logger.warning(f"Backup not supported for database type: {settings.DATABASE_URL}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to backup database: {e}")
            return False
    
    async def shutdown(self):
        """Shutdown database manager"""
        logger.info("Shutting down database manager...")
        
        if self.engine:
            self.engine.dispose()
        
        self.is_initialized = False
        logger.info("Database manager shutdown complete")

# Global database manager instance
db_manager = DatabaseManager()
