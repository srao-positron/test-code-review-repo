"""
Main application file that demonstrates usage of the modules.
This allows reviewers to see how the components interact.
"""

from flask import Flask, request, jsonify
from api.auth import app as auth_app
from api.data_processor import DataProcessor
from api.search import SearchEngine
from api.config import ConfigManager, ApplicationManager
from api.user_management import UserService, search_users

app = Flask(__name__)

# Initialize components
config = ConfigManager()
data_processor = DataProcessor()
search_engine = SearchEngine()
app_manager = ApplicationManager()
user_service = UserService()

@app.route('/')
def home():
    return jsonify({
        'message': 'Code Review Test API',
        'endpoints': [
            '/login',
            '/search',
            '/process',
            '/config',
            '/users/register',
            '/users/search',
            '/users/export'
        ]
    })

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '')
    documents = request.json.get('documents', [])
    
    # Use the inefficient search
    results = []
    for doc in documents:
        positions = search_engine.search_text(doc.get('content', ''), query)
        if positions:
            results.append({
                'document': doc,
                'positions': positions,
                'score': len(positions)
            })
    
    # Use inefficient sorting
    sorted_results = search_engine.sort_results(results)
    return jsonify(sorted_results)

@app.route('/process', methods=['POST'])
def process():
    user_ids = request.json.get('user_ids', [])
    
    # This will trigger all the performance issues
    results = data_processor.process_users(user_ids)
    stats = data_processor.calculate_statistics(results)
    
    return jsonify({
        'processed': len(results),
        'stats': stats
    })

@app.route('/config', methods=['GET', 'POST'])
def config_endpoint():
    if request.method == 'GET':
        # Exposing all config (security issue)
        return jsonify(config.config)
    else:
        # Allowing config changes via API (security issue)
        key = request.json.get('key')
        value = request.json.get('value')
        config.set(key, value)
        return jsonify({'updated': True})

@app.route('/users/register', methods=['POST'])
def register_user():
    # No input validation (security issue)
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    
    try:
        user = user_service.register_user(username, password, email)
        return jsonify(user)
    except Exception as e:
        # Exposing internal error details (security issue)
        return jsonify({'error': str(e)}), 400

@app.route('/users/search', methods=['GET'])
def search_users_endpoint():
    query = request.args.get('q', '')
    
    # Fetching all users is inefficient
    all_users = list(user_service.store.users.values())
    results = search_users(query, all_users)
    
    return jsonify(results)

@app.route('/users/export', methods=['POST'])
def export_users():
    # Accepting format from user input (security issue)
    format = request.json.get('format', 'csv')
    output_file = request.json.get('output_file', 'users_export')
    
    # This has command injection vulnerability
    user_service.export_users(format, output_file)
    
    return jsonify({'message': f'Export initiated to {output_file}'})

if __name__ == '__main__':
    # Running with debug=True (security issue)
    app.run(debug=True, port=5000)