f = open("C:/Users/PC/Desktop/python/chapter9/myfile.txt")
#lines = f.readlines()
#print(lines, type(lines))

'''line1 = f.readline()
print(line1)

line2 = f.readline()
print(line2)

line3 = f.readline()
print(line3)

line4 = f.readline()
print(line4)

line5 = f.readline()
print(line5)'''


#read file using while loop

line = f.readline()
while line != "":
    print(line.strip())
    line = f.readline()


f.close()


