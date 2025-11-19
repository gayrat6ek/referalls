"""
Database operations module
"""
import sqlite3
import logging
from typing import Optional, List, Tuple
from config import config

logger = logging.getLogger(__name__)


class Database:
    """Database manager class"""
    
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                referrer_id INTEGER,
                points INTEGER DEFAULT 0,
                is_subscribed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referrer_id) REFERENCES users(user_id)
            )
        """)
        
        # Referrals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER NOT NULL,
                referred_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referrer_id) REFERENCES users(user_id),
                FOREIGN KEY (referred_id) REFERENCES users(user_id)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def add_user(self, user_id: int, username: Optional[str] = None, 
                 first_name: Optional[str] = None, last_name: Optional[str] = None,
                 referrer_id: Optional[int] = None) -> bool:
        """Add new user to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, referrer_id)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, first_name, last_name, referrer_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[dict]:
        """Get user by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def update_user_subscription(self, user_id: int, is_subscribed: bool) -> bool:
        """Update user subscription status"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users SET is_subscribed = ? WHERE user_id = ?
            """, (1 if is_subscribed else 0, user_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating subscription: {e}")
            return False
    
    def update_phone_number(self, user_id: int, phone_number: str) -> bool:
        """Update user phone number"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users SET phone_number = ? WHERE user_id = ?
            """, (phone_number, user_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating phone number: {e}")
            return False
    
    def add_referral(self, referrer_id: int, referred_id: int) -> bool:
        """Add referral and update points"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if referral already exists
            cursor.execute("""
                SELECT id FROM referrals WHERE referrer_id = ? AND referred_id = ?
            """, (referrer_id, referred_id))
            
            if cursor.fetchone():
                conn.close()
                return False
            
            # Add referral
            cursor.execute("""
                INSERT INTO referrals (referrer_id, referred_id)
                VALUES (?, ?)
            """, (referrer_id, referred_id))
            
            # Update referrer points
            cursor.execute("""
                UPDATE users SET points = points + ? WHERE user_id = ?
            """, (config.POINTS_PER_REFERRAL, referrer_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding referral: {e}")
            return False
    
    def get_user_referrals(self, user_id: int) -> List[dict]:
        """Get all referrals for a user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT u.user_id, u.username, u.first_name, r.created_at
                FROM referrals r
                JOIN users u ON r.referred_id = u.user_id
                WHERE r.referrer_id = ?
                ORDER BY r.created_at DESC
            """, (user_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting referrals: {e}")
            return []
    
    def get_user_points(self, user_id: int) -> int:
        """Get user points"""
        user = self.get_user(user_id)
        return user['points'] if user else 0
    
    def get_referral_count(self, user_id: int) -> int:
        """Get count of user's referrals"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) as count FROM referrals WHERE referrer_id = ?
            """, (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Error getting referral count: {e}")
            return 0
    
    def get_total_users(self) -> int:
        """Get total number of users"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM users")
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Error getting total users: {e}")
            return 0
    
    def get_total_referrals(self) -> int:
        """Get total number of referrals"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM referrals")
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Error getting total referrals: {e}")
            return 0
    
    def get_subscribed_users_count(self) -> int:
        """Get count of subscribed users"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_subscribed = 1")
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Error getting subscribed users count: {e}")
            return 0
    
    def get_users_with_phone_count(self) -> int:
        """Get count of users who shared phone number"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE phone_number IS NOT NULL")
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Error getting users with phone count: {e}")
            return 0
    
    def get_top_referrers(self, limit: int = 10) -> List[dict]:
        """Get top referrers by referral count"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    u.user_id,
                    u.username,
                    u.first_name,
                    u.last_name,
                    u.phone_number,
                    u.points,
                    COUNT(r.id) as referral_count
                FROM users u
                LEFT JOIN referrals r ON u.user_id = r.referrer_id
                GROUP BY u.user_id
                HAVING referral_count > 0
                ORDER BY referral_count DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting top referrers: {e}")
            return []


# Create database instance
db = Database()

