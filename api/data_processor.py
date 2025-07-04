"""
Data processing module with intentional performance and scalability issues.
This file is designed to test the Operations Reviewer's ability to identify issues.
"""

import json
import time
from typing import List, Dict

class DataProcessor:
    def __init__(self):
        # PERFORMANCE ISSUE 1: Loading entire dataset into memory
        self.cached_data = []
        
    # PERFORMANCE ISSUE 2: Synchronous I/O blocking operations
    def load_data(self, filename: str):
        with open(filename, 'r') as f:
            # PERFORMANCE ISSUE 3: Loading entire file at once instead of streaming
            data = json.load(f)
            
        # PERFORMANCE ISSUE 4: No pagination or chunking for large datasets
        return data
    
    # PERFORMANCE ISSUE 5: N+1 query problem
    def process_users(self, user_ids: List[int]):
        results = []
        for user_id in user_ids:
            # PERFORMANCE ISSUE 6: Individual database call for each user
            user = self.fetch_user_from_db(user_id)
            # PERFORMANCE ISSUE 7: Nested loop creating O(n²) complexity
            for order in self.fetch_orders_for_user(user_id):
                # PERFORMANCE ISSUE 8: Another nested database call
                for item in self.fetch_items_for_order(order['id']):
                    results.append({
                        'user': user,
                        'order': order,
                        'item': item
                    })
        return results
    
    # PERFORMANCE ISSUE 9: No caching mechanism
    def calculate_statistics(self, data: List[Dict]):
        stats = {}
        
        # PERFORMANCE ISSUE 10: Inefficient string concatenation in loop
        report = ""
        for item in data:
            report += f"Processing item {item['id']}\n"  # Should use list and join
            
            # PERFORMANCE ISSUE 11: Recalculating same values repeatedly
            total = sum([x['value'] for x in data])
            average = total / len(data)
            
            # PERFORMANCE ISSUE 12: Creating new list copies unnecessarily
            sorted_data = sorted(data, key=lambda x: x['value'])
            filtered_data = [x for x in sorted_data if x['value'] > average]
            
        return stats
    
    # PERFORMANCE ISSUE 13: Blocking sleep in async context
    def process_batch(self, items: List[Dict]):
        processed = []
        for item in items:
            # PERFORMANCE ISSUE 14: Serial processing instead of parallel
            time.sleep(0.1)  # Simulating processing time
            processed.append(self.transform_item(item))
        return processed
    
    # PERFORMANCE ISSUE 15: Memory leak - growing list without bounds
    def add_to_cache(self, item):
        self.cached_data.append(item)
        # No cache eviction strategy
        
    # PERFORMANCE ISSUE 16: Inefficient search algorithm
    def find_item(self, items: List[Dict], target_id: int):
        # Linear search instead of using a dictionary or index
        for item in items:
            if item['id'] == target_id:
                return item
        return None
    
    # PERFORMANCE ISSUE 17: No connection pooling
    def fetch_user_from_db(self, user_id: int):
        # Creating new connection for each request
        import sqlite3
        conn = sqlite3.connect('database.db')
        # ... fetch user ...
        conn.close()
        return {'id': user_id}
    
    # PERFORMANCE ISSUE 18: No query optimization
    def fetch_orders_for_user(self, user_id: int):
        # Fetching all columns when only few are needed
        return [{'id': 1, 'user_id': user_id, 'data': 'x' * 1000}]
    
    def fetch_items_for_order(self, order_id: int):
        return [{'id': 1, 'order_id': order_id}]
    
    def transform_item(self, item: Dict) -> Dict:
        # PERFORMANCE ISSUE 19: Deep copying when not necessary
        import copy
        return copy.deepcopy(item)
    
    # PERFORMANCE ISSUE 20: No resource limits
    def generate_report(self, data: List[Dict]):
        # Could consume unlimited memory/CPU for large inputs
        result = []
        for i in range(len(data)):
            for j in range(len(data)):
                result.append(f"{data[i]} compared to {data[j]}")
        return result