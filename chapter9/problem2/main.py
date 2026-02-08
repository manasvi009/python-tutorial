import random

def game():
    # Random score between 1 and 100
    return random.randint(1, 100)


score = game()

# Read previous high score
try:
    with open("Hi-score.txt", "r") as f:
        content = f.read()
        if content == "":
            high_score = 0
        else:
            high_score = int(content)

except FileNotFoundError:
    high_score = 0


# Compare and update high score
if score > high_score:
    print("🎉 New High Score!")
    with open("Hi-score.txt", "w") as f:
        f.write(str(score))
else:
    print("High Score not broken")

print("Your Score:", score)
print("High Score:", max(score, high_score))
