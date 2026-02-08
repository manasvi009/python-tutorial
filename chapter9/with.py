f= open("C:/Users/PC/Desktop/python/chapter9/file.txt")
print(f.read())
f.close()


#this statement is written also like this 
with open("C:/Users/PC/Desktop/python/chapter9/file.txt") as f :
    print(f.read())

#You dont need to explicitly close the file 