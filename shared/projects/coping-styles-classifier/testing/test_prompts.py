#!/usr/bin/env python3
"""
Automated testing script for Source Code classification prompts.
Tests 4 different prompts against 5 known-diagnosis test cases.
"""

import json
import os
from typing import Dict, List, Tuple
from datetime import datetime

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

PROMPTS = [
    "prompt-comprehensive.md",
    "prompt-keywords-only.md", 
    "prompt-semantic-only.md",
    "prompt-embodiment-only.md"
]


def load_prompt(prompt_file: str) -> str:
    """Load prompt content from markdown file."""
    filepath = os.path.join(os.path.dirname(__file__), prompt_file)
    with open(filepath, 'r') as f:
        return f.read()


def calculate_score(returned_styles: List[str], known_diagnosis: List[str], 
                    expected_top_3: List[str]) -> Tuple[int, Dict]:
    """
    Calculate score for a test case result.
    
    Returns:
        score (0-10)
        metrics dict with precision, recall, etc.
    """
    returned_set = set(s.split('(')[0].strip().upper() for s in returned_styles)
    known_set = set(known_diagnosis)
    expected_set = set(expected_top_3)
    
    # Calculate metrics
    true_positives = len(returned_set & known_set)
    false_positives = len(returned_set - known_set)
    false_negatives = len(known_set - returned_set)
    
    precision = true_positives / len(returned_set) if returned_set else 0
    recall = true_positives / len(known_set) if known_set else 0
    
    # Check top 3 ranking
    returned_top_3 = set([s.split('(')[0].strip().upper() for s in returned_styles[:3]])
    top_3_correct = len(returned_top_3 & expected_set)
    
    # Scoring logic
    if top_3_correct == 3 and true_positives >= len(expected_set):
        score = 10  # Perfect match
    elif top_3_correct >= 2 and true_positives >= 3:
        score = 7  # Partial match
    elif true_positives >= 2:
        score = 4  # Weak match
    else:
        score = 0  # Miss
    
    metrics = {
        "precision": precision,
        "recall": recall,
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "top_3_correct": top_3_correct
    }
    
    return score, metrics


def analyze_results(results: Dict) -> Dict:
    """Analyze overall performance across all test cases."""
    analysis = {
        "average_score": 0,
        "average_precision": 0,
        "average_recall": 0,
        "total_true_positives": 0,
        "total_false_positives": 0,
        "differentiations": {}
    }
    
    scores = [r["score"] for r in results["test_results"]]
    analysis["average_score"] = sum(scores) / len(scores) if scores else 0
    
    precisions = [r["metrics"]["precision"] for r in results["test_results"]]
    analysis["average_precision"] = sum(precisions) / len(precisions) if precisions else 0
    
    recalls = [r["metrics"]["recall"] for r in results["test_results"]]
    analysis["average_recall"] = sum(recalls) / len(recalls) if recalls else 0
    
    analysis["total_true_positives"] = sum(r["metrics"]["true_positives"] for r in results["test_results"])
    analysis["total_false_positives"] = sum(r["metrics"]["false_positives"] for r in results["test_results"])
    
    # Check critical differentiations
    for test in results["test_results"]:
        if test["test_case_id"] == 5:  # INDULGED test
            returned = [s.upper() for s in test["returned_styles"]]
            analysis["differentiations"]["indulged_vs_frustrated"] = "INDULGED" in returned
    
    return analysis


