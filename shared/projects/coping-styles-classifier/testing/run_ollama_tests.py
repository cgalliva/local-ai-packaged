#!/usr/bin/env python3
"""
Automated testing script for Source Code classification prompts using Ollama.
Tests 4 prompts × 5 test cases × multiple LLM models.
"""

import json
import os
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import subprocess
import sys

# Test cases with known diagnoses
TEST_CASES = [
    {
        "id": 1,
        "statement": "I'm feeling all consumed and obsessed by this other person's presence. I'm worried that I'm slipping into like old patterns of giving way more than I'm actually receiving. And I feel really vulnerable. I feel like, like I can't even focus on anything else. And I'm like, scared for my little heart, like, I want to guard my little heart, because it's like, this outside entity is just like, please is, like, this big. Big, bad, scary, death, like sucking my life force energy. But I want it to be different. I want it to just be pure love, like what is which is also what I'm sensing at the same time.",
        "known_diagnosis": ["OMNIPOTENT", "FRUSTRATED", "PREMATURE", "CONSTRICTED", "FLOATY"],
        "expected_top_3": ["OMNIPOTENT", "PREMATURE", "CONSTRICTED"]
    },
    {
        "id": 2,
        "statement": "Um, so I just started dating this person, and it's like, triggered me, because I'm feel so anxious about, like, what's going to happen? Does he like me? It's really, like, destabilizing, and I don't like seeing that old behavior in me activated. I feel like, really needy and like Bucha. Trying to hide the fact that I'm needy and so uncomfortable in my body, and like, foggy, and like, just Yeah, consumed by it, and like, I'm thinking about it all the time, and like it's robbing me from my center.",
        "known_diagnosis": ["OMNIPOTENT", "SYMBIOTIC", "FRICTIVE", "DEPRIVED", "FLOATY", "FLIGHTY", "CONSTRICTED"],
        "expected_top_3": ["FRICTIVE", "OMNIPOTENT", "SYMBIOTIC"]
    },
    {
        "id": 3,
        "statement": "Okay, so back in August, I noticed that there was bubbling paint on my car in several different places, so I looked it up online for that model of car, and it said that it's an issue with that car. So I went to the dealership and I went. I took the car to the dealership where I bought it, and I showed them the paint, and they said that, yes, it is a problem, but that they don't fix it there, but they could file a claim with Jeep for me, since the car was still under warranty. So that was in August, and they told me that it might take a couple of months for me to hear back from them. So I checked in with them after a couple of months, and they told me there was still a couple of people ahead of me. And. Then I brought my car to be serviced another time and asked again. Following that, I got an email asking about my experience with the dealership, and if I had any issues. I shared the issue with the president of the company, and they said, although they couldn't help me, they would have somebody contact me. And that didn't happen. So I went there today to drop off my car for an oil change, and I asked about the problem again, and they again told me that there's two people ahead of me and that I will hear from them when they hear back from Jeep.",
        "known_diagnosis": ["DISCONNECTED", "FRUSTRATED", "SACRIFICING"],
        "expected_top_3": ["FRUSTRATED", "SACRIFICING", "DISCONNECTED"]
    },
    {
        "id": 4,
        "statement": "So I'm really struggling to be present. Currently, I find myself thinking about all of these things happening in the future and all these problems that I want to take care of, and all these things that I want to..I find myself being in the future a lot and focusing a lot on things that are coming up, focusing on other people's problems that I want to help them with my own challenges that I want to resolve instead of actually taking care of it in the moment, I'm just ruminating and thinking about ways that I can potentially do that in the future. So, yeah, just trying to understand what that's about and noticing the places in my day to day life, in my conversations and relationships where I'm already thinking ahead to the next thing or to solutions and not so much being in the moment.",
        "known_diagnosis": ["FRUSTRATED", "FLOATY", "CONSTRICTED", "PREMATURE", "OMNIPOTENT"],
        "expected_top_3": ["FLOATY", "PREMATURE", "OMNIPOTENT"]
    },
    {
        "id": 5,
        "statement": "So I have to really adult right now in my life. I have to rent a car, buy a car, and I have to book a flight, and the airport I want to book from isn't having flights when I need the flight, so I'm gonna have to go to another airport and, like, all these kind of technical need to sit down. Like, plan adult, be responsible. Choose. So, yeah, there's things I need to do that are adulting. I need to rent a car. I need to buy a car, mostly. And every time I need to really decide I feel resistance, so then I kind of avoid it, because it feels like a really big responsibility. And so instead, I think, okay, I'll just rent a car, and then when I try to rent a car, it doesn't work. Something's not working in the system. I can't and then I feel I can't figure this out. It's too adulty for me, and I get kind of frustrated, I guess. And then also with a flight, I need to book a flight at a certain date, and those dates are not available in the nearest airport, so I have to, like, sit down and plan a different route, yeah.",
        "known_diagnosis": ["INDULGED", "FRUSTRATED", "DISCONNECTED"],
        "expected_top_3": ["INDULGED", "FRUSTRATED", "DISCONNECTED"]
    }
]

