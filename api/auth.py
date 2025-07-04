"""
Authentication endpoint with intentional security vulnerabilities.
This file is designed to test the Security Reviewer's ability to identify issues.
"""

import hashlib
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# SECURITY ISSUE 1: Hardcoded credentials (should be in environment variables)
SECRET_KEY = "super_secret_key_123"
DATABASE_PASSWORD = "admin123"

# SECURITY ISSUE 2: Weak hashing algorithm (MD5 instead of bcrypt/argon2)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# SECURITY ISSUE 3: SQL Injection vulnerability
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # SECURITY ISSUE 4: Direct string concatenation in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hash_password(password)}'"
    
    # SECURITY ISSUE 5: No connection encryption
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # SECURITY ISSUE 6: Executing raw SQL without parameterization
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        # SECURITY ISSUE 7: Returning sensitive user data including password hash
        return jsonify({
            'success': True,
            'user_id': user[0],
            'username': user[1],
            'password_hash': user[2],
            'api_key': user[3]
        })
    else:
        # SECURITY ISSUE 8: Information disclosure - revealing whether username exists
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
        if cursor.fetchone():
            return jsonify({'error': 'Invalid password'}), 401
        else:
            return jsonify({'error': 'User not found'}), 404

# SECURITY ISSUE 9: No rate limiting on authentication endpoint
@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.json.get('email')
    
    # SECURITY ISSUE 10: Using eval() with user input
    if eval(f"'{email}'.endswith('@admin.com')"):
        # SECURITY ISSUE 11: Predictable password reset token
        reset_token = hashlib.md5(email.encode()).hexdigest()[:8]
        return jsonify({'reset_token': reset_token})
    
    return jsonify({'message': 'Reset email sent'})

# SECURITY ISSUE 12: Debug mode enabled in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # SECURITY ISSUE 13: Binding to all interfaces