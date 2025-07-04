"""
Search implementation with intentional algorithmic inefficiencies.
This file is designed to test the Algorithms Reviewer's ability to identify issues.
"""

from typing import List, Tuple, Optional
import math

class SearchEngine:
    def __init__(self):
        self.data = []
    
    # ALGORITHM ISSUE 1: Bubble sort instead of more efficient sorting algorithm
    def sort_results(self, results: List[dict]) -> List[dict]:
        n = len(results)
        for i in range(n):
            for j in range(0, n-i-1):
                if results[j]['score'] < results[j+1]['score']:
                    results[j], results[j+1] = results[j+1], results[j]
        return results
    
    # ALGORITHM ISSUE 2: Linear search instead of binary search on sorted data
    def find_document(self, documents: List[dict], doc_id: int) -> Optional[dict]:
        # Assuming documents are sorted by ID, but using linear search
        for doc in documents:
            if doc['id'] == doc_id:
                return doc
        return None
    
    # ALGORITHM ISSUE 3: Inefficient substring search
    def search_text(self, text: str, pattern: str) -> List[int]:
        # Naive substring search O(n*m) instead of KMP or Boyer-Moore
        positions = []
        for i in range(len(text) - len(pattern) + 1):
            match = True
            for j in range(len(pattern)):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                positions.append(i)
        return positions
    
    # ALGORITHM ISSUE 4: Recursive Fibonacci without memoization
    def calculate_relevance_score(self, n: int) -> int:
        # Using Fibonacci as a contrived scoring mechanism
        if n <= 1:
            return n
        return self.calculate_relevance_score(n-1) + self.calculate_relevance_score(n-2)
    
    # ALGORITHM ISSUE 5: Inefficient duplicate detection
    def remove_duplicates(self, items: List[int]) -> List[int]:
        # O(n²) approach instead of using a set
        unique = []
        for item in items:
            is_duplicate = False
            for unique_item in unique:
                if item == unique_item:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique.append(item)
        return unique
    
    # ALGORITHM ISSUE 6: Inefficient graph traversal
    def find_related_documents(self, doc_id: int, relationships: dict) -> List[int]:
        # BFS without visited set, can revisit nodes
        queue = [doc_id]
        related = []
        
        while queue:
            current = queue.pop(0)  # ALGORITHM ISSUE 7: Using list as queue (O(n) pop)
            related.append(current)
            
            if current in relationships:
                for neighbor in relationships[current]:
                    # ALGORITHM ISSUE 8: No check for already visited nodes
                    queue.append(neighbor)
        
        return related[:10]  # Limiting to prevent infinite loop
    
    # ALGORITHM ISSUE 9: Inefficient prime checking
    def is_prime_score(self, n: int) -> bool:
        # Checking all numbers up to n instead of sqrt(n)
        if n < 2:
            return False
        for i in range(2, n):
            if n % i == 0:
                return False
        return True
    
    # ALGORITHM ISSUE 10: Inefficient matrix multiplication
    def calculate_similarity_matrix(self, vectors: List[List[float]]) -> List[List[float]]:
        n = len(vectors)
        similarity = [[0.0] * n for _ in range(n)]
        
        # ALGORITHM ISSUE 11: Recalculating norms repeatedly
        for i in range(n):
            for j in range(n):
                # Calculating dot product and norms from scratch each time
                dot_product = sum(vectors[i][k] * vectors[j][k] for k in range(len(vectors[i])))
                norm_i = math.sqrt(sum(x**2 for x in vectors[i]))
                norm_j = math.sqrt(sum(x**2 for x in vectors[j]))
                
                if norm_i * norm_j > 0:
                    similarity[i][j] = dot_product / (norm_i * norm_j)
        
        return similarity
    
    # ALGORITHM ISSUE 12: Inefficient ranking algorithm
    def rank_results(self, results: List[dict]) -> List[dict]:
        # Multiple passes over data when one would suffice
        # First pass: calculate max score
        max_score = 0
        for result in results:
            if result['score'] > max_score:
                max_score = result['score']
        
        # Second pass: normalize scores
        for result in results:
            result['normalized_score'] = result['score'] / max_score if max_score > 0 else 0
        
        # Third pass: sort (using inefficient bubble sort from above)
        return self.sort_results(results)
    
    # ALGORITHM ISSUE 13: Inefficient set operations
    def find_common_terms(self, doc1_terms: List[str], doc2_terms: List[str]) -> List[str]:
        # O(n*m) intersection instead of using sets
        common = []
        for term1 in doc1_terms:
            for term2 in doc2_terms:
                if term1 == term2 and term1 not in common:
                    common.append(term1)
        return common
    
    # ALGORITHM ISSUE 14: Poor hash function causing collisions
    def simple_hash(self, key: str, table_size: int) -> int:
        # Just using first character - will cause many collisions
        return ord(key[0]) % table_size if key else 0
    
    # ALGORITHM ISSUE 15: Inefficient median finding
    def find_median_score(self, scores: List[float]) -> float:
        # Sorting entire array just to find median
        sorted_scores = self.sort_results([{'score': s} for s in scores])
        scores_only = [item['score'] for item in sorted_scores]
        
        n = len(scores_only)
        if n % 2 == 0:
            return (scores_only[n//2 - 1] + scores_only[n//2]) / 2
        else:
            return scores_only[n//2]