# Default models to test
MODELS = [
    "qwen3:8b",              # Best for speed - 6.60/10 baseline
    "gpt-oss:120b",          # Best for accuracy - 6.80/10 baseline
]


def check_ollama():
    """Check if Ollama is installed and running."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Ollama is running")
            print("\nAvailable models:")
            print(result.stdout)
            return True
        else:
            print("✗ Ollama not responding")
            return False
    except FileNotFoundError:
        print("✗ Ollama not found. Install from: https://ollama.ai")
        return False


def get_available_models():
    """Get list of pulled models from Ollama."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    models.append(model_name)
            return models
        return []
    except:
        return []


def ensure_model(model_name: str):
    """Ensure model is pulled, pull if necessary."""
    available = get_available_models()
    if model_name not in available:
        print(f"\n📥 Pulling model: {model_name}")
        print("This may take several minutes...")
        result = subprocess.run(["ollama", "pull", model_name], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {model_name} ready")
            return True
        else:
            print(f"✗ Failed to pull {model_name}")
            return False
    return True


def strip_specific_example(prompt_content: str, test_statement: str) -> str:
    """
    Remove only the specific example that matches the test case being run.
    Keeps other examples intact so the prompt isn't handicapped.
    """
    # Find the Classification Examples section
    examples_start = prompt_content.find("## Classification Examples")
    
    if examples_start == -1:
        # No examples section, return as-is
        return prompt_content
    
    # Look for the test statement (or close variant) in the examples
    # We'll match by looking for distinctive phrases
    
    # Extract distinctive phrases from test statement (first 50 chars)
    test_snippet = test_statement[:80].lower()
    
    # Split prompt into sections
    sections = re.split(r'(### Example \d+)', prompt_content)
    
    cleaned_sections = [sections[0]]  # Keep everything before examples
    
    # Process example sections
    i = 1
    while i < len(sections):
        if i + 1 < len(sections):
            example_header = sections[i]
            example_content = sections[i + 1]
            
            # Check if this example contains our test statement
            if test_snippet not in example_content.lower():
                # Keep this example - it's not the one being tested
                cleaned_sections.append(example_header)
                cleaned_sections.append(example_content)
            else:
                # Skip this example - it's the one being tested
                pass
            
            i += 2
        else:
            cleaned_sections.append(sections[i])
            i += 1
    
    return ''.join(cleaned_sections)


def call_ollama(model: str, system_prompt: str, user_message: str) -> Optional[str]:
    """Call Ollama API with system prompt and user message."""
    try:
        # Prepare the full prompt
        full_prompt = f"""<|system|>
{system_prompt}

<|user|>
Analyze this statement and return JSON classification:

{user_message}

<|assistant|>
"""
        
        # Call Ollama
        result = subprocess.run(
            ["ollama", "run", model],
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error calling {model}: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"Timeout calling {model}")
        return None
    except Exception as e:
        print(f"Exception calling {model}: {e}")
        return None


def extract_json_from_response(response: str) -> Optional[Dict]:
    """Extract and parse JSON from LLM response."""
    if not response:
        return None
    
    # Try to find JSON in the response
    # Look for ```json blocks first
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except:
            pass
    
    # Try to find raw JSON object
    json_match = re.search(r'\{[^{}]*"classifications"[^{}]*\[.*?\].*?\}', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except:
            pass
    
    # Try parsing the whole response
    try:
        return json.loads(response)
    except:
        pass
    
    return None


def calculate_score(classifications: List[Dict], known_diagnosis: List[str], 
                    expected_top_3: List[str]) -> Tuple[float, Dict]:
    """
    Calculate score for a test case result.
    
    Returns:
        score (0-10)
        metrics dict with precision, recall, etc.
    """
    if not classifications:
        return 0.0, {
            "precision": 0,
            "recall": 0,
            "true_positives": 0,
            "false_positives": 0,
            "false_negatives": 0,
            "top_3_correct": 0
        }
    
    # Extract style names from classifications
    returned_styles = []
    for c in classifications:
        style = c.get("style", "")
        # Extract main style name (remove subtype in parentheses)
        main_style = style.split('(')[0].strip().upper()
        returned_styles.append(main_style)
    
    returned_set = set(returned_styles)
    known_set = set(s.upper() for s in known_diagnosis)
    expected_set = set(s.upper() for s in expected_top_3)
    
    # Calculate metrics
    true_positives = len(returned_set & known_set)
    false_positives = len(returned_set - known_set)
    false_negatives = len(known_set - returned_set)
    
    precision = true_positives / len(returned_set) if returned_set else 0
    recall = true_positives / len(known_set) if known_set else 0
    
    # Check top 3 ranking
    returned_top_3 = set(returned_styles[:3])
    top_3_correct = len(returned_top_3 & expected_set)
    
    # Scoring logic
    if top_3_correct == 3 and true_positives >= len(expected_set):
        score = 10.0  # Perfect match
    elif top_3_correct >= 2 and true_positives >= 3:
        score = 7.0  # Good match
    elif top_3_correct >= 2 and true_positives >= 2:
        score = 6.0  # Decent match
    elif true_positives >= 2:
        score = 4.0  # Weak match
    elif true_positives >= 1:
        score = 2.0  # Very weak
    else:
        score = 0.0  # Miss
    
    metrics = {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "top_3_correct": top_3_correct,
        "returned_styles": returned_styles[:5]
    }
    
    return score, metrics


def load_prompt(prompt_file: str) -> str:
    """Load prompt content from markdown file."""
    # Handle both absolute and relative paths
    if os.path.isabs(prompt_file):
        filepath = prompt_file
    elif os.path.exists(prompt_file):
        filepath = prompt_file
    else:
        # Fallback to old behavior (relative to script directory)
        filepath = os.path.join(os.path.dirname(__file__), prompt_file)
    
    with open(filepath, 'r') as f:
        return f.read()


def run_test_suite(prompt_files: List[str], output_dir: str = "."):
    """Run the complete test suite.
    
    Args:
        prompt_files: List of prompt file paths to test
        output_dir: Directory to save results (default: current directory)
    """
    print("=" * 80)
    print("SOURCE CODE CLASSIFICATION TESTING")
    print("=" * 80)
    
    # Check Ollama
    if not check_ollama():
        sys.exit(1)
    
    # Determine which models to use
    available_models = get_available_models()
    models_to_test = []
    
    print("\n" + "=" * 80)
    print("MODEL SELECTION")
    print("=" * 80)
    
    for model in MODELS:
        if model in available_models:
            models_to_test.append(model)
            print(f"✓ Will test: {model}")
        else:
            print(f"⚠️  Skipping {model} (not pulled)")
            # Auto-pull if needed (uncomment to enable):
            # if ensure_model(model):
            #     models_to_test.append(model)
    
    if not models_to_test:
        print("\n✗ No models available for testing")
        sys.exit(1)
    
    total_tests = len(prompt_files) * len(TEST_CASES) * len(models_to_test)
    print(f"\n📊 Will test {len(prompt_files)} prompts × {len(TEST_CASES)} cases × {len(models_to_test)} models")
    print(f"   = {total_tests} total tests")
    print(f"\n⏱️  Estimated time: {total_tests * 0.5:.0f}-{total_tests * 1:.0f} minutes")
    print("\n🚀 Starting tests...")
    
    # Store all results
    all_results = {}
    
    # Run tests
    for model in models_to_test:
        print(f"\n{'=' * 80}")
        print(f"TESTING MODEL: {model}")
        print("=" * 80)
        
        model_results = {}
        
        for prompt_file in prompt_files:
            print(f"\n{'-' * 80}")
            print(f"Prompt: {prompt_file}")
            print("-" * 80)
            
            # Load prompt (we'll clean it per test case)
            prompt_content = load_prompt(prompt_file)
            
            prompt_results = {
                "prompt_file": prompt_file,
                "model": model,
                "test_results": []
            }
            
            # Test each case
            for test_case in TEST_CASES:
                print(f"  Test {test_case['id']}: ", end="", flush=True)
                
                # Remove only THIS specific test case example from prompt
                cleaned_prompt = strip_specific_example(prompt_content, test_case['statement'])
                
                # Call LLM
                response = call_ollama(model, cleaned_prompt, test_case['statement'])
                
                # Parse response
                parsed = extract_json_from_response(response)
                
                if parsed and "classifications" in parsed:
                    # Calculate score
                    score, metrics = calculate_score(
                        parsed["classifications"],
                        test_case["known_diagnosis"],
                        test_case["expected_top_3"]
                    )
                    
                    result = {
                        "test_case_id": test_case["id"],
                        "score": score,
                        "metrics": metrics,
                        "raw_response": response[:200] + "..." if len(response) > 200 else response
                    }
                    
                    print(f"Score: {score:.1f}/10 | Returned: {', '.join(metrics['returned_styles'])}")
                else:
                    result = {
                        "test_case_id": test_case["id"],
                        "score": 0.0,
                        "metrics": {"error": "Failed to parse response"},
                        "raw_response": response[:200] if response else "No response"
                    }
                    print("✗ Failed to parse response")
                
                prompt_results["test_results"].append(result)
            
            # Calculate average score for this prompt
            scores = [r["score"] for r in prompt_results["test_results"]]
            avg_score = sum(scores) / len(scores) if scores else 0
            prompt_results["average_score"] = round(avg_score, 2)
            
            print(f"\n  → Average Score: {avg_score:.2f}/10")
            
            model_results[prompt_file] = prompt_results
        
        all_results[model] = model_results
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(output_dir, exist_ok=True)
    results_file = os.path.join(output_dir, f"test-results-{timestamp}.json")
    
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'=' * 80}")
    print(f"✓ Results saved to: {results_file}")
    
    # Generate report
    generate_report(all_results, timestamp, output_dir)


def generate_report(all_results: Dict, timestamp: str, output_dir: str = "."):
    """Generate comprehensive markdown report.
    
    Args:
        all_results: Test results dictionary
        timestamp: Timestamp string for filename
        output_dir: Directory to save report (default: current directory)
    """
    report = f"""# Source Code Classification Test Results

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

"""
    
    # Overall rankings by prompt (averaged across all models)
    prompt_scores = {}
    for model, model_results in all_results.items():
        for prompt_file, prompt_data in model_results.items():
            if prompt_file not in prompt_scores:
                prompt_scores[prompt_file] = []
            prompt_scores[prompt_file].append(prompt_data["average_score"])
    
    prompt_averages = {
        prompt: sum(scores) / len(scores) 
        for prompt, scores in prompt_scores.items()
    }
    
    sorted_prompts = sorted(prompt_averages.items(), key=lambda x: x[1], reverse=True)
    
    report += "### Overall Prompt Rankings (averaged across all models)\n\n"
    for i, (prompt, score) in enumerate(sorted_prompts, 1):
        report += f"{i}. **{prompt}**: {score:.2f}/10\n"
    
    report += "\n---\n\n"
    
    # Model performance
    model_scores = {}
    for model, model_results in all_results.items():
        scores = [data["average_score"] for data in model_results.values()]
        model_scores[model] = sum(scores) / len(scores) if scores else 0
    
    sorted_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)
    
    report += "### Model Performance (averaged across all prompts)\n\n"
    for i, (model, score) in enumerate(sorted_models, 1):
        report += f"{i}. **{model}**: {score:.2f}/10\n"
    
    report += "\n---\n\n"
    
    # Detailed results
    report += "## Detailed Results\n\n"
    
    for model, model_results in all_results.items():
        report += f"### Model: {model}\n\n"
        
        for prompt_file, prompt_data in model_results.items():
            report += f"#### {prompt_file}\n\n"
            report += f"**Average Score**: {prompt_data['average_score']:.2f}/10\n\n"
            
            report += "| Test | Score | Precision | Recall | Returned Styles |\n"
            report += "|------|-------|-----------|--------|------------------|\n"
            
            for result in prompt_data["test_results"]:
                if "error" not in result["metrics"]:
                    styles = ", ".join(result["metrics"]["returned_styles"][:3])
                    report += f"| {result['test_case_id']} | {result['score']:.1f}/10 | "
                    report += f"{result['metrics']['precision']:.0%} | "
                    report += f"{result['metrics']['recall']:.0%} | {styles} |\n"
                else:
                    report += f"| {result['test_case_id']} | ERROR | - | - | Parse failed |\n"
            
            report += "\n"
        
        report += "---\n\n"
    
    # Recommendations
    report += "## Recommendations\n\n"
    
    best_prompt = sorted_prompts[0][0]
    best_score = sorted_prompts[0][1]
    best_model = sorted_models[0][0]
    
    report += f"**Best Performing Combination**:\n"
    report += f"- Prompt: `{best_prompt}` ({best_score:.2f}/10)\n"
    report += f"- Model: `{best_model}` ({model_scores[best_model]:.2f}/10)\n\n"
    
    if best_score >= 8.5:
        report += "✅ Performance exceeds optimal threshold (8.5/10). **Ready for production**.\n\n"
    elif best_score >= 7.0:
        report += "⚠️ Performance meets minimum viable threshold (7.0/10). Consider refinements before deployment.\n\n"
    else:
        report += "❌ Performance below threshold. Significant refinement needed.\n\n"
    
    # Save report
    report_file = os.path.join(output_dir, f"test-report-{timestamp}.md")
    
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"✓ Report saved to: {report_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Test Source Code coping style classification prompts with Ollama',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Test single prompt
  python3 run_ollama_tests.py ../2026-01-01-comprehensive-baseline/prompts/prompt-comprehensive.md
  
  # Test multiple prompts
  python3 run_ollama_tests.py ../2026-01-01-comprehensive-baseline/prompts/*.md
  
  # Specify output directory
  python3 run_ollama_tests.py -o ../2026-01-01-comprehensive-baseline/results/ ../2026-01-01-comprehensive-baseline/prompts/prompt-comprehensive.md
        '''
    )
    
    parser.add_argument(
        'prompts',
        nargs='+',
        help='One or more prompt files to test'
    )
    parser.add_argument(
        '-o', '--output',
        default='.',
        help='Output directory for results (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Validate prompt files exist
    for prompt_file in args.prompts:
        if not os.path.exists(prompt_file):
            print(f"✗ Error: Prompt file not found: {prompt_file}")
            sys.exit(1)
    
    try:
        run_test_suite(args.prompts, args.output)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

