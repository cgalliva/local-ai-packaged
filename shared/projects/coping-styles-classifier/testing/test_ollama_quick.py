#!/usr/bin/env python3
"""Quick test of Ollama API"""

import requests
import json

def test_ollama():
    url = "http://localhost:11434/api/generate"
    
    system_prompt = """You are a classifier. Classify the statement into ONE of these styles:
DISCONNECTED, OMNIPOTENT, FLOATY

Return just the style name."""
    
    user_prompt = "I feel like I'm floating above my body, not really here."
    
    payload = {
        "model": "qwen3:8b",
        "prompt": f"{system_prompt}\n\n{user_prompt}",
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 100
        }
    }
    
    print("Calling Ollama...")
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    print("\nResponse:")
    print(json.dumps(result, indent=2))
    print("\n\nExtracted text:")
    print(result.get("response", ""))

if __name__ == "__main__":
    test_ollama()

