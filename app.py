"""
Main application file that demonstrates usage of the modules.
This allows reviewers to see how the components interact.
"""

from flask import Flask, request, jsonify
from api.auth import app as auth_app
from api.data_processor import DataProcessor
from api.search import SearchEngine
from api.config import ConfigManager, ApplicationManager

app = Flask(__name__)

# Initialize components
config = ConfigManager()
data_processor = DataProcessor()
search_engine = SearchEngine()
app_manager = ApplicationManager()

@app.route('/')
def home():
    return jsonify({
        'message': 'Code Review Test API',
        'endpoints': [
            '/login',
            '/search',
            '/process',
            '/config'
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

if __name__ == '__main__':
    # Running with debug=True (security issue)
    app.run(debug=True, port=5000)