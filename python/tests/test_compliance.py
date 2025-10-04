"""Compliance tests against spec/test-vectors.json"""
import json
import os

def test_load_test_vectors():
    """Ensure test vectors can be loaded"""
    spec_path = os.path.join(os.path.dirname(__file__), '..', '..', 'spec', 'test-vectors.json')
    with open(spec_path) as f:
        vectors = json.load(f)
    assert 'test_cases' in vectors
    assert len(vectors['test_cases']) > 0

# Add tests that run your implementation against test vectors here
