'''def rem(l , word):
    if word in l:
     l.remove(word)
     return l
l = ["harry" , "sohan" , "sonal" , "rahul"]
print(rem(l , "an"))'''


def rem(l, word):
    n = []
    for item in l:
        if item != word:
            n.append(item.replace(word, ""))
    return n

l = ["harry", "sohan", "sonal", "rahul", "an"]
print(rem(l, "an"))
