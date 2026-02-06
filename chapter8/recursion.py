#recursion is a function which calls itself
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)
number = int(input("Enter a number :"))
print(f"Factorial of {number} is {factorial(number)}")


'''
factorial(0) = 1
factorial(1) = 1
factorial(2) = 2 * factorial(1) = 2 * 1 = 2
factorial(3) = 3 * factorial(2) = 3 * 2
factorial(4) = 4 * factorial(3) = 4 * 6
factorial(5) = 5 * factorial(4) = 5 * 24
factorial(6) = 6 * factorial(5) = 6 * 120
factorial(7) = 7 * factorial(6) = 7 * 720
factorial(8) = 8 * factorial(7) = 8 * 5040
factorial(9) = 9 * factorial(8) = 9 * 40320
factorial(10) = 10 * factorial(9) = 10 * 362880

factorial(n) = n * factorial(n-1)
'''