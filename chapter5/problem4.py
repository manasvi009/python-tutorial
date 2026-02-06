s = set()
s.add(20)
s.add(20.0)
s.add("20")
#length of set is 2 because 20 and 20.0 are considered the same element in a set
print(s)
print(len(s))