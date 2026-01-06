#!/usr/bin/env python3
"""
Helper script to add training examples to coping-styles-examples.jsonl

Usage:
    python add_example.py
    # Interactive prompts guide you through adding an example
    
    # Or provide all args:
    python add_example.py --prompt "User's problem statement..." --styles "Frustrated,Disconnected" --code "relationship_anxiety"
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

# Path to the examples file
EXAMPLES_FILE = Path(__file__).parent.parent.parent / "data" / "coping-styles-examples.jsonl"

# Valid coping styles (from word-clusters.md)
VALID_STYLES = [
    "Disconnected", "Indulged", "Frustrated", "Sacrificing", "Deprived",
    "Omnipotent", "Symbiotic", "Frictive", "Premature", "Floaty",
    "Flighty", "Constricted"
]

def interactive_add():
    """Interactively add a new example"""
    print("=" * 80)
    print("Add New Training Example")
    print("=" * 80)
    
    # Get prompt
    print("\n📝 Enter the problem statement/prompt:")
    print("   (Press Enter twice when done)")
    lines = []
    while True:
        line = input()
        if line == "" and lines:
            break
        lines.append(line)
    prompt = " ".join(lines)
    
    # Get coping styles
    print(f"\n🎯 Valid coping styles: {', '.join(VALID_STYLES)}")
    print("   Enter styles (comma-separated):")
    styles_input = input().strip()
    coping_styles = [s.strip() for s in styles_input.split(",")]
    
    # Validate styles
    invalid = [s for s in coping_styles if s not in VALID_STYLES]
    if invalid:
        print(f"   ⚠️  Warning: Unknown styles: {invalid}")
        confirm = input("   Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            print("   Cancelled.")
            return
    
    # Get code (optional)
    print("\n🏷️  Enter a code/category (optional, e.g., 'relationship_anxiety', 'work_stress'):")
    code = input().strip() or None
    
    # Get raw diagnosis (optional)
    print("\n💬 Enter raw diagnosis text (optional, leave empty if not yet diagnosed):")
    raw_diagnosis = input().strip() or None
    
    # Get source
    print("\n📍 Source of this example (e.g., 'session_transcript_03', 'manual_creation'):")
    source = input().strip() or "manual_creation"
    
    # Create example
    example = {
        "prompt": prompt,
        "coping_styles": coping_styles,
        "metadata": {
            "source": source,
            "validated": False,
            "date_added": datetime.now().strftime("%Y-%m-%d")
        }
    }
    
    if code:
        example["code"] = code
    
    if raw_diagnosis:
        example["raw_diagnosis"] = raw_diagnosis
    
    # Preview
    print("\n" + "=" * 80)
    print("Preview:")
    print(json.dumps(example, indent=2))
    print("=" * 80)
    
    confirm = input("\n✅ Add this example? (y/n): ")
    if confirm.lower() == 'y':
        add_example(example)
        print(f"✅ Example added to {EXAMPLES_FILE}")
    else:
        print("❌ Cancelled.")

def add_example(example_dict):
    """Append an example to the JSONL file"""
    with open(EXAMPLES_FILE, 'a') as f:
        f.write(json.dumps(example_dict) + '\n')

def main():
    parser = argparse.ArgumentParser(description="Add training examples for coping styles classification")
    parser.add_argument('--prompt', help='Problem statement/prompt')
    parser.add_argument('--styles', help='Comma-separated coping styles')
    parser.add_argument('--code', help='Code/category for the example')
    parser.add_argument('--raw-diagnosis', help='Raw diagnosis text (optional)')
    parser.add_argument('--source', default='manual_creation', help='Source of the example')
    
    args = parser.parse_args()
    
    # If no args provided, use interactive mode
    if not args.prompt:
        interactive_add()
        return
    
    # Non-interactive mode
    coping_styles = [s.strip() for s in args.styles.split(",")]
    
    example = {
        "prompt": args.prompt,
        "coping_styles": coping_styles,
        "metadata": {
            "source": args.source,
            "validated": False,
            "date_added": datetime.now().strftime("%Y-%m-%d")
        }
    }
    
    if args.code:
        example["code"] = args.code
    
    if args.raw_diagnosis:
        example["raw_diagnosis"] = args.raw_diagnosis
    
    add_example(example)
    print(f"✅ Example added to {EXAMPLES_FILE}")

if __name__ == "__main__":
    main()

