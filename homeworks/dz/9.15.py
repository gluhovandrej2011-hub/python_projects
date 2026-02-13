print("введите слово")
word = input()
print("введите символ который нужно узнать")
k = input()
n = int(k)
i = n - 1
if i >= 0 and i < len(word):
    ks = word[i]
    print(ks)
else:
    print("ошибка")
    print(f"нужно ввести слово имеющее от 1 до {len(word)} букв")