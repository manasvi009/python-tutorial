def grater(a ,b ,c):
    if a > b and a > c:
        print(f"{a} is grater")
    elif b > a and b > c:
        print(f"{b} is grater")
    else:
        print(f"{c} is grater")
a = int(input("Enter first number :"))
b = int(input("Enter second number :"))
c = int(input("Enter third number :"))
grater(a ,b ,c)
