# Configuration file for authentication service
import os

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
PASSWORD_MIN_LENGTH = 8
SESSION_TIMEOUT_HOURS = 24

# Database settings
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///users.db')

# Email settings for password reset
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Rate limiting
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 30
