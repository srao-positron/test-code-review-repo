"""
User management module with various issues for code review.
This adds new functionality to the existing API.
"""

import pickle
import yaml
from datetime import datetime
from typing import List, Dict, Any

# SECURITY ISSUE: Using pickle for serialization
class UserStore:
    def __init__(self, filename='users.pkl'):
        self.filename = filename
        self.users = self.load_users()
    
    def load_users(self):
        try:
            with open(self.filename, 'rb') as f:
                # SECURITY: Pickle can execute arbitrary code
                return pickle.load(f)
        except FileNotFoundError:
            return {}
    
    def save_users(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.users, f)
    
    # DESIGN ISSUE: No input validation
    def create_user(self, username: str, password: str, email: str) -> Dict:
        # SECURITY: Storing passwords in plain text
        user = {
            'id': len(self.users) + 1,
            'username': username,
            'password': password,  # Should be hashed
            'email': email,
            'created_at': datetime.now(),
            'is_admin': False
        }
        
        # ALGORITHM ISSUE: O(n) lookup to check duplicates
        for existing_user in self.users.values():
            if existing_user['username'] == username:
                raise ValueError("Username already exists")
        
        self.users[user['id']] = user
        self.save_users()
        return user
    
    # SECURITY: Mass assignment vulnerability
    def update_user(self, user_id: int, data: Dict[str, Any]) -> Dict:
        if user_id not in self.users:
            raise KeyError("User not found")
        
        # Allowing any field to be updated, including is_admin
        self.users[user_id].update(data)
        self.save_users()
        return self.users[user_id]
    
    # PERFORMANCE: Loading entire user list for simple operations
    def get_user_by_email(self, email: str) -> Dict:
        for user in self.users.values():
            if user['email'] == email:
                return user
        return None

# DESIGN ISSUE: Mixing concerns
class UserService:
    def __init__(self):
        self.store = UserStore()
        self.email_templates = {}
        self.audit_log = []
    
    # SECURITY: YAML can execute arbitrary code with load()
    def load_email_templates(self, config_file: str):
        with open(config_file, 'r') as f:
            # Should use yaml.safe_load()
            self.email_templates = yaml.load(f, Loader=yaml.Loader)
    
    # PERFORMANCE: Synchronous email sending blocks request
    def register_user(self, username: str, password: str, email: str):
        # Create user
        user = self.store.create_user(username, password, email)
        
        # Send welcome email synchronously
        self.send_welcome_email(user)
        
        # Log to audit
        self.audit_log.append({
            'action': 'user_registered',
            'user_id': user['id'],
            'timestamp': datetime.now()
        })
        
        return user
    
    # ALGORITHM: Inefficient permission checking
    def check_permission(self, user_id: int, resource: str, action: str) -> bool:
        user = self.store.users.get(user_id)
        if not user:
            return False
        
        # PERFORMANCE: Loading all permissions every time
        permissions = self.load_all_permissions()
        
        # O(n*m) complexity
        for perm in permissions:
            if perm['user_id'] == user_id:
                for allowed_resource in perm['resources']:
                    if allowed_resource == resource:
                        for allowed_action in perm['actions']:
                            if allowed_action == action:
                                return True
        
        return False
    
    def load_all_permissions(self) -> List[Dict]:
        # Simulating expensive database call
        return [
            {'user_id': 1, 'resources': ['posts', 'comments'], 'actions': ['read', 'write']},
            # ... more permissions
        ]
    
    # SECURITY: Command injection vulnerability
    def export_users(self, format: str, output_file: str):
        import os
        
        # SECURITY: User input directly in shell command
        if format == 'csv':
            os.system(f"python export_csv.py {output_file}")
        elif format == 'json':
            os.system(f"python export_json.py {output_file}")
        else:
            # SECURITY: Format string can contain shell commands
            os.system(f"python export_{format}.py {output_file}")
    
    # DESIGN: Tight coupling to external service
    def send_welcome_email(self, user: Dict):
        import smtplib
        
        # Hardcoded SMTP configuration
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.login('app@example.com', 'password123')
        
        # No error handling
        smtp.send_message(
            to=user['email'],
            subject='Welcome!',
            body=f"Welcome {user['username']}!"
        )
        
        smtp.quit()

# PERFORMANCE: No caching strategy
class UserCache:
    def __init__(self):
        self.cache = {}
    
    def get_user(self, user_id: int) -> Dict:
        # Always fetches from database
        return UserStore().users.get(user_id)
    
    def invalidate_user(self, user_id: int):
        # No-op since we're not actually caching
        pass

# ALGORITHM: Inefficient search implementation
def search_users(query: str, users: List[Dict]) -> List[Dict]:
    results = []
    
    # Multiple passes over the data
    # First pass: exact username matches
    for user in users:
        if user['username'].lower() == query.lower():
            results.append(user)
    
    # Second pass: username contains query
    for user in users:
        if query.lower() in user['username'].lower() and user not in results:
            results.append(user)
    
    # Third pass: email contains query
    for user in users:
        if query.lower() in user['email'].lower() and user not in results:
            results.append(user)
    
    return results

# DESIGN: Global function modifying state
def promote_to_admin(username: str):
    store = UserStore()
    
    # Linear search
    for user in store.users.values():
        if user['username'] == username:
            user['is_admin'] = True
            store.save_users()
            return True
    
    return False