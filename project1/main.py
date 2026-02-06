import random

def game(comp, user):
    if comp == user:
        return None

    if comp == 's' and user == 'w':
        return False
    elif comp == 'w' and user == 'g':
        return False
    elif comp == 'g' and user == 's':
        return False
    else:
        return True


print("Computer's turn: Snake(s) Water(w) or Gun(g)?")
randNo = random.randint(1, 3)

if randNo == 1:
    comp = 's'
elif randNo == 2:
    comp = 'w'
else:
    comp = 'g'

user = input("Your turn: Snake(s) Water(w) or Gun(g)? ")

result = game(comp, user)

print(f"Computer chose: {comp}")
print(f"You chose: {user}")

if result is None:
    print("🎯 The game is a draw!")
elif result:
    print("🎉 You win!")
else:
    print("💀 You lose!")
