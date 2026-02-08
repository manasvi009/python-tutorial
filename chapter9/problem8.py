# Open source file in read mode
with open("this.txt", "r") as f:
    content = f.read()

# Open destination file in write mode
with open("copy.txt", "w") as f:
    f.write(content)

print("File copied successfully.")
