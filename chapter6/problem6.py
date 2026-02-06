mark = int (input("Enter your mark: "))

if (mark >= 90 and mark <= 100):
    print("Your grade is Excellent.")
elif (mark >= 80 and mark < 90):
    print("Your grade is A.")
elif (mark >= 70 and mark < 80):
    print("Your grade is B.")
elif (mark >= 60 and mark < 70):
    print("Your grade is C.")
elif (mark >= 50 and mark < 60):
    print("Your grade is D.")
else:
    print("Your grade is F.")