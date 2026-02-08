letter = input("Enter a letter : ")
f = open("C:/Users/PC/Desktop/python/chapter9/problem1/poems.txt" , "r")
poem = (f.read())

if letter in poem:
    print(f"letter {letter} is available in poem")
else:
    print(f"letter {letter} is not available in this poem")
f.close()