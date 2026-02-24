#!/usr/bin/env python3
"""
Test script to verify YouTube functionality
"""

from jarvis_basic import processCommand

def test_youtube_commands():
    print("Testing YouTube Commands:")
    print("="*50)
    
    # Test cases for YouTube commands
    test_cases = [
        "open youtube",
        "play music on youtube",
        "search youtube for tutorials",
        "youtube play songs",
        "find cooking videos on youtube",
        "play latest news on youtube",
        "search youtube for funny videos",
        "play music videos on youtube"
    ]
    
    for i, command in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: \"{command}\"")
        result = processCommand(command)
        print(f"   Result: {result}")
    
    print("\n" + "="*50)
    print("YouTube command testing completed!")

if __name__ == "__main__":
    test_youtube_commands()