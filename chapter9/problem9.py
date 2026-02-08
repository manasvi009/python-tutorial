# Open both files in read mode
f1 = open("C:/Users/PC/Desktop/python/chapter9/file1.txt", "r")
f2 = open("C:/Users/PC/Desktop/python/chapter9/file2.txt", "r")

# Read contents
content1 = f1.read()
content2 = f2.read()

# Compare contents
if content1 == content2:
    print("Both files are identical.")
else:
    print("Files are NOT identical.")

# Close files
f1.close()
f2.close()
