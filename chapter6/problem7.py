post = '''hello my name is manasvi
        i am learning python programming
        i am enjoying it a lot
        python is a great language
        i am loving it'''

word = input("Enter a word to search: ")
if(word in post):
    print("The word is present in the post.")
else:
    print("The word is not present in this post.")