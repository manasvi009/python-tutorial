# Open the log file in read mode
with open("C:/Users/PC/Desktop/python/chapter9/logfile.txt", "r") as f:
    content = f.read()

# Check if 'python' exists in the file
if "python" in content.lower():
    print("The log file contains the word 'python'")
else:
    print("The log file does NOT contain the word 'python'")
