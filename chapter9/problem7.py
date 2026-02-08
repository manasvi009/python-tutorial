with open("C:/Users/PC/Desktop/python/chapter9/logfile.txt", "r") as f:
    line_number = 1
    found = False

    for line in f:
        if "python" in line.lower():
            print(f"'python' found at line number {line_number}")
            found = True
        line_number += 1

if not found:
    print("'python' not found in the file")
