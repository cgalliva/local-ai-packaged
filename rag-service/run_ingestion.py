#!/usr/bin/env python3
"""
Quick ingestion script - runs inside Docker network via exec
"""
import requests
import time

print("=" * 80)
print("🚀 Starting Book Ingestion")
print("=" * 80)

url = "http://rag-service:8080/ingest"
payload = {"file_path": "SOURCE CODE full manuscript 2025.docx.md"}

print(f"\n📤 Sending request to: {url}")
print(f"📖 File: {payload['file_path']}")
print("\n⏳ This will take 5-10 minutes (creating ~261 embeddings)...")
print("   Watch Docker logs: docker logs -f sc-ai-rag-service\n")

try:
    start = time.time()
    response = requests.post(url, json=payload, timeout=900)
    elapsed = time.time() - start
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "=" * 80)
        print("✅ INGESTION COMPLETE!")
        print("=" * 80)
        print(f"Status: {result['status']}")
        print(f"Chunks Created: {result['total_chunks']}")
        print(f"Message: {result['message']}")
        print(f"Time Elapsed: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
        print("=" * 80)
    else:
        print(f"\n❌ Error {response.status_code}: {response.text}")
        
except requests.exceptions.Timeout:
    print("\n⚠️  Request timed out, but ingestion may still be running.")
    print("   Check logs: docker logs sc-ai-rag-service")
except Exception as e:
    print(f"\n❌ Error: {e}")

