def main():
    x = 0
    y = 0
    while x < 10:
        x += 1
        y += 1
        yield (x,y)

for x in main():
    print(x)