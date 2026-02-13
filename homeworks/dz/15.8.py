filename = "file.txt"
line = 0
file = open(filename, 'r', encoding="utf-8")
for line in file:
    line = line + 1
print(str(line))
