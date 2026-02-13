filename = "file.txt"
text = "Здравствуй мир!"
file = open(filename, 'w', encoding = "utf-8")
file.write(text)
file.close()
print(text)