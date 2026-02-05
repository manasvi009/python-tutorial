#lists are mutable
# list creation
list=["apple" , "mango" , 56.8 , 100] 
print(list[0])
print(list[1:3])
print(list[:2])     #print 0 to 2 number index
print(list[1:])     #print 1 to last index      
print(list[:])      #print full list

# list slicing with skip value
print("list slicing with skip value\n")
print(list[0:3:2])   #print 0 to 3 index with skip value 2
print(list[::2])     #print full list with skip value 2

# list functions
print("list functions\n")
print("length of list is =", len(list))
list.append("banana")
print("list after append =", list)
list.insert(1, "grapes")
print("list after insert =", list)
list.remove(56.8)
list.pop()
print("list after remove and pop =", list)  
# list.sort()   #works only for homogeneous list
print("list after sort =", list)
list.reverse()
print("list after reverse =", list)
print("count of 'mango' in list =", list.count("mango"))
print("index of 'apple' in list =", list.index("apple"))
list2 = ["kiwi", "orange"]
list.extend(list2)
print("list after extend =", list)
list.clear()
print("list after clear =", list)
list = ["apple" , "mango" , 56.8 , 100]
print("copy of list =", list.copy())
print("maximum element in list is =", max(["apple" , "mango" , "banana"]))
print("minimum element in list is =", min(["apple" , "mango" , "banana"]))
# print("reversed list is =", list(reversed(list)))
print("sorted list is =", sorted(["apple" , "mango" , "banana"]))
print("sum of numeric elements in list is =", sum([10, 20, 30, 40]))
# print("enumerate of list is =", list(enumerate(list)))
print("type of list is =", type(list))
print("id of list is =", id(list))
print("length of list is =", len(list))
print("check if 'mango' is in list =", "mango" in list)
print("check if 'banana' is not in list =", "banana" not in list)
print("max length element in list is =", max(["apple" , "mango" , "banana"], key=len))
print("min length element in list is =", min(["apple" , "mango" , "banana"], key=len))
print("sum of numeric elements in list with start value 10 is =", sum([10, 20, 30, 40], 10))
print("all elements in list are true =", all([1, 2, 3, 4]))
print("any element in list is true =", any([0, 0, 3, 0]))
print("list after multiplying by 2 =", list * 2)
print("joining list elements with '-' =", '-'.join(["apple" , "mango" , "banana"]))
print("slicing list with step 2 =", list[::2])
print("list after deleting index 2 =", end=" ")
