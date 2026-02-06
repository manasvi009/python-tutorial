marks = {
    "manasvi" : 100,
    "pooja" : 70,
    "riya" : 80,
    "sonam" : 90,
}

print(marks)
print(marks["pooja"])
marks["riya"] = 95
print(marks)
marks["ankit"] = 85
print(marks)
del marks["sonam"]
print(marks)
print(len(marks))
print(marks.keys())
print(marks.values())
print(marks.items())
for key in marks:
    print(key, ":", marks[key])
total = sum(marks.values())
print("Total marks:", total)
average = total / len(marks)
print("Average marks:", average)
print(marks.pop("manasvi"))
