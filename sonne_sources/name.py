import random

letters = "abcdefg"
name = ""
for _ in range(8):
    rand_letter = letters[random.randint(0, (len(letters) - 1))]
    name = name + rand_letter

sonne_var("random_name", name)