def generate_report(all_results: Dict) -> str:
    """Generate comprehensive markdown report."""
    report = f"""# Classification Prompt Test Results
    
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

"""
    
    # Rankings
    prompt_scores = [(name, data["analysis"]["average_score"]) 
                     for name, data in all_results.items()]
    prompt_scores.sort(key=lambda x: x[1], reverse=True)
    
    report += "### Overall Rankings\n\n"
    for i, (prompt, score) in enumerate(prompt_scores, 1):
        report += f"{i}. **{prompt}**: {score:.1f}/10\n"
    
    report += "\n---\n\n"
    
    # Detailed results for each prompt
    for prompt_name, data in all_results.items():
        report += f"## {prompt_name}\n\n"
        report += f"**Average Score**: {data['analysis']['average_score']:.1f}/10\n"
        report += f"**Precision**: {data['analysis']['average_precision']:.1%}\n"
        report += f"**Recall**: {data['analysis']['average_recall']:.1%}\n\n"
        
        report += "### Test Case Results\n\n"
        for result in data["test_results"]:
            report += f"#### Test Case {result['test_case_id']} - Score: {result['score']}/10\n\n"
            report += f"**Returned**: {', '.join(result['returned_styles'][:5])}\n\n"
            report += f"**Known**: {', '.join(result['known_diagnosis'])}\n\n"
            report += f"**Metrics**: Precision={result['metrics']['precision']:.1%}, "
            report += f"Recall={result['metrics']['recall']:.1%}\n\n"
            if result.get("notes"):
                report += f"**Notes**: {result['notes']}\n\n"
        
        report += "---\n\n"
    
    # Comparative analysis
    report += "## Comparative Analysis\n\n"
    report += "### Strengths by Prompt\n\n"
    
    for prompt_name, data in all_results.items():
        report += f"**{prompt_name}**:\n"
        if data['analysis']['average_score'] >= 8:
            report += "- ✓ Excellent overall performance\n"
        if data['analysis']['average_precision'] >= 0.75:
            report += "- ✓ High precision (low false positives)\n"
        if data['analysis']['average_recall'] >= 0.65:
            report += "- ✓ High recall (captures most diagnoses)\n"
        report += "\n"
    
    report += "### Recommendations\n\n"
    winner = prompt_scores[0][0]
    report += f"**Primary Recommendation**: Use **{winner}** for production\n\n"
    
    if prompt_scores[0][1] >= 8.5:
        report += "Performance exceeds optimal threshold (8.5/10). Ready for deployment.\n\n"
    elif prompt_scores[0][1] >= 7.0:
        report += "Performance meets minimum viable threshold (7.0/10). Consider refinements before deployment.\n\n"
    else:
        report += "Performance below threshold. Significant refinement needed.\n\n"
    
    return report


def main():
    """Run full test suite."""
    print("Source Code Classification Prompt Testing")
    print("=" * 60)
    
    all_results = {}
    
    for prompt_file in PROMPTS:
        print(f"\nTesting: {prompt_file}")
        print("-" * 60)
        
        # Load prompt
        prompt_content = load_prompt(prompt_file)
        
        results = {
            "prompt_file": prompt_file,
            "test_results": []
        }
        
        # Test each case
        for test_case in TEST_CASES:
            print(f"  Test Case {test_case['id']}...", end=" ")
            
            # HERE: In real implementation, call LLM with prompt + statement
            # For now, this is placeholder - manual testing required
            # returned_styles = call_llm(prompt_content, test_case['statement'])
            
            # Placeholder result structure
            result = {
                "test_case_id": test_case["id"],
                "statement": test_case["statement"][:100] + "...",
                "known_diagnosis": test_case["known_diagnosis"],
                "returned_styles": [],  # Will be populated by LLM
                "score": 0,
                "metrics": {},
                "notes": "Manual testing required - see manual results"
            }
            
            results["test_results"].append(result)
            print("Placeholder")
        
        # Analyze
        results["analysis"] = analyze_results(results)
        all_results[prompt_file] = results
    
    # Generate report
    report = generate_report(all_results)
    
    # Save report
    report_file = os.path.join(os.path.dirname(__file__), 
                                f"test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md")
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n\nReport saved to: {report_file}")
    print("\nNote: This script requires LLM API integration to run automatically.")
    print("See manual testing results for actual performance data.")


if __name__ == "__main__":
    main()

