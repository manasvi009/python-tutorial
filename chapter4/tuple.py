#tuples are immutable 
t = (1, 2, 3, 4, 5)
print(t[0])
print(t[1:3])
print(t[:2])     #print 0 to 2 number index
print(t[1:])     #print 1 to last index
print(t[:])      #print full tuple
# tuple slicing with skip value
print("tuple slicing with skip value\n")
print(t[0:5:2])   #print 0 to 5 index with skip value 2
print(t[::2])     #print full tuple with skip value 2
# tuple functions
print("tuple functions\n")
print("length of tuple is =", len(t))
print("count of 2 in tuple =", t.count(2))
print("index of 3 in tuple =", t.index(3))
print("maximum element in tuple is =", max(t))
print("minimum element in tuple is =", min(t))
print("type of tuple is =", type(t))
print("id of tuple is =", id(t))
print("length of tuple is =", len(t))
print("check if 3 is in tuple =", 3 in t)
print("check if 6 is not in tuple =", 6 not in t)
print("tuple after multiplying by 2 =", t * 2)
print("slicing tuple with step 2 =", t[::2])
print("tuple after deleting index 2 =", end=" ")
temp = list(t)
del temp[2]
t = tuple(temp)
print(t)
