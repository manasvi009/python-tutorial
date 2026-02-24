#!/usr/bin/env python3
"""
Simple test file to verify Chrome launching functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jarvis_basic import processCommand

def test_chrome_launch():
    print("🧪 Testing Chrome launch functionality...")
    print("Command: 'open chrome'")
    
    result = processCommand('open chrome')
    print(f"Result: {result}")
    
    if result:
        print("✅ Chrome launch test PASSED")
    else:
        print("❌ Chrome launch test FAILED")
    
    print("Test completed!")

if __name__ == "__main__":
    test_chrome_launch()