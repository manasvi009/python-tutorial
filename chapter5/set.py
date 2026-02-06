s = set() #empty set
print(s)

a = {1, 2, 3, 4, 5}
print(a)

#functions of set
a.add(6)
print(a)
a.remove(3)
print(a)
a.discard(4)
print(a)
a.discard(10) #does not raise error if element is not present
print(a)
a.pop() #removes and returns an arbitrary element from the set
print(a)

b = {5, 6, 7, 8, 9}

print(a.union(b)) #returns a new set that is the union of a and b
print(a.intersection(b)) #returns a new set that is the intersection of a and b
print(a.difference(b)) #returns a new set that is the difference of a and b
print(a.symmetric_difference(b)) #returns a new set that is the symmetric difference of a and b

print(a.issubset(b)) #returns True if a is a subset of b
print(a.issuperset(b)) #returns True if a is a superset of b

#properties of set
print(len(a)) #returns the number of elements in the set
print(5 in a) #returns True if 5 is in the set
print(10 in a) #returns False if 10 is not in the set

#operations on set
c = a.copy() #returns a shallow copy of the set
print(c)
print(a == c) #returns True if a and c are equal
print(a is c) #returns False because a and c are different objects in memory
print(a.issubset(c)) #returns True because a is a subset of c
print(a.pop()) #removes and returns an arbitrary element from the set
print(a)

