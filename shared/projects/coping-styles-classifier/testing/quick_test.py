#!/usr/bin/env python3
"""Quick test with just 1 model × 1 prompt × 1 test case"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import from main script
from run_ollama_tests import (
    call_ollama, extract_json_from_response,
    calculate_score, load_prompt, strip_specific_example,
    TEST_CASES
)

def quick_test():
    print("=" * 60)
    print("QUICK TEST: 1 model × 1 prompt × 1 test case")
    print("=" * 60)
    
    model = "qwen3:8b"
    prompt_file = "prompt-keywords-only.md"
    test_case = TEST_CASES[4]  # The "adulting" test case
    
    print(f"\nModel: {model}")
    print(f"Prompt: {prompt_file}")
    print(f"Test: #{test_case['id']} - {test_case['statement'][:50]}...")
    
    # Load and clean prompt
    print("\n1. Loading prompt...")
    prompt_content = load_prompt(prompt_file)
    print(f"   Original prompt: {len(prompt_content)} chars")
    
    cleaned_prompt = strip_specific_example(prompt_content, test_case['statement'])
    print(f"   Cleaned prompt: {len(cleaned_prompt)} chars")
    
    # Call LLM
    print("\n2. Calling Ollama (this may take 30-60 seconds)...")
    response = call_ollama(model, cleaned_prompt, test_case['statement'])
    
    if not response:
        print("   ✗ No response from model")
        return
    
    print(f"   ✓ Got response: {len(response)} chars")
    print(f"\n   First 200 chars of response:")
    print(f"   {response[:200]}")
    
    # Parse
    print("\n3. Parsing JSON...")
    parsed = extract_json_from_response(response)
    
    if not parsed:
        print("   ✗ Failed to parse JSON")
        print(f"\n   Full response:\n{response}")
        return
    
    print(f"   ✓ Parsed successfully")
    
    if "classifications" in parsed:
        print(f"   Found {len(parsed['classifications'])} classifications:")
        for c in parsed['classifications']:
            print(f"      - {c.get('style', 'N/A')} (conf: {c.get('confidence', 0)})")
    
    # Score
    print("\n4. Calculating score...")
    score, metrics = calculate_score(
        parsed.get("classifications", []),
        test_case["known_diagnosis"],
        test_case["expected_top_3"]
    )
    
    print(f"   Score: {score}/10")
    print(f"   Metrics: {metrics}")
    
    print("\n" + "=" * 60)
    print(f"✓ TEST COMPLETE")
    print("=" * 60)
    
    # Check results
    print(f"\nExpected: {', '.join(test_case['known_diagnosis'])}")
    print(f"Got:      {', '.join(metrics.get('returned_styles', []))}")
    
    if score >= 7.0:
        print("\n✅ GOOD SCORE - Script is working correctly!")
    elif score >= 4.0:
        print("\n⚠️  MODERATE SCORE - Script working, results need review")
    else:
        print("\n❌ LOW SCORE - May need prompt adjustment")

if __name__ == "__main__":
    try:
        quick_test()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

