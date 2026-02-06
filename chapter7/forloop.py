#range function in for loop
for i in range(1,6):
    print(i)


#for loop with list
list=[67,89,67,90]
for i in list:
     print(i)

#   for loop with touple
touple = (78,57,40,30)
for i in touple:
     print(i)

#for loop with string
for i in "manasvi":
    print(i)
#nested for loop
for i in range(1,4):
    for j in range(1,4):
        print(i,j)
# print multiplication table of a number using for loop
num = int(input("Enter a number to print its multiplication table: "))
for i in range(1,11):
    print(f"{num} x {i} = {num*i}")

# print even numbers from 1 to 20 using for loop
for i in range(1,21):
    if(i % 2 == 0):
        print(i)
# print odd numbers from 1 to 20 using for loop
for i in range(1,21):
    if(i % 2 != 0):
        print(i)
# print sum of first n natural numbers using for loop
n = int(input("Enter a number: "))
sum = 0
for i in range(1,n+1):
    sum += i
print(f"The sum of first {n} natural numbers is {sum}")
# print factorial of a number using for loop
num = int(input("Enter a number to find its factorial: "))
factorial = 1
for i in range(1,num+1):
    factorial *= i
print(f"The factorial of {num} is {factorial}")
# print reverse of a number using for loop
num = int(input("Enter a number to find its reverse: "))
reverse = 0
for i in str(num):
    reverse = i + str(reverse)
print(f"The reverse of {num} is {reverse}")

