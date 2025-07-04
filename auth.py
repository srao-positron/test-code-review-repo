import hashlib
import secrets
import json
from typing import Dict, Optional
from datetime import datetime, timedelta

class AuthenticationService:
    """Handles user authentication with security best practices"""
    
    def __init__(self):
        self.users_db = {}  # In production, use proper database
        self.sessions = {}
        self.token_expiry = timedelta(hours=24)
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """Hash password using SHA-256 with salt"""
        if not salt:
            salt = secrets.token_hex(16)
        
        # TODO: Use bcrypt or scrypt instead of SHA-256
        password_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
        return password_hash, salt
    
    def register_user(self, username: str, password: str, email: str) -> Dict:
        """Register a new user"""
        # Basic validation
        if not username or not password or not email:
            raise ValueError("All fields are required")
        
        if username in self.users_db:
            raise ValueError("Username already exists")
        
        # Hash the password
        password_hash, salt = self.hash_password(password)
        
        # Store user data
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'salt': salt,
            'created_at': datetime.now().isoformat(),
            'is_active': True
        }
        
        # Save to database (using JSON for demo)
        self.users_db[username] = user_data
        self._persist_users()
        
        return {'username': username, 'email': email}
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return session token"""
        user = self.users_db.get(username)
        if not user:
            return None
        
        # Verify password
        password_hash, _ = self.hash_password(password, user['salt'])
        if password_hash != user['password_hash']:
            return None
        
        # Generate session token
        token = secrets.token_urlsafe(32)
        self.sessions[token] = {
            'username': username,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + self.token_expiry
        }
        
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify session token and return user info"""
        session = self.sessions.get(token)
        if not session:
            return None
        
        # Check expiration
        if datetime.now() > session['expires_at']:
            del self.sessions[token]
            return None
        
        return {'username': session['username']}
    
    def _persist_users(self):
        """Save users to file (demo only)"""
        with open('users.json', 'w') as f:
            json.dump(self.users_db, f)
    
    def load_users(self):
        """Load users from file (demo only)"""
        try:
            with open('users.json', 'r') as f:
                self.users_db = json.load(f)
        except FileNotFoundError:
            self.users_db = {}

# Example usage
if __name__ == "__main__":
    auth = AuthenticationService()
    
    # Register a user
    try:
        user = auth.register_user("john_doe", "password123", "john@example.com")
        print(f"User registered: {user}")
    except ValueError as e:
        print(f"Registration failed: {e}")
    
    # Authenticate
    token = auth.authenticate("john_doe", "password123")
    if token:
        print(f"Authentication successful. Token: {token[:10]}...")
    else:
        print("Authentication failed")
