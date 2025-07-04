"""
Configuration management with intentional design issues.
This file is designed to test the System Design Reviewer's ability to identify issues.
"""

import json
import os

# DESIGN ISSUE 1: Global mutable state
CONFIG = {}
DATABASE_CONNECTIONS = []
CACHE_INSTANCES = {}

# DESIGN ISSUE 2: Singleton pattern with implementation issues
class ConfigManager:
    _instance = None
    
    def __new__(cls):
        # DESIGN ISSUE 3: Not thread-safe singleton
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # DESIGN ISSUE 4: Initialization happens every time instance is accessed
        self.config = self.load_config()
    
    # DESIGN ISSUE 5: Tight coupling to file system
    def load_config(self):
        with open('/etc/app/config.json', 'r') as f:
            return json.load(f)
    
    # DESIGN ISSUE 6: No validation or type checking
    def get(self, key):
        return self.config.get(key)
    
    # DESIGN ISSUE 7: Allowing runtime config mutations
    def set(self, key, value):
        self.config[key] = value
        # DESIGN ISSUE 8: Immediate file write on every change
        with open('/etc/app/config.json', 'w') as f:
            json.dump(self.config, f)

# DESIGN ISSUE 9: God object with too many responsibilities
class ApplicationManager:
    def __init__(self):
        self.config = ConfigManager()
        self.users = {}
        self.sessions = {}
        self.cache = {}
        self.database = None
        self.logger = None
        self.emailer = None
        self.metrics = None
        
    # DESIGN ISSUE 10: Violating single responsibility principle
    def handle_request(self, request):
        # Authentication
        user = self.authenticate_user(request)
        
        # Logging
        self.log_request(request)
        
        # Caching
        cached = self.check_cache(request)
        if cached:
            return cached
            
        # Database operation
        result = self.query_database(request)
        
        # Email notification
        self.send_email(user, result)
        
        # Metrics
        self.record_metrics(request, result)
        
        return result
    
    # DESIGN ISSUE 11: Methods that shouldn't be in this class
    def authenticate_user(self, request):
        pass
    
    def log_request(self, request):
        pass
    
    def check_cache(self, request):
        pass
    
    def query_database(self, request):
        pass
    
    def send_email(self, user, result):
        pass
    
    def record_metrics(self, request, result):
        pass

# DESIGN ISSUE 12: Static dependencies instead of dependency injection
class DatabaseService:
    def __init__(self):
        # DESIGN ISSUE 13: Hardcoded dependencies
        self.config = ConfigManager()
        self.connection_string = self.config.get('database_url')
        
    # DESIGN ISSUE 14: No abstraction/interface
    def query(self, sql):
        import psycopg2
        conn = psycopg2.connect(self.connection_string)
        # ...

# DESIGN ISSUE 15: Circular dependencies
class ServiceA:
    def __init__(self):
        self.service_b = ServiceB()
    
    def do_something(self):
        return self.service_b.get_data()

class ServiceB:
    def __init__(self):
        self.service_a = ServiceA()  # Circular dependency
    
    def get_data(self):
        return "data"

# DESIGN ISSUE 16: No abstraction layers
def process_payment(amount, card_number, cvv):
    # DESIGN ISSUE 17: Direct integration with external service
    import stripe
    stripe.api_key = CONFIG.get('stripe_key')
    
    # DESIGN ISSUE 18: Business logic mixed with infrastructure
    if amount > 10000:
        # DESIGN ISSUE 19: No event system, direct coupling
        send_fraud_alert(card_number)
    
    # DESIGN ISSUE 20: No error handling strategy
    charge = stripe.Charge.create(
        amount=amount,
        currency='usd',
        source=card_number
    )
    
    # DESIGN ISSUE 21: Synchronous operations that should be async
    update_inventory(charge.metadata)
    send_receipt_email(charge.receipt_email)
    update_analytics(charge)
    
    return charge

# DESIGN ISSUE 22: No clear module boundaries
def send_fraud_alert(card_number):
    # Reaching into other modules directly
    ApplicationManager().emailer.send_alert(card_number)

def update_inventory(metadata):
    # Direct database access from utility function
    DatabaseService().query("UPDATE inventory SET ...")

def send_receipt_email(email):
    # No message queue, direct sending
    ApplicationManager().emailer.send_receipt(email)

def update_analytics(charge):
    # Synchronous external API call
    import requests
    requests.post('https://analytics.example.com/api/track', json=charge)

# DESIGN ISSUE 23: No clear separation of concerns
class UserController:
    def create_user(self, data):
        # DESIGN ISSUE 24: Controller doing too much
        # Validation
        if not data.get('email'):
            raise ValueError("Email required")
        
        # Business logic
        if User.exists(data['email']):
            raise ValueError("User exists")
        
        # Database operation
        user = User.create(data)
        
        # External service call
        self.send_welcome_email(user)
        
        # Caching
        CACHE_INSTANCES['users'][user.id] = user
        
        return user

# DESIGN ISSUE 25: No configuration validation or schema
def load_environment_config():
    # Just reading environment variables without validation
    return {
        'database_url': os.environ.get('DATABASE_URL'),
        'api_key': os.environ.get('API_KEY'),
        'debug': os.environ.get('DEBUG'),
        # No defaults, no type conversion, no validation
    }