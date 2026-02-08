import os

# Old file name
old_name = "C:/Users/PC/Desktop/python/chapter9/myfile1.txt"

# New file name
new_name = "C:/Users/PC/Desktop/python/chapter9/renamed_by_python.txt"

# Rename the file
os.rename(old_name, new_name)

print("File renamed successfully.")
