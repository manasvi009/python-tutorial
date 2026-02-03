import os

# select the directory whose contents you want to list
directory_path = "/"

#use the os module to list the contents of the directory
contents = os.listdir(directory_path)

# print the contents of the directory
print(contents)
