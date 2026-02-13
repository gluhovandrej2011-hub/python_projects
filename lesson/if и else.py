


import random

comp_number = random.randint(1,100)
user_number = 0
is_guess = False

print("Я загадал число от 1 до 100. Попробуй отгадай")

while is_guess == False:
    user_number = int(input("введи своё число: "))
    
    if user_number > comp_number:
        print("Введите поменьше")
    elif user_number < comp_number:
        print("Введите побольше")
    else:
        print("Ураа вы победили")
        is_guess = True