#!/usr/bin/env python3
"""
Test script to verify browser launching functionality
"""

from jarvis_basic import processCommand

def test_browser_commands():
    print("Testing Browser Commands:")
    print("="*50)
    
    # Test cases for browser commands
    test_cases = [
        "open chrome",
        "open firefox", 
        "open edge",
        "launch chrome",
        "start firefox app"
    ]
    
    for i, command in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: \"{command}\"")
        result = processCommand(command)
        print(f"   Result: {result}")
    
    print("\n" + "="*50)
    print("Browser command testing completed!")

if __name__ == "__main__":
    test_browser_commands()