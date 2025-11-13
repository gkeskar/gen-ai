#!/usr/bin/env python
"""Test script to find working Gemini model names"""
import os
from dotenv import load_dotenv
import litellm

load_dotenv()

# Test different model name formats
model_names = [
    "gemini/gemini-1.5-flash",
    "gemini/gemini-1.5-flash-001",
    "gemini/gemini-1.5-flash-002",
    "gemini/gemini-1.5-flash-latest",
    "gemini/gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
]

print(f"GEMINI_API_KEY is set: {bool(os.getenv('GEMINI_API_KEY'))}")
print(f"GOOGLE_API_KEY is set: {bool(os.getenv('GOOGLE_API_KEY'))}\n")

for model in model_names:
    try:
        print(f"Testing {model}...", end=" ")
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": "Say 'OK' if you can read this"}],
            max_tokens=10
        )
        print(f"✅ SUCCESS")
        print(f"   Response: {response.choices[0].message.content}\n")
        break  # Stop after first success
    except Exception as e:
        error_msg = str(e).split('\n')[0][:100]
        print(f"❌ FAILED: {error_msg}")
