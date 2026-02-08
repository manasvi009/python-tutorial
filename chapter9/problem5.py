list = ["Donkey" , "Monkey" , "Horse"]
with open("C:/Users/PC/Desktop/python/chapter9/problem5.txt") as f:
    content = f.read()

for word in list:
    content = content.replace(word , "######")

    with open("C:/Users/PC/Desktop/python/chapter9/problem5.txt" , "w") as f:
        f.write(content)

        print("All words are updated successfully!!!")