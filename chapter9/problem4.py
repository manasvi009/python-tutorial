with open("C:/Users/PC/Desktop/python/chapter9/problem4.txt") as f:
    content = f.read()

    content = content.replace("Donkey" , "######")

    with open("C:/Users/PC/Desktop/python/chapter9/problem4.txt" , "w") as f:
        f.write(content)

        print("Donkey is replaced")
                              