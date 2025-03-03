import random
import string

def generate_random_string(length=30):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

word_list = ["experiment", "attachment", "overcharge", "projection", "connection", "commitment", "understand", "provincial", "discourage", "systemmatic", "withdrawl", "generation", "vegetation", "restaurant", "memorandum", "reluctance", "tournamnet", "brilliance"]

for word in word_list:
        with open(word + ".txt", "w") as file:
           file.write(f"flag{{" + generate_random_string(30) + "}")

chosen_file = word_list[random.randint(0, len(word_list) - 1)]
shift = random.randint(4, 16)

shifted_word = ""
for char in chosen_file:
    shifted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
    shifted_word += shifted_char

print(chosen_file)
print(shift)
print(shifted_word)