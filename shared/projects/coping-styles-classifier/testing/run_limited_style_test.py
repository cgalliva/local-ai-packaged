#!/usr/bin/env python3
"""
Test runner for prompts with limited style coverage.
Only grades on styles that are actually in the prompt.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Test cases
TEST_CASES = [
    {
        "id": 1,
        "statement": "I'm feeling all consumed and obsessed by this other person's presence. I'm worried that I'm slipping into like old patterns of giving way more than I'm actually receiving. And I feel really vulnerable. I feel like, like I can't even focus on anything else. And I'm like, scared for my little heart, like, I want to guard my little heart, because it's like, this outside entity is just like, please is, like, this big. Big, bad, scary, death, like sucking my life force energy. But I want it to be different. I want it to just be pure love, like what is which is also what I'm sensing at the same time.",
        "full_diagnosis": ["OMNIPOTENT", "FRUSTRATED", "PREMATURE", "CONSTRICTED", "FLOATY"],
        "available_diagnosis": ["OMNIPOTENT", "FLOATY"],  # Only styles in the limited prompt
        "expected_top": ["OMNIPOTENT", "FLOATY"]
    },
    {
        "id": 2,
        "statement": "Um, so I just started dating this person, and it's like, triggered me, because I'm feel so anxious about, like, what's going to happen? Does he like me? It's really, like, destabilizing, and I don't like seeing that old behavior in me activated. I feel like, really needy and like Bucha. Trying to hide the fact that I'm needy and so uncomfortable in my body, and like, foggy, and like, just Yeah, consumed by it, and like, I'm thinking about it all the time, and like it's robbing me from my center.",
        "full_diagnosis": ["OMNIPOTENT", "SYMBIOTIC", "FRICTIVE", "DEPRIVED", "FLOATY", "FLIGHTY", "CONSTRICTED"],
        "available_diagnosis": ["OMNIPOTENT", "SYMBIOTIC", "FRICTIVE", "DEPRIVED", "FLOATY", "FLIGHTY"],
        "expected_top": ["FRICTIVE", "OMNIPOTENT", "SYMBIOTIC"]
    },
    {
        "id": 3,
        "statement": "Okay, so back in August, I noticed that there was bubbling paint on my car in several different places, so I looked it up online for that model of car, and it said that it's an issue with that car. So I went to the dealership and I went. I took the car to the dealership where I bought it, and I showed them the paint, and they said that, yes, it is a problem, but that they don't fix it there, but they could file a claim with Jeep for me, since the car was still under warranty. So that was in August, and they told me that it might take a couple of months for me to hear back from them. So I checked in with them after a couple of months, and they told me there was still a couple of people ahead of me. And. Then I brought my car to be serviced another time and asked again. Following that, I got an email asking about my experience with the dealership, and if I had any issues. I shared the issue with the president of the company, and they said, although they couldn't help me, they would have somebody contact me. And that didn't happen. So I went there today to drop off my car for an oil change, and I asked about the problem again, and they again told me that there's two people ahead of me and that I will hear from them when they hear back from Jeep.",
        "full_diagnosis": ["DISCONNECTED", "FRUSTRATED", "SACRIFICING"],
        "available_diagnosis": ["DISCONNECTED"],
        "expected_top": ["DISCONNECTED"]
    },
    {
        "id": 4,
        "statement": "So I'm really struggling to be present. Currently, I find myself thinking about all of these things happening in the future and all these problems that I want to take care of, and all these things that I want to..I find myself being in the future a lot and focusing a lot on things that are coming up, focusing on other people's problems that I want to help them with my own challenges that I want to resolve instead of actually taking care of it in the moment, I'm just ruminating and thinking about ways that I can potentially do that in the future. So, yeah, just trying to understand what that's about and noticing the places in my day to day life, in my conversations and relationships where I'm already thinking ahead to the next thing or to solutions and not so much being in the moment.",
        "full_diagnosis": ["FRUSTRATED", "FLOATY", "CONSTRICTED", "PREMATURE", "OMNIPOTENT"],
        "available_diagnosis": ["FLOATY", "OMNIPOTENT"],
        "expected_top": ["FLOATY", "OMNIPOTENT"]
    },
    {
        "id": 5,
        "statement": "So I have to really adult right now in my life. I have to rent a car, buy a car, and I have to book a flight, and the airport I want to book from isn't having flights when I need the flight, so I'm gonna have to go to another airport and, like, all these kind of technical need to sit down. Like, plan adult, be responsible. Choose. So, yeah, there's things I need to do that are adulting. I need to rent a car. I need to buy a car, mostly. And every time I need to really decide I feel resistance, so then I kind of avoid it, because it feels like a really big responsibility. And so instead, I think, okay, I'll just rent a car, and then when I try to rent a car, it doesn't work. Something's not working in the system. I can't and then I feel I can't figure this out. It's too adulty for me, and I get kind of frustrated, I guess. And then also with a flight, I need to book a flight at a certain date, and those dates are not available in the nearest airport, so I have to, like, sit down and plan a different route, yeah.",
        "full_diagnosis": ["INDULGED", "FRUSTRATED", "DISCONNECTED"],
        "available_diagnosis": ["DISCONNECTED"],
        "expected_top": ["DISCONNECTED"]
    }
]

# Models to test
MODELS = [
    "qwen3:8b",
    "qwen3-coder:30b-a3b-q8_0",
    "gpt-oss:120b"
]

# Styles available in the limited prompt
AVAILABLE_STYLES = {
    "DISCONNECTED", "FLIGHTY", "FLOATY", "STIFF", "MASKED",
    "FRICTIVE", "OMNIPOTENT", "DEPRIVED", 
    "WOUNDED", "INDISPENSABLE", "ELUSIVE", "PURSUING", 
    "CHARMING", "SCAVENGING", "STOCKPILING", "SYMBIOTIC"
}

def call_ollama(model, system_prompt, user_prompt):
    """Call Ollama HTTP API with given prompts."""
    import requests
    
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": f"{system_prompt}\n\nUSER: {user_prompt}\n\nASSISTANT:",
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 1000  # Increased to allow full response
            }
        }
        
        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()
        
        result = response.json()
        
        # Check both 'response' and 'thinking' fields (qwen3 uses 'thinking')
        response_text = result.get("response", "").strip()
        thinking_text = result.get("thinking", "").strip()
        
        # Return whichever has content, prefer response over thinking
        if response_text:
            return response_text
        elif thinking_text:
            return thinking_text
        else:
            return ""
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def parse_response(response):
    """Parse model response to extract styles."""
    if not response:
        return []
    
    import re
    import json
    styles = []
    
    # Try to parse as JSON first
    try:
        # Look for JSON object or array
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            # Extract from various JSON structures
            if "classifications" in data:
                for item in data["classifications"]:
                    style = item.get("style", "").upper()
                    if style in AVAILABLE_STYLES and style not in styles:
                        styles.append(style)
            elif "styles" in data:
                for style in data["styles"]:
                    style_name = style.upper() if isinstance(style, str) else style.get("name", "").upper()
                    if style_name in AVAILABLE_STYLES and style_name not in styles:
                        styles.append(style_name)
    except:
        pass
    
    # If no JSON or JSON parsing failed, look for style names in text
    if not styles:
        # Look for all-caps words that match known styles
        for style in AVAILABLE_STYLES:
            # Match whole word only
            if re.search(r'\b' + style + r'\b', response.upper()):
                if style not in styles:
                    styles.append(style)
    
    return styles[:5]  # Return top 5

def calculate_limited_score(predicted, available_diagnosis, expected_top):
    """
    Calculate score based only on available styles.
    
    Scoring:
    - 2 points for each correct style in available_diagnosis found
    - 1 bonus point if top prediction matches expected_top[0]
    - -1 point for each style predicted that's NOT in AVAILABLE_STYLES (shouldn't happen)
    """
    score = 0
    max_score = len(available_diagnosis) * 2 + 1  # Max points possible
    
    # Points for correct predictions
    for style in predicted:
        if style in available_diagnosis:
            score += 2
        elif style not in AVAILABLE_STYLES:
            # Penalty for predicting unavailable styles
            score -= 1
    
    # Bonus for correct top prediction
    if predicted and expected_top and predicted[0] == expected_top[0]:
        score += 1
    
    # Normalize to 0-10 scale
    if max_score > 0:
        normalized_score = (score / max_score) * 10
        return max(0, min(10, normalized_score))  # Clamp between 0-10
    return 0

def run_tests(prompt_file):
    """Run all test cases against specified prompt file."""
    print(f"\n{'='*80}")
    print(f"Testing: {prompt_file}")
    print(f"{'='*80}\n")
    
    # Read prompt file
    with open(prompt_file, 'r') as f:
        system_prompt = f.read()
    
    results = {
        "prompt_file": str(prompt_file),
        "timestamp": datetime.now().isoformat(),
        "models": {},
        "available_styles": list(AVAILABLE_STYLES)
    }
    
    for model in MODELS:
        print(f"\n--- Testing with {model} ---\n")
        model_results = {
            "scores": [],
            "details": []
        }
        
        for test_case in TEST_CASES:
            print(f"Test {test_case['id']}: ", end="", flush=True)
            
            user_prompt = f"Classify this statement:\n\n{test_case['statement']}"
            
            response = call_ollama(model, system_prompt, user_prompt)
            predicted = parse_response(response)
            
            score = calculate_limited_score(
                predicted,
                test_case['available_diagnosis'],
                test_case['expected_top']
            )
            
            model_results["scores"].append(score)
            model_results["details"].append({
                "test_id": test_case['id'],
                "full_diagnosis": test_case['full_diagnosis'],
                "available_diagnosis": test_case['available_diagnosis'],
                "predicted": predicted,
                "score": score,
                "response": response[:500] if response else None
            })
            
            print(f"Score: {score:.1f}/10")
            print(f"  Available: {test_case['available_diagnosis']}")
            print(f"  Predicted: {predicted}")
            print()
        
        avg_score = sum(model_results["scores"]) / len(model_results["scores"])
        model_results["average_score"] = avg_score
        results["models"][model] = model_results
        
        print(f"Average for {model}: {avg_score:.2f}/10\n")
    
    return results

def generate_report(results, output_dir="."):
    """Generate markdown report.
    
    Args:
        results: Test results dictionary
        output_dir: Directory to save report (default: current directory)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"test-report-limited-{timestamp}.md")
    
    with open(report_file, 'w') as f:
        f.write(f"# Limited Style Test Report\n\n")
        f.write(f"**Prompt File**: {results['prompt_file']}\n\n")
        f.write(f"**Timestamp**: {results['timestamp']}\n\n")
        f.write(f"**Available Styles**: {', '.join(sorted(results['available_styles']))}\n\n")
        f.write(f"---\n\n")
        
        f.write("## Summary\n\n")
        f.write("| Model | Avg Score | Grade |\n")
        f.write("|-------|-----------|-------|\n")
        for model, data in results['models'].items():
            grade = "✅ Good" if data['average_score'] >= 7 else "⚠️ Fair" if data['average_score'] >= 5 else "❌ Poor"
            f.write(f"| {model} | {data['average_score']:.2f}/10 | {grade} |\n")
        
        f.write("\n---\n\n")
        
        f.write("## Detailed Results\n\n")
        for model, data in results['models'].items():
            f.write(f"### {model}\n\n")
            for detail in data['details']:
                f.write(f"#### Test {detail['test_id']} - Score: {detail['score']:.1f}/10\n\n")
                f.write(f"**Full Original Diagnosis**: {', '.join(detail['full_diagnosis'])}\n\n")
                f.write(f"**Available for Grading**: {', '.join(detail['available_diagnosis'])}\n\n")
                f.write(f"**Model Predicted**: {', '.join(detail['predicted']) if detail['predicted'] else 'None'}\n\n")
                f.write("---\n\n")
    
    print(f"\n✅ Report saved to: {report_file}")
    return report_file

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Test limited-style classification prompts with Ollama',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Test single prompt
  python3 run_limited_style_test.py ../2026-01-02-keywords-experiments/prompts/prompt-keywords-with-shared.md
  
  # Specify output directory
  python3 run_limited_style_test.py -o ../2026-01-02-keywords-experiments/results/ ../2026-01-02-keywords-experiments/prompts/prompt-keywords-with-shared.md
        '''
    )
    
    parser.add_argument(
        'prompt',
        help='Prompt file to test'
    )
    parser.add_argument(
        '-o', '--output',
        default='.',
        help='Output directory for results (default: current directory)'
    )
    
    args = parser.parse_args()
    prompt_file = Path(args.prompt)
    output_dir = args.output
    
    if not prompt_file.exists():
        print(f"Error: Prompt file not found: {prompt_file}")
        sys.exit(1)
    
    print("🚀 Starting Limited Style Test Suite")
    print(f"Testing {len(TEST_CASES)} cases with {len(MODELS)} models")
    print(f"Available styles: {len(AVAILABLE_STYLES)}")
    
    results = run_tests(prompt_file)
    
    # Save JSON results
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = os.path.join(output_dir, f"test-results-limited-{timestamp}.json")
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✅ Results saved to: {json_file}")
    
    # Generate report
    report_file = generate_report(results, output_dir)
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)

